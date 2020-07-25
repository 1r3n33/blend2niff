"""NIFF2 Shape Parts Tests."""

import unittest

from blend2niff.exporter.niff2_part import (
    niff2_part_list_header_builder, niff2_part_list_header_writer,
    niff2_part_node_builder, niff2_part_node_writer)


class TestNiff2Part(unittest.TestCase):
    def test_niff2_part_list_header_builder(self):
        one_tri = niff2_part_node_builder(12, 34, 56, 78, [1])
        two_tris = niff2_part_node_builder(12, 34, 56, 78, [1, 2])
        parts = [one_tri, two_tris]
        part_list_header = niff2_part_list_header_builder(parts)
        self.assertEqual(part_list_header.part_list_tag, 0x00090000)
        self.assertEqual(part_list_header.part_list_header_size, 32)
        self.assertEqual(part_list_header.part_list_size, 116)
        self.assertEqual(part_list_header.part_num, 2)
        self.assertEqual(part_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(part_list_header.user_extension_block_size, 0)

    def test_niff2_part_list_header_writer(self):
        one_tri = niff2_part_node_builder(12, 34, 56, 78, [1])
        two_tris = niff2_part_node_builder(12, 34, 56, 78, [1, 2])
        parts = [one_tri, two_tris]
        part_list_header = niff2_part_list_header_builder(parts)
        buf = niff2_part_list_header_writer(
            part_list_header, parts, bytearray())
        byte_list = [0x00, 0x09, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0x74,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x28,
                     0x00, 0x00, 0x00, 0x2C]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_part_node_builder(self):
        part_node = niff2_part_node_builder(1, 2, 3, 4, [5, 6, 7, 8, 9, 0])
        self.assertEqual(part_node.part_tag, 0x00090100)
        self.assertEqual(part_node.this_part_index, 1)
        self.assertEqual(part_node.part_size, 60)
        self.assertEqual(part_node.part_name_index, 2)
        self.assertEqual(part_node.mat_index, 4)
        self.assertEqual(part_node.tri_group_index, 3)
        self.assertEqual(part_node.part_tri_num, 6)
        self.assertEqual(part_node.nintendo_extension_block_size, 0)
        self.assertEqual(part_node.user_extension_block_size, 0)
        self.assertEqual(part_node.tri_indices, [5, 6, 7, 8, 9, 0])

    def test_niff2_part_node_writer(self):
        part_node = niff2_part_node_builder(1, 2, 3, 4, [5, 6, 7, 8, 9, 0])
        buf = niff2_part_node_writer(part_node, bytearray())
        byte_list = [0x00, 0x09, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x3C,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x03,
                     0x00, 0x00, 0x00, 0x06,
                     0x00, 0x00, 0x00, 0x05,
                     0x00, 0x00, 0x00, 0x06,
                     0x00, 0x00, 0x00, 0x07,
                     0x00, 0x00, 0x00, 0x08,
                     0x00, 0x00, 0x00, 0x09,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
