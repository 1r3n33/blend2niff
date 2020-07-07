"""NIFF2 Shape Tests."""

import unittest
from blend2niff.exporter.niff2_shape import (
    niff2_shape_list_header_builder, niff2_shape_list_header_writer, niff2_shape_node_builder, niff2_shape_node_writer)


class TestNiff2Shape(unittest.TestCase):
    def test_niff2_shape_list_header_builder(self):
        shape_list_header = niff2_shape_list_header_builder([])
        self.assertEqual(shape_list_header.shape_list_tag, 0x00030000)
        self.assertEqual(shape_list_header.shape_list_header_size, 24)
        self.assertEqual(shape_list_header.shape_list_size, 24)
        self.assertEqual(shape_list_header.shape_num, 0)
        self.assertEqual(shape_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(shape_list_header.user_extension_block_size, 0)

    def test_niff2_shape_list_header_writer(self):
        shape_list_header = niff2_shape_list_header_builder([])
        buf = bytearray()
        niff2_shape_list_header_writer(shape_list_header, [], buf)
        self.assertEqual(buf, bytearray(
            b'\x00\x03\x00\x00\x00\x00\x00\x18\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def test_niff2_shape_node_builder(self):
        shape_node = niff2_shape_node_builder(12, 34, 56, 78)
        self.assertEqual(shape_node.shape_tag, 0x00030100)
        self.assertEqual(shape_node.this_shape_index, 12)
        self.assertEqual(shape_node.shape_size, 52)
        self.assertEqual(shape_node.shape_name_index, 34)
        self.assertEqual(shape_node.shape_type, 0x00000014)
        self.assertEqual(shape_node.shape_tri_link, 56)
        self.assertEqual(shape_node.shape_mat_link, 78)
        self.assertEqual(shape_node.shape_part_num, 0)
        self.assertEqual(shape_node.nintendo_extension_block_size, 12)
        self.assertEqual(shape_node.user_extension_block_size, 0)
        self.assertEqual(shape_node.kind_of_node_for_geometry, 0x00080100)
        self.assertEqual(shape_node.external_mat_file_name_index, 0xFFFFFFFF)
        self.assertEqual(shape_node.external_mat_name_index, 0xFFFFFFFF)

    def test_niff2_shape_node_writer(self):
        shape_node = niff2_shape_node_builder(12, 34, 56, 78)
        buf = bytearray()
        niff2_shape_node_writer(shape_node, buf)
        self.assertEqual(buf, bytearray(
            b'\x00\x03\x01\x00\x00\x00\x00\x0C\x00\x00\x00\x34\x00\x00\x00\x22\x00\x00\x00\x14\x00\x00\x00\x38\x00\x00\x00\x4E\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x08\x01\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'))
