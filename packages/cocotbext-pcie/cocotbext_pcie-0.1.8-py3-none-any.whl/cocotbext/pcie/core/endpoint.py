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

import mmap

from .function import Function
from .tlp import Tlp, TlpType
from .utils import byte_mask_update


class Endpoint(Function):
    """PCIe endpoint function, implements endpoint config space"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configuration registers
        self.header_type = 0
        self.bar = [0]*6
        self.bar_mask = [0]*6
        self.cardbus_cis = 0
        self.subsystem_vendor_id = 0
        self.subsystem_id = 0

        self.pcie_device_type = 0

    """
    Endpoint (type 0) config space

    31                                                                  0
    +---------------------------------+---------------------------------+
    |            Device ID            |            Vendor ID            |   0   0x00
    +---------------------------------+---------------------------------+
    |             Status              |             Command             |   1   0x04
    +---------------------------------+----------------+----------------+
    |                    Class Code                    |  Revision ID   |   2   0x08
    +----------------+----------------+----------------+----------------+
    |      BIST      |  Header Type   |    Primary     |   Cache Line   |   3   0x0C
    |                |                | Latency Timer  |      Size      |
    +----------------+----------------+----------------+----------------+
    |                      Base Address Register 0                      |   4   0x10
    +-------------------------------------------------------------------+
    |                      Base Address Register 1                      |   5   0x14
    +-------------------------------------------------------------------+
    |                      Base Address Register 2                      |   6   0x18
    +-------------------------------------------------------------------+
    |                      Base Address Register 3                      |   7   0x1C
    +-------------------------------------------------------------------+
    |                      Base Address Register 4                      |   8   0x20
    +-------------------------------------------------------------------+
    |                      Base Address Register 5                      |   9   0x24
    +-------------------------------------------------------------------+
    |                       Cardbus CIS pointer                         |  10   0x28
    +---------------------------------+---------------------------------+
    |          Subsystem ID           |       Subsystem Vendor ID       |  11   0x2C
    +---------------------------------+---------------------------------+
    |                    Expansion ROM Base Address                     |  12   0x30
    +--------------------------------------------------+----------------+
    |                     Reserved                     |    Cap Ptr     |  13   0x34
    +--------------------------------------------------+----------------+
    |                             Reserved                              |  14   0x38
    +----------------+----------------+----------------+----------------+
    |    Max Lat     |    Min Gnt     |    Int Pin     |    Int Line    |  15   0x3C
    +----------------+----------------+----------------+----------------+
    """
    async def read_config_register(self, reg):
        if reg == 4:
            return self.bar[0]
        elif reg == 5:
            return self.bar[1]
        elif reg == 6:
            return self.bar[2]
        elif reg == 7:
            return self.bar[3]
        elif reg == 8:
            return self.bar[4]
        elif reg == 9:
            return self.bar[5]
        elif reg == 10:
            return self.cardbus_cis
        elif reg == 11:
            return (self.subsystem_id << 16) | self.subsystem_vendor_id
        elif reg == 12:
            return (self.expansion_rom_addr & 0xfffff800) | (1 if self.expansion_rom_enable else 0)
        elif reg == 13:
            return self.cap_ptr
        elif reg == 14:
            return 0  # reserved
        elif reg == 15:
            return (self.intr_pin << 8) | self.intr_line
        else:
            return await super().read_config_register(reg)

    async def write_config_register(self, reg, data, mask):
        if reg == 4:
            self.bar[0] = byte_mask_update(self.bar[0], mask, data, self.bar_mask[0])
        elif reg == 5:
            self.bar[1] = byte_mask_update(self.bar[1], mask, data, self.bar_mask[1])
        elif reg == 6:
            self.bar[2] = byte_mask_update(self.bar[2], mask, data, self.bar_mask[2])
        elif reg == 7:
            self.bar[3] = byte_mask_update(self.bar[3], mask, data, self.bar_mask[3])
        elif reg == 8:
            self.bar[4] = byte_mask_update(self.bar[4], mask, data, self.bar_mask[4])
        elif reg == 9:
            self.bar[5] = byte_mask_update(self.bar[5], mask, data, self.bar_mask[5])
        elif reg == 12:
            self.expansion_rom_addr = byte_mask_update(self.expansion_rom_addr,
                mask, data, self.expansion_rom_addr_mask) & 0xfffff800
            if mask & 0x1:
                self.expansion_rom_enable = (data & 1) != 0
        elif reg == 15:
            self.intr_line = byte_mask_update(self.intr_line, mask & 1, data)
            self.intr_pin = byte_mask_update(self.intr_pin, (mask >> 1) & 1, data >> 8)
        else:
            await super().write_config_register(reg, data, mask)


class MemoryEndpoint(Endpoint):
    """PCIe endpoint function, implements BARs pointing to internal memory"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.regions = [None]*6
        self.bar_ptr = 0

        self.register_rx_tlp_handler(TlpType.IO_READ, self.handle_io_read_tlp)
        self.register_rx_tlp_handler(TlpType.IO_WRITE, self.handle_io_write_tlp)
        self.register_rx_tlp_handler(TlpType.MEM_READ, self.handle_mem_read_tlp)
        self.register_rx_tlp_handler(TlpType.MEM_READ_64, self.handle_mem_read_tlp)
        self.register_rx_tlp_handler(TlpType.MEM_WRITE, self.handle_mem_write_tlp)
        self.register_rx_tlp_handler(TlpType.MEM_WRITE_64, self.handle_mem_write_tlp)

    def add_region(self, size, read=None, write=None, ext=False, prefetch=False, io=False):
        if self.bar_ptr > 5 or (ext and self.bar_ptr > 4):
            raise Exception("No more BARs available")

        mem = None
        self.configure_bar(self.bar_ptr, size, ext, prefetch, io)
        if not read and not write:
            mem = mmap.mmap(-1, size)
            self.regions[self.bar_ptr] = mem
        else:
            self.regions[self.bar_ptr] = (read, write)
        if ext:
            self.bar_ptr += 2
        else:
            self.bar_ptr += 1
        return mem

    def add_io_region(self, size, read=None, write=None):
        return self.add_region(size, read, write, False, False, True)

    def add_mem_region(self, size, read=None, write=None):
        return self.add_region(size, read, write)

    def add_prefetchable_mem_region(self, size, read=None, write=None):
        return self.add_region(size, read, write, True, True)

    async def read_region(self, region, addr, length):
        if not self.regions[region]:
            raise Exception("Invalid region")
        if type(self.regions[region]) is tuple:
            return await self.regions[region][0](addr, length)
        else:
            return self.regions[region][addr:addr+length]

    async def write_region(self, region, addr, data):
        if not self.regions[region]:
            raise Exception("Invalid region")
        if type(self.regions[region]) is tuple:
            await self.regions[region][1](addr, data)
        else:
            self.regions[region][addr:addr+len(data)] = data

    async def handle_io_read_tlp(self, tlp):
        m = self.match_bar(tlp.address, True)
        if len(m) == 1:
            self.log.info("IO read, address 0x%08x, BE 0x%x, tag %d",
                tlp.address, tlp.first_be, tlp.tag)

            assert tlp.length == 1

            # prepare completion TLP
            cpl = Tlp.create_completion_data_for_tlp(tlp, self.pcie_id)

            region = m[0][0]
            addr = m[0][1]
            offset = 0
            start_offset = None
            mask = tlp.first_be

            # perform read
            data = bytearray(4)

            for k in range(4):
                if mask & (1 << k):
                    if start_offset is None:
                        start_offset = offset
                else:
                    if start_offset is not None and offset != start_offset:
                        data[start_offset:offset] = await self.read_region(region, addr+start_offset, offset-start_offset)
                    start_offset = None

                offset += 1

            if start_offset is not None and offset != start_offset:
                data[start_offset:offset] = await self.read_region(region, addr+start_offset, offset-start_offset)

            cpl.set_data(data)
            cpl.byte_count = 4
            cpl.length = 1

            self.log.debug("Completion: %s", repr(cpl))
            await self.send(cpl)

        else:
            self.log.warning("IO request did not match any BARs")

            # Unsupported request
            cpl = Tlp.create_ur_completion_for_tlp(tlp, self.pcie_id)
            self.log.debug("UR Completion: %s", repr(cpl))
            await self.send(cpl)

    async def handle_io_write_tlp(self, tlp):
        m = self.match_bar(tlp.address, True)
        if len(m) == 1:
            self.log.info("IO write, address 0x%08x, BE 0x%x, tag %d, data 0x%08x",
                tlp.address, tlp.first_be, tlp.tag, tlp.data[0])

            assert tlp.length == 1

            # prepare completion TLP
            cpl = Tlp.create_completion_for_tlp(tlp, self.pcie_id)

            region = m[0][0]
            addr = m[0][1]
            offset = 0
            start_offset = None
            mask = tlp.first_be

            # perform write
            data = tlp.get_data()

            for k in range(4):
                if mask & (1 << k):
                    if start_offset is None:
                        start_offset = offset
                else:
                    if start_offset is not None and offset != start_offset:
                        await self.write_region(region, addr+start_offset, data[start_offset:offset])
                    start_offset = None

                offset += 1

            if start_offset is not None and offset != start_offset:
                await self.write_region(region, addr+start_offset, data[start_offset:offset])

            cpl.byte_count = 4

            self.log.debug("Completion: %s", repr(cpl))
            await self.send(cpl)

        else:
            self.log.warning("IO request did not match any BARs")

            # Unsupported request
            cpl = Tlp.create_ur_completion_for_tlp(tlp, self.pcie_id)
            self.log.debug("UR Completion: %s", repr(cpl))
            await self.send(cpl)

    async def handle_mem_read_tlp(self, tlp):
        m = self.match_bar(tlp.address)
        if len(m) == 1:
            self.log.info("Memory read, address 0x%08x, length %d, BE 0x%x/0x%x, tag %d",
                tlp.address, tlp.length, tlp.first_be, tlp.last_be, tlp.tag)

            # perform operation
            region = m[0][0]
            addr = m[0][1]

            # check for 4k boundary crossing
            if tlp.length*4 > 0x1000 - (addr & 0xfff):
                print("Request crossed 4k boundary, discarding request")
                return

            # perform read
            data = bytearray(await self.read_region(region, addr, tlp.length*4))

            # prepare completion TLP(s)
            m = 0
            n = 0
            addr = tlp.address+tlp.get_first_be_offset()
            dw_length = tlp.length
            byte_length = tlp.get_be_byte_count()

            while m < dw_length:
                cpl = Tlp.create_completion_data_for_tlp(tlp, self.pcie_id)

                cpl_dw_length = dw_length - m
                cpl_byte_length = byte_length - n
                cpl.byte_count = cpl_byte_length
                if cpl_dw_length > 32 << self.max_payload_size:
                    cpl_dw_length = 32 << self.max_payload_size  # max payload size
                    cpl_dw_length -= (addr & 0x7c) >> 2  # RCB align

                cpl.lower_address = addr & 0x7f

                cpl.set_data(data[m*4:(m+cpl_dw_length)*4])

                self.log.debug("Completion: %s", repr(cpl))
                await self.send(cpl)

                m += cpl_dw_length
                n += cpl_dw_length*4 - (addr & 3)
                addr += cpl_dw_length*4 - (addr & 3)

        else:
            self.log.warning("Memory request did not match any BARs")

            # Unsupported request
            cpl = Tlp.create_ur_completion_for_tlp(tlp, self.pcie_id)
            self.log.debug("UR Completion: %s", repr(cpl))
            await self.send(cpl)

    async def handle_mem_write_tlp(self, tlp):
        m = self.match_bar(tlp.address)
        if len(m) == 1:
            self.log.info("Memory write, address 0x%08x, length %d, BE 0x%x/0x%x",
                tlp.address, tlp.length, tlp.first_be, tlp.last_be)

            # perform operation
            region = m[0][0]
            addr = m[0][1]
            offset = 0
            start_offset = None
            mask = tlp.first_be

            # check for 4k boundary crossing
            if tlp.length*4 > 0x1000 - (addr & 0xfff):
                self.log.warning("Request crossed 4k boundary, discarding request")
                return

            # perform write
            data = tlp.get_data()

            # first dword
            for k in range(4):
                if mask & (1 << k):
                    if start_offset is None:
                        start_offset = offset
                else:
                    if start_offset is not None and offset != start_offset:
                        await self.write_region(region, addr+start_offset, data[start_offset:offset])
                    start_offset = None

                offset += 1

            if tlp.length > 2:
                # middle dwords
                if start_offset is None:
                    start_offset = offset
                offset += (tlp.length-2)*4

            if tlp.length > 1:
                # last dword
                mask = tlp.last_be

                for k in range(4):
                    if mask & (1 << k):
                        if start_offset is None:
                            start_offset = offset
                    else:
                        if start_offset is not None and offset != start_offset:
                            await self.write_region(region, addr+start_offset, data[start_offset:offset])
                        start_offset = None

                    offset += 1

            if start_offset is not None and offset != start_offset:
                await self.write_region(region, addr+start_offset, data[start_offset:offset])

            # memory writes are posted, so don't send a completion

        else:
            self.log.warning("Memory request did not match any BARs")
