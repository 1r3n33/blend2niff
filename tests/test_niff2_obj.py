"""NIFF2 Object Tests."""

import unittest
from parameterized import parameterized

from blend2niff.exporter.niff2_obj import (
    niff2_obj_list_header_builder, niff2_obj_list_header_writer,
    niff2_obj_node_builder, niff2_obj_node_writer)


class TestNiff2Obj(unittest.TestCase):
    def test_niff2_obj_list_header_builder(self):
        obj_node = niff2_obj_node_builder(12, 34, 56, 78, 90)
        objs = [obj_node]
        obj_list_header = niff2_obj_list_header_builder(objs)
        self.assertEqual(obj_list_header.obj_list_tag, 0x00020000)
        self.assertEqual(obj_list_header.obj_list_header_size, 28)
        self.assertEqual(obj_list_header.obj_list_size, 144)
        self.assertEqual(obj_list_header.obj_num, len(objs))
        self.assertEqual(obj_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(obj_list_header.user_extension_block_size, 0)

    def test_niff2_obj_list_header_writer(self):
        obj_node = niff2_obj_node_builder(12, 34, 56, 78, 90)
        objs = [obj_node]
        obj_list_header = niff2_obj_list_header_builder(objs)
        buf = bytearray()
        niff2_obj_list_header_writer(obj_list_header, objs, buf)
        byte_list = [0x00, 0x02, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x1C,
                     0x00, 0x00, 0x00, 0x90,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x74]
        self.assertEqual(list(buf), byte_list)

    @parameterized.expand([
        ("3d", 56, 0x00000001),
        ("null", 0xFFFFFFFF, 0x00000000),
    ])
    def test_niff2_obj_node_builder(self, _, shape_index, expected_type):
        obj_node = niff2_obj_node_builder(12, 34, shape_index, 78, 90)
        self.assertEqual(obj_node.obj_tag, 0x00020100)
        self.assertEqual(obj_node.this_obj_index, 12)
        self.assertEqual(obj_node.obj_size, 116)
        self.assertEqual(obj_node.obj_name_index, 34)
        self.assertEqual(obj_node.obj_state, 1)
        self.assertEqual(obj_node.obj_type, expected_type)
        self.assertEqual(obj_node.obj_group, 0)
        self.assertEqual(obj_node.obj_pri, 0)
        self.assertEqual(obj_node.obj_render_cycle_type, 0)
        self.assertEqual(obj_node.obj_render_pri, 0x00d00000)
        self.assertEqual(obj_node.obj_render_type0, 0)
        self.assertEqual(obj_node.obj_render_type1, 0)
        self.assertEqual(obj_node.have_link_billboard, 0)
        self.assertEqual(obj_node.obj_lod_num, 0)
        self.assertEqual(obj_node.obj_child_num, 0)
        self.assertEqual(obj_node.obj_parent_link, 0xFFFFFFFF)
        self.assertEqual(obj_node.obj_shape_link, shape_index)
        self.assertEqual(obj_node.obj_mat_link, 78)
        self.assertEqual(obj_node.obj_anim_link, 90)
        self.assertEqual(obj_node.obj_coll_link, 0xFFFFFFFF)
        self.assertEqual(obj_node.nintendo_extension_block_size, 28)
        self.assertEqual(obj_node.user_extension_block_size, 0)
        self.assertEqual(obj_node.obj_render_cycle_type_for_fog, 1)
        self.assertEqual(obj_node.obj_render_pri_for_fog, 0x00d00000)
        self.assertEqual(obj_node.obj_render_type0_for_fog, 0)
        self.assertEqual(obj_node.obj_render_type1_for_fog, 0)
        self.assertEqual(obj_node.obj_chain_root_link_num, 0)
        self.assertEqual(obj_node.external_obj_lod_num, 0)
        self.assertEqual(obj_node.external_obj_num, 0)

    def test_niff2_obj_node_writer(self):
        obj_node = niff2_obj_node_builder(12, 34, 56, 78, 90)
        buf = bytearray()
        niff2_obj_node_writer(obj_node, buf)
        byte_list = [0x00, 0x02, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x0C,
                     0x00, 0x00, 0x00, 0x74,
                     0x00, 0x00, 0x00, 0x22,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0xD0, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x4E,
                     0x00, 0x00, 0x00, 0x5A,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x1C,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0xD0, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
