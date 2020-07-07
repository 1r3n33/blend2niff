"""NIFF2 Color Tests."""

import unittest
from blend2niff.exporter.niff2_color import (
    niff2_color_list_header_builder, niff2_tri_color_group_node_builder, niff2_vtx_color_group_node_builder)


class TestNiff2Color(unittest.TestCase):
    def test_niff2_color_list_header_builder(self):
        color_floats = [1.0, 2.0, 3.0, 4.0]
        tri_color_group_node = niff2_tri_color_group_node_builder(
            123, color_floats)
        vtx_color_group_node = niff2_vtx_color_group_node_builder(
            123, color_floats)
        color_list_header = niff2_color_list_header_builder(
            [tri_color_group_node], [vtx_color_group_node])
        self.assertEqual(color_list_header.color_list_tag, 0x00050000)
        self.assertEqual(color_list_header.color_list_header_size, 36)
        self.assertEqual(color_list_header.color_list_size, 108)
        self.assertEqual(color_list_header.tri_color_group_num, 1)
        self.assertEqual(color_list_header.vtx_color_group_num, 1)
        self.assertEqual(color_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(color_list_header.user_extension_block_size, 0)

    def test_niff2_tri_color_group_node_builder(self):
        color_floats = [1.0, 2.0, 3.0, 4.0]
        tri_color_group_node = niff2_tri_color_group_node_builder(
            123, color_floats)
        self.assertEqual(tri_color_group_node.tri_color_group_tag, 0x0050100)
        self.assertEqual(tri_color_group_node.this_tri_color_group_index, 123)
        self.assertEqual(tri_color_group_node.tri_color_group_header_size, 20)
        self.assertEqual(tri_color_group_node.tri_color_group_size, 36)
        self.assertEqual(tri_color_group_node.tri_color_num, 1)

    def test_niff2_vtx_color_group_node_builder(self):
        color_floats = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        vtx_color_group_node = niff2_vtx_color_group_node_builder(
            123, color_floats)
        self.assertEqual(vtx_color_group_node.vtx_color_group_tag, 0x0050200)
        self.assertEqual(vtx_color_group_node.this_vtx_color_group_index, 123)
        self.assertEqual(vtx_color_group_node.vtx_color_group_header_size, 20)
        self.assertEqual(vtx_color_group_node.vtx_color_group_size, 52)
        self.assertEqual(vtx_color_group_node.vtx_color_num, 2)
