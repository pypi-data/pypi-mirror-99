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

import cocotb

from .version import __version__
from .constants import AxiBurstType, AxiProt, AxiResp
from .axi_channels import AxiAWSink, AxiWSink, AxiBSource, AxiARSink, AxiRSource
from .memory import Memory
from .reset import Reset


class AxiRamWrite(Memory, Reset):
    def __init__(self, bus, clock, reset=None, reset_active_level=True, size=1024, mem=None, *args, **kwargs):
        self.log = logging.getLogger(f"cocotb.{bus.aw._entity._name}.{bus.aw._name}")

        self.log.info("AXI RAM model (write)")
        self.log.info("cocotbext-axi version %s", __version__)
        self.log.info("Copyright (c) 2020 Alex Forencich")
        self.log.info("https://github.com/alexforencich/cocotbext-axi")

        super().__init__(size, mem, *args, **kwargs)

        self.aw_channel = AxiAWSink(bus.aw, clock, reset, reset_active_level)
        self.aw_channel.queue_occupancy_limit = 2
        self.w_channel = AxiWSink(bus.w, clock, reset, reset_active_level)
        self.w_channel.queue_occupancy_limit = 2
        self.b_channel = AxiBSource(bus.b, clock, reset, reset_active_level)
        self.b_channel.queue_occupancy_limit = 2

        self.width = len(self.w_channel.bus.wdata)
        self.byte_size = 8
        self.byte_width = self.width // self.byte_size
        self.strb_mask = 2**self.byte_width-1

        self.log.info("AXI RAM model configuration:")
        self.log.info("  Memory size: %d bytes", len(self.mem))
        self.log.info("  Address width: %d bits", len(self.aw_channel.bus.awaddr))
        self.log.info("  ID width: %d bits", len(self.aw_channel.bus.awid))
        self.log.info("  Byte size: %d bits", self.byte_size)
        self.log.info("  Data width: %d bits (%d bytes)", self.width, self.byte_width)

        assert self.byte_width == len(self.w_channel.bus.wstrb)
        assert self.byte_width * self.byte_size == self.width

        assert len(self.b_channel.bus.bid) == len(self.aw_channel.bus.awid)

        self._process_write_cr = None

        self._init_reset(reset, reset_active_level)

    def _handle_reset(self, state):
        if state:
            self.log.info("Reset asserted")
            if self._process_write_cr is not None:
                self._process_write_cr.kill()
                self._process_write_cr = None

            self.aw_channel.clear()
            self.w_channel.clear()
            self.b_channel.clear()
        else:
            self.log.info("Reset de-asserted")
            if self._process_write_cr is None:
                self._process_write_cr = cocotb.fork(self._process_write())

    async def _process_write(self):
        while True:
            aw = await self.aw_channel.recv()

            awid = int(aw.awid)
            addr = int(aw.awaddr)
            length = int(aw.awlen)
            size = int(aw.awsize)
            burst = int(aw.awburst)
            prot = AxiProt(int(aw.awprot))

            self.log.info("Write burst awid: 0x%x awaddr: 0x%08x awlen: %d awsize: %d awprot: %s",
                awid, addr, length, size, prot)

            num_bytes = 2**size
            assert 0 < num_bytes <= self.byte_width

            aligned_addr = (addr // num_bytes) * num_bytes
            length += 1

            transfer_size = num_bytes*length

            if burst == AxiBurstType.WRAP:
                lower_wrap_boundary = (addr // transfer_size) * transfer_size
                upper_wrap_boundary = lower_wrap_boundary + transfer_size

            if burst == AxiBurstType.INCR:
                # check 4k boundary crossing
                assert 0x1000-(aligned_addr & 0xfff) >= transfer_size

            cur_addr = aligned_addr

            for n in range(length):
                cur_word_addr = (cur_addr // self.byte_width) * self.byte_width

                w = await self.w_channel.recv()

                data = int(w.wdata)
                strb = int(w.wstrb)
                last = int(w.wlast)

                # todo latency

                self.mem.seek(cur_word_addr % self.size)

                data = data.to_bytes(self.byte_width, 'little')

                self.log.debug("Write word awid: 0x%x addr: 0x%08x wstrb: 0x%02x data: %s",
                    awid, cur_addr, strb, ' '.join((f'{c:02x}' for c in data)))

                for i in range(self.byte_width):
                    if strb & (1 << i):
                        self.mem.write(data[i:i+1])
                    else:
                        self.mem.seek(1, 1)

                assert last == (n == length-1)

                if burst != AxiBurstType.FIXED:
                    cur_addr += num_bytes

                    if burst == AxiBurstType.WRAP:
                        if cur_addr == upper_wrap_boundary:
                            cur_addr = lower_wrap_boundary

            b = self.b_channel._transaction_obj()
            b.bid = awid
            b.bresp = AxiResp.OKAY

            await self.b_channel.send(b)


class AxiRamRead(Memory, Reset):
    def __init__(self, bus, clock, reset=None, reset_active_level=True, size=1024, mem=None, *args, **kwargs):
        self.log = logging.getLogger(f"cocotb.{bus.ar._entity._name}.{bus.ar._name}")

        self.log.info("AXI RAM model (read)")
        self.log.info("cocotbext-axi version %s", __version__)
        self.log.info("Copyright (c) 2020 Alex Forencich")
        self.log.info("https://github.com/alexforencich/cocotbext-axi")

        super().__init__(size, mem, *args, **kwargs)

        self.ar_channel = AxiARSink(bus.ar, clock, reset, reset_active_level)
        self.ar_channel.queue_occupancy_limit = 2
        self.r_channel = AxiRSource(bus.r, clock, reset, reset_active_level)
        self.r_channel.queue_occupancy_limit = 2

        self.width = len(self.r_channel.bus.rdata)
        self.byte_size = 8
        self.byte_width = self.width // self.byte_size

        self.log.info("AXI RAM model configuration:")
        self.log.info("  Memory size: %d bytes", len(self.mem))
        self.log.info("  Address width: %d bits", len(self.ar_channel.bus.araddr))
        self.log.info("  ID width: %d bits", len(self.ar_channel.bus.arid))
        self.log.info("  Byte size: %d bits", self.byte_size)
        self.log.info("  Data width: %d bits (%d bytes)", self.width, self.byte_width)

        assert self.byte_width * self.byte_size == self.width

        assert len(self.r_channel.bus.rid) == len(self.ar_channel.bus.arid)

        self._process_read_cr = None

        self._init_reset(reset, reset_active_level)

    def _handle_reset(self, state):
        if state:
            self.log.info("Reset asserted")
            if self._process_read_cr is not None:
                self._process_read_cr.kill()
                self._process_read_cr = None

            self.ar_channel.clear()
            self.r_channel.clear()
        else:
            self.log.info("Reset de-asserted")
            if self._process_read_cr is None:
                self._process_read_cr = cocotb.fork(self._process_read())

    async def _process_read(self):
        while True:
            ar = await self.ar_channel.recv()

            arid = int(ar.arid)
            addr = int(ar.araddr)
            length = int(ar.arlen)
            size = int(ar.arsize)
            burst = int(ar.arburst)
            prot = AxiProt(ar.arprot)

            self.log.info("Read burst arid: 0x%x araddr: 0x%08x arlen: %d arsize: %d arprot: %s",
                arid, addr, length, size, prot)

            num_bytes = 2**size
            assert 0 < num_bytes <= self.byte_width

            aligned_addr = (addr // num_bytes) * num_bytes
            length += 1

            transfer_size = num_bytes*length

            if burst == AxiBurstType.WRAP:
                lower_wrap_boundary = (addr // transfer_size) * transfer_size
                upper_wrap_boundary = lower_wrap_boundary + transfer_size

            if burst == AxiBurstType.INCR:
                # check 4k boundary crossing
                assert 0x1000-(aligned_addr & 0xfff) >= transfer_size

            cur_addr = aligned_addr

            for n in range(length):
                cur_word_addr = (cur_addr // self.byte_width) * self.byte_width

                self.mem.seek(cur_word_addr % self.size)

                data = self.mem.read(self.byte_width)

                r = self.r_channel._transaction_obj()
                r.rid = arid
                r.rdata = int.from_bytes(data, 'little')
                r.rlast = n == length-1
                r.rresp = AxiResp.OKAY

                await self.r_channel.send(r)

                self.log.debug("Read word awid: 0x%x addr: 0x%08x data: %s",
                    arid, cur_addr, ' '.join((f'{c:02x}' for c in data)))

                if burst != AxiBurstType.FIXED:
                    cur_addr += num_bytes

                    if burst == AxiBurstType.WRAP:
                        if cur_addr == upper_wrap_boundary:
                            cur_addr = lower_wrap_boundary


class AxiRam(Memory):
    def __init__(self, bus, clock, reset=None, reset_active_level=True, size=1024, mem=None, *args, **kwargs):
        self.write_if = None
        self.read_if = None

        super().__init__(size, mem, *args, **kwargs)

        self.write_if = AxiRamWrite(bus.write, clock, reset, reset_active_level, mem=self.mem)
        self.read_if = AxiRamRead(bus.read, clock, reset, reset_active_level, mem=self.mem)
