"""NIFF2 Vector Tests."""

import unittest
from blend2niff.exporter.niff2_vector import (
    niff2_vector_list_header_builder, niff2_tri_nv_group_node_builder, niff2_vtx_nv_group_node_builder)


class TestNiff2Vector(unittest.TestCase):
    def test_niff2_vector_list_header_builder(self):
        nv_floats = [1.0, 2.0, 3.0]
        tri_nv_group_node = niff2_tri_nv_group_node_builder(
            123, nv_floats)
        vtx_nv_group_node = niff2_vtx_nv_group_node_builder(
            123, nv_floats)
        vector_list_header = niff2_vector_list_header_builder(
            [tri_nv_group_node], [vtx_nv_group_node])
        self.assertEqual(vector_list_header.vector_list_tag, 0x00060000)
        self.assertEqual(vector_list_header.vector_list_header_size, 36)
        self.assertEqual(vector_list_header.vector_list_size, 100)
        self.assertEqual(vector_list_header.tri_nv_group_num, 1)
        self.assertEqual(vector_list_header.vtx_nv_group_num, 1)
        self.assertEqual(vector_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(vector_list_header.user_extension_block_size, 0)

    def test_niff2_tri_nv_group_node_builder(self):
        nv_floats = [1.0, 2.0, 3.0]
        tri_nv_group_node = niff2_tri_nv_group_node_builder(
            123, nv_floats)
        self.assertEqual(tri_nv_group_node.tri_nv_group_tag, 0x0060100)
        self.assertEqual(tri_nv_group_node.this_tri_nv_group_index, 123)
        self.assertEqual(tri_nv_group_node.tri_nv_group_header_size, 20)
        self.assertEqual(tri_nv_group_node.tri_nv_group_size, 32)
        self.assertEqual(tri_nv_group_node.tri_nv_num, 1)

    def test_niff2_vtx_nv_group_node_builder(self):
        nv_floats = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        vtx_nv_group_node = niff2_vtx_nv_group_node_builder(
            123, nv_floats)
        self.assertEqual(vtx_nv_group_node.vtx_nv_group_tag, 0x0060200)
        self.assertEqual(vtx_nv_group_node.this_vtx_nv_group_index, 123)
        self.assertEqual(vtx_nv_group_node.vtx_nv_group_header_size, 20)
        self.assertEqual(vtx_nv_group_node.vtx_nv_group_size, 44)
        self.assertEqual(vtx_nv_group_node.vtx_nv_num, 2)
