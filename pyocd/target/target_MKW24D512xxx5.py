# pyOCD debugger
# Copyright (c) 2018 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .family.target_kinetis import Kinetis
from .family.flash_kinetis import Flash_Kinetis
from ..core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ..debug.svd import SVDFile
import logging

FLASH_ALGO = { 'load_address' : 0x20000000,
               'instructions' : [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0xb510483e, 0x5120f24c, 0xf64d81c1, 0x81c11128, 0xf0218801, 0x80010101, 0x78414839, 0x0160f001,
    0xbf0c2940, 0x21002101, 0x444a4a36, 0xb1397011, 0xf0217841, 0x70410160, 0xf0117841, 0xd1fb0f60,
    0x44484831, 0xf864f000, 0xbf182800, 0xbd102001, 0x4448482c, 0xb1587800, 0x78414829, 0x0160f021,
    0x0140f041, 0x78417041, 0x0160f001, 0xd1fa2940, 0x47702000, 0xb5104824, 0x44484924, 0xf893f000,
    0xbf182800, 0x2100bd10, 0xe8bd481f, 0x44484010, 0xb959f000, 0x4c1cb570, 0x444c4605, 0x4b1b4601,
    0x68e24620, 0xf8b7f000, 0xbf182800, 0x2300bd70, 0x68e24629, 0x4070e8bd, 0x44484813, 0xb94df000,
    0x460cb570, 0x4606460b, 0x480f4601, 0x4615b084, 0xf0004448, 0x2800f8ec, 0xb004bf1c, 0x2000bd70,
    0xe9cd2101, 0x90021000, 0x462b4807, 0x46314622, 0xf0004448, 0xb004f980, 0x0000bd70, 0x40052000,
    0x4007e000, 0x00000004, 0x00000008, 0x6b65666b, 0xbf042800, 0x47702004, 0x6cc949eb, 0x6103f3c1,
    0xbf08290f, 0x2100f44f, 0x4ae8bf1f, 0xf832447a, 0x02891011, 0xe9c02200, 0x21022100, 0x61426081,
    0x61820289, 0x1203e9c0, 0x51a0f04f, 0xf44f6201, 0x62415180, 0x47704610, 0xbf0e2800, 0x61012004,
    0x47702000, 0x48da4602, 0x49d96840, 0x0070f440, 0x47706048, 0x217048d7, 0x21807001, 0x78017001,
    0x0f80f011, 0x7800d0fb, 0x0f20f010, 0x2067bf1c, 0xf0104770, 0xbf1c0f10, 0x47702068, 0x0001f010,
    0x2069bf18, 0x28004770, 0x2004bf04, 0xb5104770, 0x4ac84604, 0x403bf06f, 0x48c76050, 0xbf144281,
    0x2000206b, 0xbf182800, 0x4620bd10, 0xffd2f7ff, 0x46204603, 0xffc6f7ff, 0xbd104618, 0xbf042800,
    0x47702004, 0x60532300, 0x60d36093, 0x61536113, 0x61d36193, 0x68c16011, 0xe9d06051, 0xfbb11001,
    0x6090f0f0, 0x21082004, 0x0103e9c2, 0x1005e9c2, 0x200061d0, 0xe92d4770, 0xb0884df0, 0x46984615,
    0x4682460c, 0xf7ff466a, 0x462affd9, 0x46504621, 0xf0009b04, 0x0007f931, 0xb008bf1c, 0x8df0e8bd,
    0x4600e9dd, 0x1e451960, 0xf0f6fbb5, 0x5010fb06, 0xfbb5b120, 0x1c40f0f6, 0x1e454370, 0xbf9842ac,
    0xb270f8df, 0xf024d81c, 0xf040407f, 0xf8cb6010, 0x48990004, 0xbf144580, 0x2000206b, 0xbf1c2800,
    0xe8bdb008, 0x46508df0, 0xff74f7ff, 0xf8da4607, 0x28000010, 0x4780bf18, 0x4434b917, 0xd9e242ac,
    0xf7ff4650, 0xb008ff5f, 0xe8bd4638, 0x2a008df0, 0x2004bf04, 0xe92d4770, 0xb08945f0, 0x461e4614,
    0x4680460d, 0xf7ff466a, 0x4632ff89, 0x46404629, 0xf0009b03, 0x0007f8e1, 0xb009bf1c, 0x85f0e8bd,
    0x2e009d00, 0xf8dfbf18, 0xd025a1ec, 0x0b04f854, 0x0008f8ca, 0x28049803, 0xf025bf04, 0xf040407f,
    0xd00960c0, 0xd1092808, 0x0b04f854, 0x000cf8ca, 0x407ff025, 0x60e0f040, 0x0004f8ca, 0xf7ff4640,
    0xf8d8ff29, 0x46071010, 0xbf182900, 0xb91f4788, 0x44059803, 0xd1d91a36, 0xf7ff4640, 0xb009ff13,
    0xe8bd4638, 0x280085f0, 0x2004bf04, 0x4a634770, 0x4101ea42, 0x60514a5f, 0xe92de70c, 0xb0884dff,
    0x469a4614, 0x466a460d, 0xf7ff9808, 0x4622ff37, 0x9b054629, 0xf0009808, 0x2800f88f, 0xb00cbf1c,
    0x8df0e8bd, 0x4629466a, 0xf7ff9808, 0x9e00ff27, 0x8008f8dd, 0xf1c84270, 0x40080100, 0x42b74247,
    0x4447bf08, 0xbf182c00, 0xb128f8df, 0x1bbdd01f, 0xbf8842a5, 0x98054625, 0x417ff026, 0xf0f0fbb5,
    0x7180f041, 0x1004f8cb, 0xea400400, 0xf040200a, 0xf8cb00ff, 0x98080008, 0xfeccf7ff, 0xbf1c2800,
    0xe8bdb00c, 0x1b648df0, 0x4447442e, 0xb00cd1df, 0xe8bd2000, 0x2b008df0, 0x2004bf04, 0xe92d4770,
    0xb0884dff, 0xe9dd4616, 0x461d7a14, 0x466a460c, 0x8058f8dd, 0xf7ff9808, 0xe9ddfee1, 0x46323007,
    0xf0004621, 0x2800f839, 0xb00cbf1c, 0x8df0e8bd, 0x2e009c00, 0xb00cbf04, 0x8df0e8bd, 0xb094f8df,
    0x407ff06f, 0x6707ea40, 0x407ff024, 0x7000f040, 0x0004f8cb, 0x7008f8cb, 0xf8cb6828, 0x9808000c,
    0xfe88f7ff, 0xf1bab168, 0xbf180f00, 0x4000f8ca, 0x0f00f1b8, 0x2100bf1c, 0x1000f8c8, 0xe8bdb00c,
    0x99078df0, 0xf0211a76, 0x440d0103, 0x440c9907, 0xb00cd1da, 0x8df0e8bd, 0xbf042800, 0x47702004,
    0x0301f1a3, 0xbf0e4219, 0x2065421a, 0x68034770, 0xd806428b, 0x44116840, 0x42884418, 0x2000bf24,
    0x20664770, 0x00004770, 0x40048000, 0x000003b8, 0x4001f000, 0x40020000, 0x6b65666b, 0x4000ffff,
    0x40020004, 0x40020010, 0x00100008, 0x00200018, 0x00400030, 0x00800060, 0x010000c0, 0x02000180,
    0x04000300, 0x00000600, 0x00000000, 0x00000000,
    ],

    'pc_init' : 0x20000021,
    'pc_unInit': 0x20000071,
    'pc_program_page': 0x200000E1,
    'pc_erase_sector': 0x200000B5,
    'pc_eraseAll' : 0x20000095,

    'static_base' : 0x20000000 + 0x00000020 + 0x00000508,
    'begin_stack' : 0x20000000 + 0x00000800,
    'begin_data' : 0x20000000 + 0x00000A00,
    'page_buffers' : [0x20000a00, 0x20001200],   # Enable double buffering
    'min_program_length' : 4,
    'analyzer_supported' : True,
    'analyzer_address' : 0x1ffff800
  };

class KW24D5(Kinetis):

    memoryMap = MemoryMap(
        FlashRegion(    start=0,           length=0x80000,      blocksize=0x800, is_boot_memory=True,
            algo=FLASH_ALGO, flash_class=Flash_Kinetis),
        RamRegion(      start=0x1fff8000,  length=0x10000)
        )

    def __init__(self, transport):
        super(KW24D5, self).__init__(transport, self.memoryMap)
        self._svd_location = SVDFile(vendor="Freescale", filename="MKW24D5.svd")

