"""NIFF2 Anim Tests."""

import unittest
from blend2niff.exporter.niff2_anim import (
    niff2_anim_list_header_builder, niff2_anim_list_header_writer)


class TestNiff2Anim(unittest.TestCase):
    def test_niff2_anim_list_header_builder(self):
        anim_list_header = niff2_anim_list_header_builder()
        self.assertEqual(anim_list_header.anim_list_tag, 0x00c0000)
        self.assertEqual(anim_list_header.anim_list_header_size, 24)
        self.assertEqual(anim_list_header.anim_list_size, 24)
        self.assertEqual(anim_list_header.anim_group_num, 0)
        self.assertEqual(anim_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(anim_list_header.user_extension_block_size, 0)

    def test_niff2_anim_list_header_writer(self):
        anim_list_header = niff2_anim_list_header_builder()
        buf = bytearray()
        niff2_anim_list_header_writer(anim_list_header, buf)
        self.assertEqual(buf, bytearray(
            b'\x00\x0c\x00\x00\x00\x00\x00\x18\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
