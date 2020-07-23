"""Niff2 Tri Tests."""

import unittest
from parameterized import parameterized

from blend2niff.exporter.niff2_tri import (
    niff2_tri_list_header_builder, niff2_tri_list_header_writer,
    niff2_tri_group_builder, niff2_tri_group_writer,
    niff2_tri_node_builder, niff2_tri_node_writer)


class TestNiff2Tri(unittest.TestCase):

    def test_niff2_tri_list_header_builder(self):
        one_tri = niff2_tri_group_builder(1, 2, 3, [4, 5, 6])
        two_tris = niff2_tri_group_builder(1, 2, 3, [4, 5, 6, 7, 8, 9])
        tri_list_header = niff2_tri_list_header_builder([one_tri, two_tris])
        self.assertEqual(tri_list_header.tri_list_tag, 0x00080000)
        self.assertEqual(tri_list_header.tri_list_header_size, 32)
        self.assertEqual(tri_list_header.tri_list_size, 372)
        self.assertEqual(tri_list_header.tri_group_num, 2)
        self.assertEqual(tri_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(tri_list_header.user_extension_block_size, 0)

    def test_niff2_tri_list_header_writer(self):
        one_tri = niff2_tri_group_builder(1, 2, 3, [4, 5, 6])
        two_tris = niff2_tri_group_builder(1, 2, 3, [4, 5, 6, 7, 8, 9])
        tri_groups = [one_tri, two_tris]
        tri_list_header = niff2_tri_list_header_builder(tri_groups)
        buf = niff2_tri_list_header_writer(
            tri_list_header, tri_groups, bytearray())
        byte_list = [0x00, 0x08, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x01, 0x74,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x84,
                     0x00, 0x00, 0x00, 0xD0]
        self.assertEqual(list(buf), byte_list)

    @parameterized.expand([("one_tri", 1, 2, 3, [4, 5, 6], 132),
                           ("two_tris", 1, 2, 3, [4, 5, 6, 7, 8, 9], 208)])
    def test_niff2_tri_group_builder(self, _, index, name_index, vtx_group_index, vtx_indices,
                                     expected_size):
        tri_group = niff2_tri_group_builder(
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
        self.assertEqual(tri_group.vtx_nv_group_index, vtx_group_index+1)
        self.assertEqual(tri_group.st_group_index, 0)
        for tri_index, tri in zip(range(len(tri_group.tris)), tri_group.tris):
            self.assertEqual(tri_index, tri.this_tri_index)

    def test_niff2_tri_group_writer(self):
        tri_group = niff2_tri_group_builder(12, 34, 56, [7, 8, 9])
        buf = niff2_tri_group_writer(tri_group, bytearray())
        byte_list = [0x00, 0x08, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x0C,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0x84,
                     0x00, 0x00, 0x00, 0x22,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x39,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x39,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x08, 0x01, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x4C,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x07,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x07,
                     0x00, 0x00, 0x00, 0x07,
                     0x00, 0x00, 0x00, 0x08,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x08,
                     0x00, 0x00, 0x00, 0x08,
                     0x00, 0x00, 0x00, 0x09,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x09,
                     0x00, 0x00, 0x00, 0x09,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)

    @parameterized.expand([("default", 1, [2, 3, 4], 76)])
    def test_niff2_tri_node_builder(self, _, index, vtx_indices, expected_size):
        tri = niff2_tri_node_builder(index, vtx_indices)
        self.assertEqual(tri.tri_tag, 0x00080101)
        self.assertEqual(tri.this_tri_index, index)
        self.assertEqual(tri.tri_size, expected_size)
        self.assertEqual(tri.tri_nv_index, 0)
        self.assertEqual(tri.tri_color_index, 0)
        self.assertEqual(tri.vtx_index0, 2)
        self.assertEqual(tri.st_index0, 0)
        self.assertEqual(tri.vtx_nv_index0, 2)
        self.assertEqual(tri.vtx_color_index0, 2)
        self.assertEqual(tri.vtx_index1, 3)
        self.assertEqual(tri.st_index1, 0)
        self.assertEqual(tri.vtx_nv_index1, 3)
        self.assertEqual(tri.vtx_color_index1, 3)
        self.assertEqual(tri.vtx_index2, 4)
        self.assertEqual(tri.st_index2, 0)
        self.assertEqual(tri.vtx_nv_index2, 4)
        self.assertEqual(tri.vtx_color_index2, 4)
        self.assertEqual(tri.nintendo_extension_block_size, 0)
        self.assertEqual(tri.user_extension_block_size, 0)

    def test_niff2_tri_node_writer(self):
        tri = niff2_tri_node_builder(123, [4, 5, 6])
        buf = niff2_tri_node_writer(tri, bytearray())
        byte_list = [0x00, 0x08, 0x01, 0x01,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x4C,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x05,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x05,
                     0x00, 0x00, 0x00, 0x05,
                     0x00, 0x00, 0x00, 0x06,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x06,
                     0x00, 0x00, 0x00, 0x06,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
