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
from collections import namedtuple, Counter

import cocotb
from cocotb.queue import Queue
from cocotb.triggers import Event

from .version import __version__
from .constants import AxiBurstType, AxiLockType, AxiProt, AxiResp
from .axi_channels import AxiAWSource, AxiWSource, AxiBSink, AxiARSource, AxiRSink
from .reset import Reset

# AXI master write helper objects
AxiWriteCmd = namedtuple("AxiWriteCmd", ["address", "data", "awid", "burst", "size",
    "lock", "cache", "prot", "qos", "region", "user", "wuser", "event"])
AxiWriteRespCmd = namedtuple("AxiWriteRespCmd", ["address", "length", "size", "cycles",
    "prot", "burst_list", "event"])
AxiWriteResp = namedtuple("AxiWriteResp", ["address", "length", "resp", "user"])

# AXI master read helper objects
AxiReadCmd = namedtuple("AxiReadCmd", ["address", "length", "arid", "burst", "size",
    "lock", "cache", "prot", "qos", "region", "user", "event"])
AxiReadRespCmd = namedtuple("AxiReadRespCmd", ["address", "length", "size", "cycles",
    "prot", "burst_list", "event"])
AxiReadResp = namedtuple("AxiReadResp", ["address", "data", "resp", "user"])


class AxiMasterWrite(Reset):
    def __init__(self, bus, clock, reset=None, reset_active_level=True, max_burst_len=256):
        self.log = logging.getLogger(f"cocotb.{bus.aw._entity._name}.{bus.aw._name}")

        self.log.info("AXI master (write)")
        self.log.info("cocotbext-axi version %s", __version__)
        self.log.info("Copyright (c) 2020 Alex Forencich")
        self.log.info("https://github.com/alexforencich/cocotbext-axi")

        self.aw_channel = AxiAWSource(bus.aw, clock, reset, reset_active_level)
        self.aw_channel.queue_occupancy_limit = 2
        self.w_channel = AxiWSource(bus.w, clock, reset, reset_active_level)
        self.w_channel.queue_occupancy_limit = 2
        self.b_channel = AxiBSink(bus.b, clock, reset, reset_active_level)
        self.b_channel.queue_occupancy_limit = 2

        self.write_command_queue = Queue()
        self.current_write_command = None

        self.id_count = 2**len(self.aw_channel.bus.awid)
        self.cur_id = 0
        self.active_id = Counter()

        self.int_write_resp_command_queue = [Queue() for k in range(self.id_count)]
        self.current_write_resp_command = [None for k in range(self.id_count)]
        self.int_write_resp_queue_list = [Queue() for k in range(self.id_count)]

        self.in_flight_operations = 0
        self._idle = Event()
        self._idle.set()

        self.width = len(self.w_channel.bus.wdata)
        self.byte_size = 8
        self.byte_width = self.width // self.byte_size
        self.strb_mask = 2**self.byte_width-1

        self.max_burst_len = max(min(max_burst_len, 256), 1)
        self.max_burst_size = (self.byte_width-1).bit_length()

        self.log.info("AXI master configuration:")
        self.log.info("  Address width: %d bits", len(self.aw_channel.bus.awaddr))
        self.log.info("  ID width: %d bits", len(self.aw_channel.bus.awid))
        self.log.info("  Byte size: %d bits", self.byte_size)
        self.log.info("  Data width: %d bits (%d bytes)", self.width, self.byte_width)
        self.log.info("  Max burst size: %d (%d bytes)", self.max_burst_size, 2**self.max_burst_size)
        self.log.info("  Max burst length: %d cycles (%d bytes)",
            self.max_burst_len, self.max_burst_len*self.byte_width)

        assert self.byte_width == len(self.w_channel.bus.wstrb)
        assert self.byte_width * self.byte_size == self.width

        assert len(self.b_channel.bus.bid) == len(self.aw_channel.bus.awid)

        self._process_write_cr = None
        self._process_write_resp_cr = None
        self._process_write_resp_id_cr = None

        self._init_reset(reset, reset_active_level)

    def init_write(self, address, data, awid=None, burst=AxiBurstType.INCR, size=None, lock=AxiLockType.NORMAL,
            cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0, event=None):

        if event is None:
            event = Event()

        if not isinstance(event, Event):
            raise ValueError("Expected event object")

        if awid is None or awid < 0:
            awid = None
        elif awid > self.id_count:
            raise ValueError("Requested ID exceeds maximum ID allowed for ID signal width")

        burst = AxiBurstType(burst)

        if size is None or size < 0:
            size = self.max_burst_size
        elif size > self.max_burst_size:
            raise ValueError("Requested burst size exceeds maximum burst size allowed for bus width")

        lock = AxiLockType(lock)
        prot = AxiProt(prot)

        if wuser is None:
            wuser = 0
        elif isinstance(wuser, int):
            pass
        else:
            wuser = list(wuser)

        self.in_flight_operations += 1
        self._idle.clear()

        cmd = AxiWriteCmd(address, bytearray(data), awid, burst, size, lock,
            cache, prot, qos, region, user, wuser, event)
        self.write_command_queue.put_nowait(cmd)

        return event

    def idle(self):
        return not self.in_flight_operations

    async def wait(self):
        while not self.idle():
            await self._idle.wait()

    async def write(self, address, data, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        event = self.init_write(address, data, awid, burst, size, lock, cache, prot, qos, region, user, wuser)
        await event.wait()
        return event.data

    async def write_words(self, address, data, byteorder='little', ws=2, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        words = data
        data = bytearray()
        for w in words:
            data.extend(w.to_bytes(ws, byteorder))
        await self.write(address, data, awid, burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_dwords(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        await self.write_words(address, data, byteorder, 4, awid, burst, size,
            lock, cache, prot, qos, region, user, wuser)

    async def write_qwords(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        await self.write_words(address, data, byteorder, 8, awid, burst, size,
            lock, cache, prot, qos, region, user, wuser)

    async def write_byte(self, address, data, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        await self.write(address, [data], awid, burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_word(self, address, data, byteorder='little', ws=2, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        await self.write_words(address, [data], byteorder, ws, awid, burst, size,
            lock, cache, prot, qos, region, user, wuser)

    async def write_dword(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        await self.write_dwords(address, [data], byteorder, awid, burst, size,
            lock, cache, prot, qos, region, user, wuser)

    async def write_qword(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        await self.write_qwords(address, [data], byteorder, awid, burst, size,
            lock, cache, prot, qos, region, user, wuser)

    def _handle_reset(self, state):
        if state:
            self.log.info("Reset asserted")
            if self._process_write_cr is not None:
                self._process_write_cr.kill()
                self._process_write_cr = None
            if self._process_write_resp_cr is not None:
                self._process_write_resp_cr.kill()
                self._process_write_resp_cr = None
            if self._process_write_resp_id_cr is not None:
                for cr in self._process_write_resp_id_cr:
                    cr.kill()
                self._process_write_resp_id_cr = None

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

            for q in self.int_write_resp_command_queue:
                while not q.empty():
                    cmd = q.get_nowait()
                    flush_cmd(cmd)

            for k in range(len(self.current_write_resp_command)):
                if self.current_write_resp_command[k]:
                    cmd = self.current_write_resp_command[k]
                    self.current_write_resp_command[k] = None
                    flush_cmd(cmd)

            for q in self.int_write_resp_queue_list:
                while not q.empty():
                    q.get_nowait()

            self.cur_id = 0
            self.active_id = Counter()

            self.in_flight_operations = 0
            self._idle.set()
        else:
            self.log.info("Reset de-asserted")
            if self._process_write_cr is None:
                self._process_write_cr = cocotb.fork(self._process_write())
            if self._process_write_resp_cr is None:
                self._process_write_resp_cr = cocotb.fork(self._process_write_resp())
            if self._process_write_resp_id_cr is None:
                self._process_write_resp_id_cr = [cocotb.fork(self._process_write_resp_id(i)) for i in range(self.id_count)]

    async def _process_write(self):
        while True:
            cmd = await self.write_command_queue.get()
            self.current_write_command = cmd

            num_bytes = 2**cmd.size

            aligned_addr = (cmd.address // num_bytes) * num_bytes
            word_addr = (cmd.address // self.byte_width) * self.byte_width

            start_offset = cmd.address % self.byte_width
            end_offset = ((cmd.address + len(cmd.data) - 1) % self.byte_width) + 1

            cycles = (len(cmd.data) + (cmd.address % num_bytes) + num_bytes-1) // num_bytes

            cur_addr = aligned_addr
            offset = 0
            cycle_offset = aligned_addr-word_addr
            n = 0
            transfer_count = 0

            burst_list = []
            burst_length = 0

            if cmd.awid is not None:
                awid = cmd.awid
            else:
                awid = self.cur_id
                self.cur_id = (self.cur_id+1) % self.id_count

            wuser = cmd.wuser

            self.log.info("Write start addr: 0x%08x awid: 0x%x prot: %s data: %s",
                cmd.address, awid, cmd.prot, ' '.join((f'{c:02x}' for c in cmd.data)))

            for k in range(cycles):
                start = cycle_offset
                stop = cycle_offset+num_bytes

                if k == 0:
                    start = start_offset
                if k == cycles-1:
                    stop = end_offset

                strb = (self.strb_mask << start) & self.strb_mask & (self.strb_mask >> (self.byte_width - stop))

                val = 0
                for j in range(start, stop):
                    val |= cmd.data[offset] << j*8
                    offset += 1

                if n >= burst_length:
                    transfer_count += 1
                    n = 0

                    # split on burst length
                    burst_length = min(cycles-k, min(max(self.max_burst_len, 1), 256))
                    # split on 4k address boundary
                    burst_length = (min(burst_length*num_bytes, 0x1000-(cur_addr & 0xfff))+num_bytes-1)//num_bytes

                    burst_list.append(burst_length)

                    aw = self.aw_channel._transaction_obj()
                    aw.awid = awid
                    aw.awaddr = cur_addr
                    aw.awlen = burst_length-1
                    aw.awsize = cmd.size
                    aw.awburst = cmd.burst
                    aw.awlock = cmd.lock
                    aw.awcache = cmd.cache
                    aw.awprot = cmd.prot
                    aw.awqos = cmd.qos
                    aw.awregion = cmd.region
                    aw.awuser = cmd.user

                    self.active_id[awid] += 1
                    await self.aw_channel.send(aw)

                    self.log.info("Write burst start awid: 0x%x awaddr: 0x%08x awlen: %d awsize: %d awprot: %s",
                        awid, cur_addr, burst_length-1, cmd.size, cmd.prot)

                n += 1

                w = self.w_channel._transaction_obj()
                w.wdata = val
                w.wstrb = strb
                w.wlast = n >= burst_length

                if isinstance(wuser, int):
                    w.wuser = wuser
                else:
                    if wuser:
                        w.wuser = wuser.pop(0)
                    else:
                        w.wuser = 0

                await self.w_channel.send(w)

                cur_addr += num_bytes
                cycle_offset = (cycle_offset + num_bytes) % self.byte_width

            resp_cmd = AxiWriteRespCmd(cmd.address, len(cmd.data), cmd.size, cycles, cmd.prot, burst_list, cmd.event)
            await self.int_write_resp_command_queue[awid].put(resp_cmd)

            self.current_write_command = None

    async def _process_write_resp(self):
        while True:
            b = await self.b_channel.recv()

            bid = int(b.bid)

            if self.active_id[bid] <= 0:
                raise Exception(f"Unexpected burst ID {bid}")

            await self.int_write_resp_queue_list[bid].put(b)

    async def _process_write_resp_id(self, bid):
        while True:
            cmd = await self.int_write_resp_command_queue[bid].get()
            self.current_write_resp_command[bid] = cmd

            resp = AxiResp.OKAY
            user = []

            for burst_length in cmd.burst_list:
                b = await self.int_write_resp_queue_list[bid].get()

                burst_id = int(b.bid)
                burst_resp = AxiResp(b.bresp)
                burst_user = int(b.buser)

                if burst_resp != AxiResp.OKAY:
                    resp = burst_resp

                if burst_user is not None:
                    user.append(burst_user)

                if self.active_id[bid] <= 0:
                    raise Exception(f"Unexpected burst ID {bid}")

                self.active_id[bid] -= 1

                self.log.info("Write burst complete bid: 0x%x bresp: %s", burst_id, burst_resp)

            self.log.info("Write complete addr: 0x%08x prot: %s resp: %s length: %d",
                cmd.address, cmd.prot, resp, cmd.length)

            write_resp = AxiWriteResp(cmd.address, cmd.length, resp, user)

            cmd.event.set(write_resp)

            self.current_write_resp_command[bid] = None

            self.in_flight_operations -= 1

            if self.in_flight_operations == 0:
                self._idle.set()


class AxiMasterRead(Reset):
    def __init__(self, bus, clock, reset=None, reset_active_level=True, max_burst_len=256):
        self.log = logging.getLogger(f"cocotb.{bus.ar._entity._name}.{bus.ar._name}")

        self.log.info("AXI master (read)")
        self.log.info("cocotbext-axi version %s", __version__)
        self.log.info("Copyright (c) 2020 Alex Forencich")
        self.log.info("https://github.com/alexforencich/cocotbext-axi")

        self.ar_channel = AxiARSource(bus.ar, clock, reset, reset_active_level)
        self.ar_channel.queue_occupancy_limit = 2
        self.r_channel = AxiRSink(bus.r, clock, reset, reset_active_level)
        self.r_channel.queue_occupancy_limit = 2

        self.read_command_queue = Queue()
        self.current_read_command = None

        self.id_count = 2**len(self.ar_channel.bus.arid)
        self.cur_id = 0
        self.active_id = Counter()

        self.int_read_resp_command_queue = [Queue() for k in range(self.id_count)]
        self.current_read_resp_command = [None for k in range(self.id_count)]
        self.int_read_resp_queue_list = [Queue() for k in range(self.id_count)]

        self.in_flight_operations = 0
        self._idle = Event()
        self._idle.set()

        self.width = len(self.r_channel.bus.rdata)
        self.byte_size = 8
        self.byte_width = self.width // self.byte_size

        self.max_burst_len = max(min(max_burst_len, 256), 1)
        self.max_burst_size = (self.byte_width-1).bit_length()

        self.log.info("AXI master configuration:")
        self.log.info("  Address width: %d bits", len(self.ar_channel.bus.araddr))
        self.log.info("  ID width: %d bits", len(self.ar_channel.bus.arid))
        self.log.info("  Byte size: %d bits", self.byte_size)
        self.log.info("  Data width: %d bits (%d bytes)", self.width, self.byte_width)
        self.log.info("  Max burst size: %d (%d bytes)", self.max_burst_size, 2**self.max_burst_size)
        self.log.info("  Max burst length: %d cycles (%d bytes)",
            self.max_burst_len, self.max_burst_len*self.byte_width)

        assert self.byte_width * self.byte_size == self.width

        assert len(self.r_channel.bus.rid) == len(self.ar_channel.bus.arid)

        self._process_read_cr = None
        self._process_read_resp_cr = None
        self._process_read_resp_id_cr = None

        self._init_reset(reset, reset_active_level)

    def init_read(self, address, length, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, event=None):

        if event is None:
            event = Event()

        if not isinstance(event, Event):
            raise ValueError("Expected event object")

        if length < 0:
            raise ValueError("Read length must be positive")

        if arid is None or arid < 0:
            arid = None
        elif arid > self.id_count:
            raise ValueError("Requested ID exceeds maximum ID allowed for ID signal width")

        burst = AxiBurstType(burst)

        if size is None or size < 0:
            size = self.max_burst_size
        elif size > self.max_burst_size:
            raise ValueError("Requested burst size exceeds maximum burst size allowed for bus width")

        lock = AxiLockType(lock)
        prot = AxiProt(prot)

        self.in_flight_operations += 1
        self._idle.clear()

        cmd = AxiReadCmd(address, length, arid, burst, size, lock, cache, prot, qos, region, user, event)
        self.read_command_queue.put_nowait(cmd)

        return event

    def idle(self):
        return not self.in_flight_operations

    async def wait(self):
        while not self.idle():
            await self._idle.wait()

    async def read(self, address, length, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        event = self.init_read(address, length, arid, burst, size, lock, cache, prot, qos, region, user)
        await event.wait()
        return event.data

    async def read_words(self, address, count, byteorder='little', ws=2, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        data = await self.read(address, count*ws, arid, burst, size, lock, cache, prot, qos, region, user)
        words = []
        for k in range(count):
            words.append(int.from_bytes(data.data[ws*k:ws*(k+1)], byteorder))
        return words

    async def read_dwords(self, address, count, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_words(address, count, byteorder, 4, arid, burst, size,
            lock, cache, prot, qos, region, user)

    async def read_qwords(self, address, count, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_words(address, count, byteorder, 8, arid, burst, size,
            lock, cache, prot, qos, region, user)

    async def read_byte(self, address, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return (await self.read(address, 1, arid, burst, size, lock, cache, prot, qos, region, user)).data[0]

    async def read_word(self, address, byteorder='little', ws=2, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return (await self.read_words(address, 1, byteorder, ws, arid, burst, size,
            lock, cache, prot, qos, region, user))[0]

    async def read_dword(self, address, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return (await self.read_dwords(address, 1, byteorder, arid, burst, size,
            lock, cache, prot, qos, region, user))[0]

    async def read_qword(self, address, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return (await self.read_qwords(address, 1, byteorder, arid, burst, size,
            lock, cache, prot, qos, region, user))[0]

    def _handle_reset(self, state):
        if state:
            self.log.info("Reset asserted")
            if self._process_read_cr is not None:
                self._process_read_cr.kill()
                self._process_read_cr = None
            if self._process_read_resp_cr is not None:
                self._process_read_resp_cr.kill()
                self._process_read_resp_cr = None
            if self._process_read_resp_id_cr is not None:
                for cr in self._process_read_resp_id_cr:
                    cr.kill()
                self._process_read_resp_id_cr = None

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

            for q in self.int_read_resp_command_queue:
                while not q.empty():
                    cmd = q.get_nowait()
                    flush_cmd(cmd)

            for k in range(len(self.current_read_resp_command)):
                if self.current_read_resp_command[k]:
                    cmd = self.current_read_resp_command[k]
                    self.current_read_resp_command[k] = None
                    flush_cmd(cmd)

            for q in self.int_read_resp_queue_list:
                while not q.empty():
                    q.get_nowait()

            self.cur_id = 0
            self.active_id = Counter()

            self.in_flight_operations = 0
            self._idle.set()
        else:
            self.log.info("Reset de-asserted")
            if self._process_read_cr is None:
                self._process_read_cr = cocotb.fork(self._process_read())
            if self._process_read_resp_cr is None:
                self._process_read_resp_cr = cocotb.fork(self._process_read_resp())
            if self._process_read_resp_id_cr is None:
                self._process_read_resp_id_cr = [cocotb.fork(self._process_read_resp_id(i)) for i in range(self.id_count)]

    async def _process_read(self):
        while True:
            cmd = await self.read_command_queue.get()
            self.current_read_command = cmd

            num_bytes = 2**cmd.size

            aligned_addr = (cmd.address // num_bytes) * num_bytes

            cycles = (cmd.length + num_bytes-1 + (cmd.address % num_bytes)) // num_bytes

            burst_list = []

            cur_addr = aligned_addr
            n = 0

            burst_length = 0

            if cmd.arid is not None:
                arid = cmd.arid
            else:
                arid = self.cur_id
                self.cur_id = (self.cur_id+1) % self.id_count

            self.log.info("Read start addr: 0x%08x arid: 0x%x prot: %s", cmd.address, arid, cmd.prot)

            for k in range(cycles):

                n += 1
                if n >= burst_length:
                    n = 0

                    # split on burst length
                    burst_length = min(cycles-k, min(max(self.max_burst_len, 1), 256))
                    # split on 4k address boundary
                    burst_length = (min(burst_length*num_bytes, 0x1000-(cur_addr & 0xfff))+num_bytes-1)//num_bytes

                    burst_list.append(burst_length)

                    ar = self.r_channel._transaction_obj()
                    ar.arid = arid
                    ar.araddr = cur_addr
                    ar.arlen = burst_length-1
                    ar.arsize = cmd.size
                    ar.arburst = cmd.burst
                    ar.arlock = cmd.lock
                    ar.arcache = cmd.cache
                    ar.arprot = cmd.prot
                    ar.arqos = cmd.qos
                    ar.arregion = cmd.region
                    ar.aruser = cmd.user

                    self.active_id[arid] += 1
                    await self.ar_channel.send(ar)

                    self.log.info("Read burst start arid: 0x%x araddr: 0x%08x arlen: %d arsize: %d arprot: %s",
                        arid, cur_addr, burst_length-1, cmd.size, cmd.prot)

                cur_addr += num_bytes

            resp_cmd = AxiReadRespCmd(cmd.address, cmd.length, cmd.size, cycles, cmd.prot, burst_list, cmd.event)
            await self.int_read_resp_command_queue[arid].put(resp_cmd)

            self.current_read_command = None

    async def _process_read_resp(self):
        while True:
            r = await self.r_channel.recv()

            rid = int(r.rid)

            if self.active_id[rid] <= 0:
                raise Exception(f"Unexpected burst ID {rid}")

            await self.int_read_resp_queue_list[rid].put(r)

    async def _process_read_resp_id(self, rid):
        while True:
            cmd = await self.int_read_resp_command_queue[rid].get()
            self.current_read_resp_command[rid] = cmd

            num_bytes = 2**cmd.size

            aligned_addr = (cmd.address // num_bytes) * num_bytes
            word_addr = (cmd.address // self.byte_width) * self.byte_width

            start_offset = cmd.address % self.byte_width

            cycle_offset = aligned_addr - word_addr
            data = bytearray()

            resp = AxiResp.OKAY
            user = []

            first = True

            for burst_length in cmd.burst_list:
                for k in range(burst_length):
                    r = await self.int_read_resp_queue_list[rid].get()

                    cycle_id = int(r.rid)
                    cycle_data = int(r.rdata)
                    cycle_resp = AxiResp(r.rresp)
                    cycle_last = int(r.rlast)
                    cycle_user = int(r.ruser)

                    if cycle_resp != AxiResp.OKAY:
                        resp = cycle_resp

                    if cycle_user is not None:
                        user.append(cycle_user)

                    start = cycle_offset
                    stop = cycle_offset+num_bytes

                    if first:
                        start = start_offset

                    assert cycle_last == (k == burst_length - 1)

                    for j in range(start, stop):
                        data.append((cycle_data >> j*8) & 0xff)

                    cycle_offset = (cycle_offset + num_bytes) % self.byte_width

                    first = False

                if self.active_id[rid] <= 0:
                    raise Exception(f"Unexpected burst ID {rid}")

                self.active_id[rid] -= 1

                self.log.info("Read burst complete rid: 0x%x rresp: %s", cycle_id, resp)

            data = data[:cmd.length]

            self.log.info("Read complete addr: 0x%08x prot: %s resp: %s data: %s",
                cmd.address, cmd.prot, resp, ' '.join((f'{c:02x}' for c in data)))

            read_resp = AxiReadResp(cmd.address, data, resp, user)

            cmd.event.set(read_resp)

            self.current_read_resp_command[rid] = None

            self.in_flight_operations -= 1

            if self.in_flight_operations == 0:
                self._idle.set()


class AxiMaster:
    def __init__(self, bus, clock, reset=None, reset_active_level=True, max_burst_len=256):
        self.write_if = None
        self.read_if = None

        self.write_if = AxiMasterWrite(bus.write, clock, reset, reset_active_level, max_burst_len)
        self.read_if = AxiMasterRead(bus.read, clock, reset, reset_active_level, max_burst_len)

    def init_read(self, address, length, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, event=None):
        return self.read_if.init_read(address, length, arid, burst, size, lock, cache, prot, qos, region, user, event)

    def init_write(self, address, data, awid=None, burst=AxiBurstType.INCR, size=None, lock=AxiLockType.NORMAL,
            cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0, event=None):
        return self.write_if.init_write(address, data, awid, burst, size, lock, cache, prot, qos, region, user, wuser, event)

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

    async def read(self, address, length, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read(address, length, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_words(self, address, count, byteorder='little', ws=2, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_words(address, count, byteorder, ws, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_dwords(self, address, count, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_dwords(address, count, byteorder, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_qwords(self, address, count, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_qwords(address, count, byteorder, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_byte(self, address, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_byte(address, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_word(self, address, byteorder='little', ws=2, arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_word(address, byteorder, ws, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_dword(self, address, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_dword(address, byteorder, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def read_qword(self, address, byteorder='little', arid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0):
        return await self.read_if.read_qword(address, byteorder, arid,
            burst, size, lock, cache, prot, qos, region, user)

    async def write(self, address, data, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write(address, data, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_words(self, address, data, byteorder='little', ws=2, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_words(address, data, byteorder, ws, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_dwords(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_dwords(address, data, byteorder, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_qwords(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_qwords(address, data, byteorder, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_byte(self, address, data, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_byte(address, data, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_word(self, address, data, byteorder='little', ws=2, awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_word(address, data, byteorder, ws, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_dword(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_dword(address, data, byteorder, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)

    async def write_qword(self, address, data, byteorder='little', awid=None, burst=AxiBurstType.INCR, size=None,
            lock=AxiLockType.NORMAL, cache=0b0011, prot=AxiProt.NONSECURE, qos=0, region=0, user=0, wuser=0):
        return await self.write_if.write_qword(address, data, byteorder, awid,
            burst, size, lock, cache, prot, qos, region, user, wuser)
