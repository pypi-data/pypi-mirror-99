"""

Copyright (c) 2020 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import logging
from collections import namedtuple

import cocotb
from cocotb.queue import Queue
from cocotb.triggers import Event

from .version import __version__
from .constants import AxiProt, AxiResp
from .axil_channels import AxiLiteAWSource, AxiLiteWSource, AxiLiteBSink, AxiLiteARSource, AxiLiteRSink
from .reset import Reset

# AXI lite master write
AxiLiteWriteCmd = namedtuple("AxiLiteWriteCmd", ["address", "data", "prot", "event"])
AxiLiteWriteRespCmd = namedtuple("AxiLiteWriteRespCmd", ["address", "length", "cycles", "prot", "event"])
AxiLiteWriteResp = namedtuple("AxiLiteWriteResp", ["address", "length", "resp"])

# AXI lite master read
AxiLiteReadCmd = namedtuple("AxiLiteReadCmd", ["address", "length", "prot", "event"])
AxiLiteReadRespCmd = namedtuple("AxiLiteReadRespCmd", ["address", "length", "cycles", "prot", "event"])
AxiLiteReadResp = namedtuple("AxiLiteReadResp", ["address", "data", "resp"])


class AxiLiteMasterWrite(Reset):
    def __init__(self, bus, clock, reset=None, reset_active_level=True):
        self.log = logging.getLogger(f"cocotb.{bus.aw._entity._name}.{bus.aw._name}")

        self.log.info("AXI lite master (write)")
        self.log.info("cocotbext-axi version %s", __version__)
        self.log.info("Copyright (c) 2020 Alex Forencich")
        self.log.info("https://github.com/alexforencich/cocotbext-axi")

        self.aw_channel = AxiLiteAWSource(bus.aw, clock, reset, reset_active_level)
        self.aw_channel.queue_occupancy_limit = 2
        self.w_channel = AxiLiteWSource(bus.w, clock, reset, reset_active_level)
        self.w_channel.queue_occupancy_limit = 2
        self.b_channel = AxiLiteBSink(bus.b, clock, reset, reset_active_level)
        self.b_channel.queue_occupancy_limit = 2

        self.write_command_queue = Queue()
        self.current_write_command = None

        self.int_write_resp_command_queue = Queue()
        self.current_write_resp_command = None

        self.in_flight_operations = 0
        self._idle = Event()
        self._idle.set()

        self.width = len(self.w_channel.bus.wdata)
        self.byte_size = 8
        self.byte_width = self.width // self.byte_size
        self.strb_mask = 2**self.byte_width-1

        self.log.info("AXI lite master configuration:")
        self.log.info("  Address width: %d bits", len(self.aw_channel.bus.awaddr))
        self.log.info("  Byte size: %d bits", self.byte_size)
        self.log.info("  Data width: %d bits (%d bytes)", self.width, self.byte_width)

        assert self.byte_width == len(self.w_channel.bus.wstrb)
        assert self.byte_width * self.byte_size == self.width

        self._process_write_cr = None
        self._process_write_resp_cr = None

        self._init_reset(reset, reset_active_level)

    def init_write(self, address, data, prot=AxiProt.NONSECURE, event=None):
        if event is None:
            event = Event()

        if not isinstance(event, Event):
            raise ValueError("Expected event object")

        self.in_flight_operations += 1
        self._idle.clear()

        self.write_command_queue.put_nowait(AxiLiteWriteCmd(address, bytearray(data), prot, event))

        return event

    def idle(self):
        return not self.in_flight_operations

    async def wait(self):
        while not self.idle():
            await self._idle.wait()

    async def write(self, address, data, prot=AxiProt.NONSECURE):
        event = self.init_write(address, data, prot)
        await event.wait()
        return event.data

    async def write_words(self, address, data, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        words = data
        data = bytearray()
        for w in words:
            data.extend(w.to_bytes(ws, byteorder))
        await self.write(address, data, prot)

    async def write_dwords(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        await self.write_words(address, data, byteorder, 4, prot)

    async def write_qwords(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        await self.write_words(address, data, byteorder, 8, prot)

    async def write_byte(self, address, data, prot=AxiProt.NONSECURE):
        await self.write(address, [data], prot)

    async def write_word(self, address, data, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        await self.write_words(address, [data], byteorder, ws, prot)

    async def write_dword(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        await self.write_dwords(address, [data], byteorder, prot)

    async def write_qword(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        await self.write_qwords(address, [data], byteorder, prot)

    def _handle_reset(self, state):
        if state:
            self.log.info("Reset asserted")
            if self._process_write_cr is not None:
                self._process_write_cr.kill()
                self._process_write_cr = None
            if self._process_write_resp_cr is not None:
                self._process_write_resp_cr.kill()
                self._process_write_resp_cr = None

            self.aw_channel.clear()
            self.w_channel.clear()
            self.b_channel.clear()

            def flush_cmd(cmd):
                self.log.warning("Flushed write operation during reset: %s", cmd)
                if cmd.event:
                    cmd.event.set(None)

            while not self.write_command_queue.empty():
                cmd = self.write_command_queue.get_nowait()
                flush_cmd(cmd)

            if self.current_write_command:
                cmd = self.current_write_command
                self.current_write_command = None
                flush_cmd(cmd)

            while not self.int_write_resp_command_queue.empty():
                cmd = self.int_write_resp_command_queue.get_nowait()
                flush_cmd(cmd)

            if self.current_write_resp_command:
                cmd = self.current_write_resp_command
                self.current_write_resp_command = None
                flush_cmd(cmd)

            self.in_flight_operations = 0
            self._idle.set()
        else:
            self.log.info("Reset de-asserted")
            if self._process_write_cr is None:
                self._process_write_cr = cocotb.fork(self._process_write())
            if self._process_write_resp_cr is None:
                self._process_write_resp_cr = cocotb.fork(self._process_write_resp())

    async def _process_write(self):
        while True:
            cmd = await self.write_command_queue.get()
            self.current_write_command = cmd

            word_addr = (cmd.address // self.byte_width) * self.byte_width

            start_offset = cmd.address % self.byte_width
            end_offset = ((cmd.address + len(cmd.data) - 1) % self.byte_width) + 1

            strb_start = (self.strb_mask << start_offset) & self.strb_mask
            strb_end = self.strb_mask >> (self.byte_width - end_offset)

            cycles = (len(cmd.data) + (cmd.address % self.byte_width) + self.byte_width-1) // self.byte_width

            resp_cmd = AxiLiteWriteRespCmd(cmd.address, len(cmd.data), cycles, cmd.prot, cmd.event)
            await self.int_write_resp_command_queue.put(resp_cmd)

            offset = 0

            self.log.info("Write start addr: 0x%08x prot: %s data: %s",
                cmd.address, cmd.prot, ' '.join((f'{c:02x}' for c in cmd.data)))

            for k in range(cycles):
                start = 0
                stop = self.byte_width
                strb = self.strb_mask

                if k == 0:
                    start = start_offset
                    strb &= strb_start
                if k == cycles-1:
                    stop = end_offset
                    strb &= strb_end

                val = 0
                for j in range(start, stop):
                    val |= cmd.data[offset] << j*8
                    offset += 1

                aw = self.aw_channel._transaction_obj()
                aw.awaddr = word_addr + k*self.byte_width
                aw.awprot = cmd.prot

                w = self.w_channel._transaction_obj()
                w.wdata = val
                w.wstrb = strb

                await self.aw_channel.send(aw)
                await self.w_channel.send(w)

            self.current_write_command = None

    async def _process_write_resp(self):
        while True:
            cmd = await self.int_write_resp_command_queue.get()
            self.current_write_resp_command = cmd

            resp = AxiResp.OKAY

            for k in range(cmd.cycles):
                b = await self.b_channel.recv()

                cycle_resp = AxiResp(b.bresp)

                if cycle_resp != AxiResp.OKAY:
                    resp = cycle_resp

            self.log.info("Write complete addr: 0x%08x prot: %s resp: %s length: %d",
                cmd.address, cmd.prot, resp, cmd.length)

            write_resp = AxiLiteWriteResp(cmd.address, cmd.length, resp)

            cmd.event.set(write_resp)

            self.current_write_resp_command = None

            self.in_flight_operations -= 1

            if self.in_flight_operations == 0:
                self._idle.set()


class AxiLiteMasterRead(Reset):
    def __init__(self, bus, clock, reset=None, reset_active_level=True):
        self.log = logging.getLogger(f"cocotb.{bus.ar._entity._name}.{bus.ar._name}")

        self.log.info("AXI lite master (read)")
        self.log.info("cocotbext-axi version %s", __version__)
        self.log.info("Copyright (c) 2020 Alex Forencich")
        self.log.info("https://github.com/alexforencich/cocotbext-axi")

        self.ar_channel = AxiLiteARSource(bus.ar, clock, reset, reset_active_level)
        self.ar_channel.queue_occupancy_limit = 2
        self.r_channel = AxiLiteRSink(bus.r, clock, reset, reset_active_level)
        self.r_channel.queue_occupancy_limit = 2

        self.read_command_queue = Queue()
        self.current_read_command = None

        self.int_read_resp_command_queue = Queue()
        self.current_read_resp_command = None

        self.in_flight_operations = 0
        self._idle = Event()
        self._idle.set()

        self.width = len(self.r_channel.bus.rdata)
        self.byte_size = 8
        self.byte_width = self.width // self.byte_size

        self.log.info("AXI lite master configuration:")
        self.log.info("  Address width: %d bits", len(self.ar_channel.bus.araddr))
        self.log.info("  Byte size: %d bits", self.byte_size)
        self.log.info("  Data width: %d bits (%d bytes)", self.width, self.byte_width)

        assert self.byte_width * self.byte_size == self.width

        self._process_read_cr = None
        self._process_read_resp_cr = None

        self._init_reset(reset, reset_active_level)

    def init_read(self, address, length, prot=AxiProt.NONSECURE, event=None):
        if event is None:
            event = Event()

        if not isinstance(event, Event):
            raise ValueError("Expected event object")

        self.in_flight_operations += 1
        self._idle.clear()

        self.read_command_queue.put_nowait(AxiLiteReadCmd(address, length, prot, event))

        return event

    def idle(self):
        return not self.in_flight_operations

    async def wait(self):
        while not self.idle():
            await self._idle.wait()

    async def read(self, address, length, prot=AxiProt.NONSECURE):
        event = self.init_read(address, length, prot)
        await event.wait()
        return event.data

    async def read_words(self, address, count, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        data = await self.read(address, count*ws, prot)
        words = []
        for k in range(count):
            words.append(int.from_bytes(data.data[ws*k:ws*(k+1)], byteorder))
        return words

    async def read_dwords(self, address, count, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.read_words(address, count, byteorder, 4, prot)

    async def read_qwords(self, address, count, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.read_words(address, count, byteorder, 8, prot)

    async def read_byte(self, address, prot=AxiProt.NONSECURE):
        return (await self.read(address, 1, prot)).data[0]

    async def read_word(self, address, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        return (await self.read_words(address, 1, byteorder, ws, prot))[0]

    async def read_dword(self, address, byteorder='little', prot=AxiProt.NONSECURE):
        return (await self.read_dwords(address, 1, byteorder, prot))[0]

    async def read_qword(self, address, byteorder='little', prot=AxiProt.NONSECURE):
        return (await self.read_qwords(address, 1, byteorder, prot))[0]

    def _handle_reset(self, state):
        if state:
            self.log.info("Reset asserted")
            if self._process_read_cr is not None:
                self._process_read_cr.kill()
                self._process_read_cr = None
            if self._process_read_resp_cr is not None:
                self._process_read_resp_cr.kill()
                self._process_read_resp_cr = None

            self.ar_channel.clear()
            self.r_channel.clear()

            def flush_cmd(cmd):
                self.log.warning("Flushed read operation during reset: %s", cmd)
                if cmd.event:
                    cmd.event.set(None)

            while not self.read_command_queue.empty():
                cmd = self.read_command_queue.get_nowait()
                flush_cmd(cmd)

            if self.current_read_command:
                cmd = self.current_read_command
                self.current_read_command = None
                flush_cmd(cmd)

            while not self.int_read_resp_command_queue.empty():
                cmd = self.int_read_resp_command_queue.get_nowait()
                flush_cmd(cmd)

            if self.current_read_resp_command:
                cmd = self.current_read_resp_command
                self.current_read_resp_command = None
                flush_cmd(cmd)

            self.in_flight_operations = 0
            self._idle.set()
        else:
            self.log.info("Reset de-asserted")
            if self._process_read_cr is None:
                self._process_read_cr = cocotb.fork(self._process_read())
            if self._process_read_resp_cr is None:
                self._process_read_resp_cr = cocotb.fork(self._process_read_resp())

    async def _process_read(self):
        while True:
            cmd = await self.read_command_queue.get()
            self.current_read_command = cmd

            word_addr = (cmd.address // self.byte_width) * self.byte_width

            cycles = (cmd.length + self.byte_width-1 + (cmd.address % self.byte_width)) // self.byte_width

            resp_cmd = AxiLiteReadRespCmd(cmd.address, cmd.length, cycles, cmd.prot, cmd.event)
            await self.int_read_resp_command_queue.put(resp_cmd)

            self.log.info("Read start addr: 0x%08x prot: %s length: %d",
                cmd.address, cmd.prot, cmd.length)

            for k in range(cycles):
                ar = self.ar_channel._transaction_obj()
                ar.araddr = word_addr + k*self.byte_width
                ar.arprot = cmd.prot

                await self.ar_channel.send(ar)

            self.current_read_command = None

    async def _process_read_resp(self):
        while True:
            cmd = await self.int_read_resp_command_queue.get()
            self.current_read_resp_command = cmd

            start_offset = cmd.address % self.byte_width
            end_offset = ((cmd.address + cmd.length - 1) % self.byte_width) + 1

            data = bytearray()

            resp = AxiResp.OKAY

            for k in range(cmd.cycles):
                r = await self.r_channel.recv()

                cycle_data = int(r.rdata)
                cycle_resp = AxiResp(r.rresp)

                if cycle_resp != AxiResp.OKAY:
                    resp = cycle_resp

                start = 0
                stop = self.byte_width

                if k == 0:
                    start = start_offset
                if k == cmd.cycles-1:
                    stop = end_offset

                for j in range(start, stop):
                    data.extend(bytearray([(cycle_data >> j*8) & 0xff]))

            self.log.info("Read complete addr: 0x%08x prot: %s resp: %s data: %s",
                cmd.address, cmd.prot, resp, ' '.join((f'{c:02x}' for c in data)))

            read_resp = AxiLiteReadResp(cmd.address, data, resp)

            cmd.event.set(read_resp)

            self.current_read_resp_command = None

            self.in_flight_operations -= 1

            if self.in_flight_operations == 0:
                self._idle.set()


class AxiLiteMaster:
    def __init__(self, bus, clock, reset=None, reset_active_level=True):
        self.write_if = None
        self.read_if = None

        self.write_if = AxiLiteMasterWrite(bus.write, clock, reset, reset_active_level)
        self.read_if = AxiLiteMasterRead(bus.read, clock, reset, reset_active_level)

    def init_read(self, address, length, prot=AxiProt.NONSECURE, event=None):
        return self.read_if.init_read(address, length, prot, event)

    def init_write(self, address, data, prot=AxiProt.NONSECURE, event=None):
        return self.write_if.init_write(address, data, prot, event)

    def idle(self):
        return (not self.read_if or self.read_if.idle()) and (not self.write_if or self.write_if.idle())

    async def wait(self):
        while not self.idle():
            await self.write_if.wait()
            await self.read_if.wait()

    async def wait_read(self):
        await self.read_if.wait()

    async def wait_write(self):
        await self.write_if.wait()

    async def read(self, address, length, prot=AxiProt.NONSECURE):
        return await self.read_if.read(address, length, prot)

    async def read_words(self, address, count, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        return await self.read_if.read_words(address, count, byteorder, ws, prot)

    async def read_dwords(self, address, count, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.read_if.read_dwords(address, count, byteorder, prot)

    async def read_qwords(self, address, count, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.read_if.read_qwords(address, count, byteorder, prot)

    async def read_byte(self, address, prot=AxiProt.NONSECURE):
        return await self.read_if.read_byte(address, prot)

    async def read_word(self, address, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        return await self.read_if.read_word(address, byteorder, ws, prot)

    async def read_dword(self, address, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.read_if.read_dword(address, byteorder, prot)

    async def read_qword(self, address, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.read_if.read_qword(address, byteorder, prot)

    async def write(self, address, data, prot=AxiProt.NONSECURE):
        return await self.write_if.write(address, data, prot)

    async def write_words(self, address, data, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        return await self.write_if.write_words(address, data, byteorder, ws, prot)

    async def write_dwords(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.write_if.write_dwords(address, data, byteorder, prot)

    async def write_qwords(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.write_if.write_qwords(address, data, byteorder, prot)

    async def write_byte(self, address, data, prot=AxiProt.NONSECURE):
        return await self.write_if.write_byte(address, data, prot)

    async def write_word(self, address, data, byteorder='little', ws=2, prot=AxiProt.NONSECURE):
        return await self.write_if.write_word(address, data, byteorder, ws, prot)

    async def write_dword(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.write_if.write_dword(address, data, byteorder, prot)

    async def write_qword(self, address, data, byteorder='little', prot=AxiProt.NONSECURE):
        return await self.write_if.write_qword(address, data, byteorder, prot)
