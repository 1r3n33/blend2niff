"""Niff2 Tri Tests"""

import unittest
from parameterized import parameterized

from blend2niff.exporter.niff2_tri import niff2_tri_group_node_builder


class TestNiff2Tri(unittest.TestCase):

    @parameterized.expand([
        ("default", 1, 2, 3, 56),
    ])
    def test_niff2_tri_group_builder(self, _, index, name_index, vtx_group_index, expected_size):
        tri_group = niff2_tri_group_node_builder(
            index, name_index, vtx_group_index)
        self.assertEqual(tri_group.tri_group_tag, 0x00080100)
        self.assertEqual(tri_group.this_tri_group_index, index)
        self.assertEqual(tri_group.tri_group_header_size, 32)
        self.assertEqual(tri_group.tri_group_size, expected_size)
        self.assertEqual(tri_group.tri_group_name_index, name_index)
        self.assertEqual(tri_group.tri_anim_type, 0)
        self.assertEqual(tri_group.tri_anim_frame_num, 0)
        self.assertEqual(tri_group.tri_num, 0)
        self.assertEqual(tri_group.vtx_group_index, vtx_group_index)
        self.assertEqual(tri_group.tri_color_group_index, 0xFFFFFFFF)
        self.assertEqual(tri_group.vtx_color_group_index, 0xFFFFFFFF)
        self.assertEqual(tri_group.tri_nv_group_index, 0xFFFFFFFF)
        self.assertEqual(tri_group.vtx_nv_group_index, 0xFFFFFFFF)
        self.assertEqual(tri_group.st_group_index, 0xFFFFFFFF)


if __name__ == '__main__':
    unittest.main()
