"""NIFF2 Object Tests."""

import unittest
from blend2niff.exporter.niff2_obj import (
    niff2_obj_list_header_builder, niff2_obj_node_builder)


class TestNiff2Obj(unittest.TestCase):
    def test_niff2_obj_list_header_builder(self):
        obj_node = niff2_obj_node_builder(12, 34, 56, 78)
        objs = [obj_node]
        obj_list_header = niff2_obj_list_header_builder(objs)
        self.assertEqual(obj_list_header.obj_list_tag, 0x00020000)
        self.assertEqual(obj_list_header.obj_list_header_size, 28)
        self.assertEqual(obj_list_header.obj_list_size, 144)
        self.assertEqual(obj_list_header.obj_num, len(objs))
        self.assertEqual(obj_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(obj_list_header.user_extension_block_size, 0)

    def test_niff2_obj_node_builder(self):
        obj_node = niff2_obj_node_builder(12, 34, 56, 78)
        self.assertEqual(obj_node.obj_tag, 0x00020100)
        self.assertEqual(obj_node.this_obj_index, 12)
        self.assertEqual(obj_node.obj_size, 116)
        self.assertEqual(obj_node.obj_name_index, 34)
        self.assertEqual(obj_node.obj_state, 1)
        self.assertEqual(obj_node.obj_type, 1)
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
        self.assertEqual(obj_node.obj_shape_link, 56)
        self.assertEqual(obj_node.obj_mat_link, 78)
        self.assertEqual(obj_node.obj_anim_link, 0xFFFFFFFF)
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
