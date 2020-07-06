"""NIFF2 s,t Texture Coordinates Tests."""

import unittest
from parameterized import parameterized

from blend2niff.exporter.niff2_st import (
    niff2_st_list_header_builder, niff2_st_group_node_builder)


class TestNiff2St(unittest.TestCase):
    def test_niff2_st_list_header_builder(self):
        st_floats = [1.0, 2.0, 3.0, 4.0]
        st_group_node = niff2_st_group_node_builder(123, st_floats)
        st_list_header = niff2_st_list_header_builder([st_group_node])
        self.assertEqual(st_list_header.st_list_tag, 0x00070000)
        self.assertEqual(st_list_header.st_list_header_size, 28)
        self.assertEqual(st_list_header.st_list_size, 64)
        self.assertEqual(st_list_header.st_group_num, 1)
        self.assertEqual(st_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(st_list_header.user_extension_block_size, 0)

    @parameterized.expand([
        ("one-st", 123, [1.0, 2.0], 28),
        ("two-st", 456, [1.0, 2.0, 3.0, 4.0], 36),
    ])
    def test_niff2_st_group_node_builder(self, _, index, st_floats, expected_size):
        st_group_node = niff2_st_group_node_builder(index, st_floats)
        self.assertEqual(st_group_node.st_group_tag, 0x00070100)
        self.assertEqual(st_group_node.this_st_group_index, index)
        self.assertEqual(st_group_node.st_group_header_size, 20)
        self.assertEqual(st_group_node.st_group_size, expected_size)
        self.assertEqual(st_group_node.st_num, len(st_floats)//2)
