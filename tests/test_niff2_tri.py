"""Niff2 Tri Tests."""

import unittest
from parameterized import parameterized

from blend2niff.exporter.niff2_tri import (
    niff2_tri_group_node_builder, niff2_tri_node_builder)


class TestNiff2Tri(unittest.TestCase):

    @parameterized.expand([
        ("one_tri", 1, 2, 3, [4, 5, 6], 132),
        ("two_tris", 1, 2, 3, [4, 5, 6, 7, 8, 9], 208),
    ])
    def test_niff2_tri_group_node_builder(self, _, index, name_index, vtx_group_index, vtx_indices, expected_size):
        tri_group = niff2_tri_group_node_builder(
            index, name_index, vtx_group_index, vtx_indices)
        self.assertEqual(tri_group.tri_group_tag, 0x00080100)
        self.assertEqual(tri_group.this_tri_group_index, index)
        self.assertEqual(tri_group.tri_group_header_size, 32)
        self.assertEqual(tri_group.tri_group_size, expected_size)
        self.assertEqual(tri_group.tri_group_name_index, name_index)
        self.assertEqual(tri_group.tri_anim_type, 0)
        self.assertEqual(tri_group.tri_anim_frame_num, 0)
        self.assertEqual(tri_group.tri_num, len(vtx_indices)//3)
        self.assertEqual(tri_group.vtx_group_index, vtx_group_index)
        self.assertEqual(tri_group.tri_color_group_index, 0)
        self.assertEqual(tri_group.vtx_color_group_index, vtx_group_index+1)
        self.assertEqual(tri_group.tri_nv_group_index, 0)
        self.assertEqual(tri_group.vtx_nv_group_index, 0)
        self.assertEqual(tri_group.st_group_index, 0)
        for index, tri in zip(range(len(tri_group.tris)), tri_group.tris):
            self.assertEqual(index, tri.this_tri_index)

    @parameterized.expand([
        ("default", 1, [2, 3, 4], 76),
    ])
    def test_niff2_tri_node_builder(self, _, index, vtx_indices, expected_size):
        tri = niff2_tri_node_builder(index, vtx_indices)
        self.assertEqual(tri.tri_tag, 0x00080101)
        self.assertEqual(tri.this_tri_index, index)
        self.assertEqual(tri.tri_size, expected_size)
        self.assertEqual(tri.tri_nv_index, 0)
        self.assertEqual(tri.tri_color_index, 0)
        self.assertEqual(tri.vtx_index0, 2)
        self.assertEqual(tri.st_index0, 0)
        self.assertEqual(tri.vtx_nv_index0, 0)
        self.assertEqual(tri.vtx_color_index0, 2)
        self.assertEqual(tri.vtx_index1, 3)
        self.assertEqual(tri.st_index1, 0)
        self.assertEqual(tri.vtx_nv_index1, 0)
        self.assertEqual(tri.vtx_color_index1, 3)
        self.assertEqual(tri.vtx_index2, 4)
        self.assertEqual(tri.st_index2, 0)
        self.assertEqual(tri.vtx_nv_index2, 0)
        self.assertEqual(tri.vtx_color_index2, 4)
        self.assertEqual(tri.nintendo_extension_block_size, 0)
        self.assertEqual(tri.user_extension_block_size, 0)
