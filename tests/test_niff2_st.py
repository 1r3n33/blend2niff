"""NIFF2 s,t Texture Coordinates Tests."""

import unittest
from parameterized import parameterized

from blend2niff.niff2.niff2_st import (
    niff2_st_list_header_builder, niff2_st_list_header_writer,
    niff2_st_group_builder, niff2_st_group_writer)


class TestNiff2St(unittest.TestCase):
    def test_niff2_st_list_header_builder(self):
        st_floats = [1.0, 2.0, 3.0, 4.0]
        st_group = niff2_st_group_builder(123, st_floats)
        st_list_header = niff2_st_list_header_builder([st_group])
        self.assertEqual(st_list_header.st_list_tag, 0x00070000)
        self.assertEqual(st_list_header.st_list_header_size, 28)
        self.assertEqual(st_list_header.st_list_size, 64)
        self.assertEqual(st_list_header.st_group_num, 1)
        self.assertEqual(st_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(st_list_header.user_extension_block_size, 0)

    def test_niff2_st_list_header_writer(self):
        st_floats = [1.0, 2.0, 3.0, 4.0]
        st_group = niff2_st_group_builder(123, st_floats)
        st_list_header = niff2_st_list_header_builder([st_group])
        buf = niff2_st_list_header_writer(
            st_list_header, [st_group], bytearray())
        byte_list = [0x00, 0x07, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x1C,
                     0x00, 0x00, 0x00, 0x40,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x24]
        self.assertEqual(list(buf), byte_list)

    @parameterized.expand([
        ("one-st", 123, [1.0, 2.0], 28),
        ("two-st", 456, [1.0, 2.0, 3.0, 4.0], 36),
    ])
    def test_niff2_st_group_builder(self, _, index, st_floats, expected_size):
        st_group = niff2_st_group_builder(index, st_floats)
        self.assertEqual(st_group.st_group_tag, 0x00070100)
        self.assertEqual(st_group.this_st_group_index, index)
        self.assertEqual(st_group.st_group_header_size, 20)
        self.assertEqual(st_group.st_group_size, expected_size)
        self.assertEqual(st_group.st_num, len(st_floats)//2)

    def test_niff2_st_group_writer(self):
        st_floats = [1.0, 2.0, 3.0, 4.0]
        st_group = niff2_st_group_builder(123, st_floats)
        buf = niff2_st_group_writer(st_group, bytearray())
        byte_list = [0x00, 0x07, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x14,
                     0x00, 0x00, 0x00, 0x24,
                     0x00, 0x00, 0x00, 0x02,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00,
                     0x40, 0x80, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
