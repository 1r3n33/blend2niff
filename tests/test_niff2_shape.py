"""NIFF2 Shape Tests."""

import unittest
from blend2niff.niff2.niff2_shape import (
    niff2_shape_list_header_builder, niff2_shape_list_header_writer,
    niff2_shape_node_builder, niff2_shape_node_writer)
from blend2niff.niff2.niff2_part import niff2_part_node_builder


class TestNiff2Shape(unittest.TestCase):
    def test_niff2_shape_list_header_builder(self):
        part0 = niff2_part_node_builder(1, 2, 3, 4, [5])
        part1 = niff2_part_node_builder(6, 7, 8, 9, [0, 1])
        part2 = niff2_part_node_builder(2, 3, 4, 5, [6, 7, 8])
        one_part = niff2_shape_node_builder(12, 34, 56, 78, [part0])
        two_parts = niff2_shape_node_builder(78, 56, 43, 21, [part1, part2])
        shape_list_header = niff2_shape_list_header_builder(
            [one_part, two_parts])
        self.assertEqual(shape_list_header.shape_list_tag, 0x00030000)
        self.assertEqual(shape_list_header.shape_list_header_size, 32)
        self.assertEqual(shape_list_header.shape_list_size, 148)
        self.assertEqual(shape_list_header.shape_num, 2)
        self.assertEqual(shape_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(shape_list_header.user_extension_block_size, 0)

    def test_niff2_shape_list_header_writer(self):
        part0 = niff2_part_node_builder(1, 2, 3, 4, [5])
        part1 = niff2_part_node_builder(6, 7, 8, 9, [0, 1])
        part2 = niff2_part_node_builder(2, 3, 4, 5, [6, 7, 8])
        one_part = niff2_shape_node_builder(12, 34, 56, 78, [part0])
        two_parts = niff2_shape_node_builder(78, 56, 43, 21, [part1, part2])
        shape_list_header = niff2_shape_list_header_builder(
            [one_part, two_parts])
        buf = niff2_shape_list_header_writer(
            shape_list_header, [one_part, two_parts], bytearray())
        byte_list = [0x00, 0x03, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0x94,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x3C]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_shape_node_builder(self):
        part0 = niff2_part_node_builder(1, 2, 3, 4, [5, 6])
        part1 = niff2_part_node_builder(7, 8, 9, 0, [1, 2, 3])
        shape_node = niff2_shape_node_builder(12, 34, 56, 78, [part0, part1])
        self.assertEqual(shape_node.shape_tag, 0x00030100)
        self.assertEqual(shape_node.this_shape_index, 12)
        self.assertEqual(shape_node.shape_size, 60)
        self.assertEqual(shape_node.shape_name_index, 34)
        self.assertEqual(shape_node.shape_type, 0x00000014)
        self.assertEqual(shape_node.shape_tri_link, 56)
        self.assertEqual(shape_node.shape_mat_link, 78)
        self.assertEqual(shape_node.shape_part_num, 2)
        self.assertEqual(shape_node.nintendo_extension_block_size, 12)
        self.assertEqual(shape_node.user_extension_block_size, 0)
        self.assertEqual(shape_node.kind_of_node_for_geometry, 0x00080100)
        self.assertEqual(shape_node.external_mat_file_name_index, 0xFFFFFFFF)
        self.assertEqual(shape_node.external_mat_name_index, 0xFFFFFFFF)
        self.assertEqual(shape_node.parts, [part0, part1])

    def test_niff2_shape_node_writer(self):
        part0 = niff2_part_node_builder(1, 2, 3, 4, [5, 6])
        part1 = niff2_part_node_builder(7, 8, 9, 0, [1, 2, 3])
        shape_node = niff2_shape_node_builder(12, 34, 56, 78, [part0, part1])
        buf = niff2_shape_node_writer(shape_node, bytearray())
        byte_list = [0x00, 0x03, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x0C,
                     0x00, 0x00, 0x00, 0x3C,
                     0x00, 0x00, 0x00, 0x22,
                     0x00, 0x00, 0x00, 0x14,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x4E,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x0C,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x07,
                     0x00, 0x08, 0x01, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF]
        self.assertEqual(list(buf), byte_list)
