"""NIFF2 Light Tests."""

import unittest

from blend2niff.exporter.niff2_light import (
    niff2_light_list_header_builder, niff2_light_list_header_writer)


class TestLight(unittest.TestCase):
    def test_niff2_light_list_header_builder(self):
        light_list_header = niff2_light_list_header_builder()
        self.assertEqual(light_list_header.light_list_tag, 0x000F0000)
        self.assertEqual(light_list_header.light_list_header_size, 24)
        self.assertEqual(light_list_header.light_list_size, 24)
        self.assertEqual(light_list_header.light_num, 0)
        self.assertEqual(light_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(light_list_header.user_extension_block_size, 0)

    def test_niff2_light_list_header_writer(self):
        light_list_header = niff2_light_list_header_builder()
        buf = niff2_light_list_header_writer(light_list_header, bytearray())
        byte_list = [0x00, 0x0f, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
