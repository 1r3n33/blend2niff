"""NIFF2 Anim Tests."""

import unittest
from blend2niff.niff2.niff2_anim import (
    niff2_anim_list_header_builder, niff2_anim_list_header_writer,
    niff2_anim_group_builder, niff2_anim_group_writer,
    niff2_anim_node_builder, niff2_anim_node_writer)


class TestNiff2Anim(unittest.TestCase):
    def test_niff2_anim_list_header_builder(self):
        anim_node = niff2_anim_node_builder(
            [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        anim_group = niff2_anim_group_builder(123, 456, anim_node)
        anim_list_header = niff2_anim_list_header_builder([anim_group])
        self.assertEqual(anim_list_header.anim_list_tag, 0x00c0000)
        self.assertEqual(anim_list_header.anim_list_header_size, 28)
        self.assertEqual(anim_list_header.anim_list_size, 276)
        self.assertEqual(anim_list_header.anim_group_num, 1)
        self.assertEqual(anim_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(anim_list_header.user_extension_block_size, 0)

    def test_niff2_anim_list_header_writer(self):
        anim_node = niff2_anim_node_builder(
            [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        anim_group = niff2_anim_group_builder(123, 456, anim_node)
        anim_list_header = niff2_anim_list_header_builder([anim_group])
        buf = bytearray()
        niff2_anim_list_header_writer(anim_list_header, [anim_group], buf)
        byte_list = [0x00, 0x0C, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x1c,
                     0x00, 0x00, 0x01, 0x14,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0xF8]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_anim_group_builder(self):
        anim_node = niff2_anim_node_builder(
            [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        anim_group = niff2_anim_group_builder(123, 456, anim_node)
        self.assertEqual(anim_group.anim_group_tag, 0x000c0100)
        self.assertEqual(anim_group.this_anim_group_index, 123)
        self.assertEqual(anim_group.anim_group_header_size, 196)
        self.assertEqual(anim_group.anim_group_size, 248)
        self.assertEqual(anim_group.anim_name_index, 456)
        self.assertEqual(anim_group.anim_type, 0)
        self.assertEqual(anim_group.frame_rate, 0)
        self.assertEqual(anim_group.anim_num, 1)
        self.assertEqual(anim_group.anim_loop, 0)
        self.assertEqual(anim_group.anim_rot_mtx_order, 0x00010203)
        self.assertEqual(anim_group.nintendo_extension_block_size, 148)
        self.assertEqual(anim_group.user_extension_block_size, 0)
        self.assertEqual(anim_group.use_animation_channel, 0)
        self.assertEqual(anim_group.rotate_axis_num, 0)
        self.assertEqual(anim_group.rotate_x_num, 0)
        self.assertEqual(anim_group.rotate_y_num, 0)
        self.assertEqual(anim_group.rotate_z_num, 0)
        self.assertEqual(anim_group.orientation_xy_num, 0)
        self.assertEqual(anim_group.translation_num, 0)
        self.assertEqual(anim_group.unique_scale_num, 0)
        self.assertEqual(anim_group.classical_scale_num, 0)
        self.assertEqual(
            anim_group.kind_of_orientation_constraint_node, 0xFFFFFFFF)
        self.assertEqual(anim_group.orientation_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.kind_of_direction_constraint_node, 0xFFFFFFFF)
        self.assertEqual(anim_group.direction_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.kind_of_up_vector_constraint_node, 0xFFFFFFFF)
        self.assertEqual(anim_group.up_vector_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.kind_of_preferred_axis_constraint_node, 0xFFFFFFFF)
        self.assertEqual(anim_group.preferred_axis_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.kind_of_position_constrint_node, 0xFFFFFFFF)
        self.assertEqual(anim_group.position_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.kind_of_unique_scale_constraint_node, 0xFFFFFFFF)
        self.assertEqual(anim_group.unique_scale_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.kind_of_classical_scale_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.classical_scale_constraint_node, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_orientation_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_orientation_constraint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_direction_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_direction_consrtaint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_upvector_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_upvector_constraint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_perferred_axis_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_preferred_axis_constraint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_position_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_position_constraint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_unique_scale_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_unique_scale_constraint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_classical_scale_constraint_file_name_index, 0xFFFFFFFF)
        self.assertEqual(
            anim_group.external_classical_scale_constraint_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(anim_group.anim_node, anim_node)

    def test_niff2_anim_group_writer(self):
        anim_node = niff2_anim_node_builder(
            [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        anim_group = niff2_anim_group_builder(123, 456, anim_node)
        buf = bytearray()
        niff2_anim_group_writer(anim_group, buf)
        byte_list = [0x00, 0x0C, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0xC4,
                     0x00, 0x00, 0x00, 0xF8,
                     0x00, 0x00, 0x01, 0xC8,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x01, 0x02, 0x03,
                     0x00, 0x00, 0x00, 0x94,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x0C, 0x01, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x34,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00,
                     0x40, 0x80, 0x00, 0x00,
                     0x40, 0xA0, 0x00, 0x00,
                     0x40, 0xC0, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x40, 0xE0, 0x00, 0x00,
                     0x41, 0x00, 0x00, 0x00,
                     0x41, 0x10, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_anim_node_builder(self):
        anim_node = niff2_anim_node_builder(
            [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        self.assertEqual(anim_node.anim_tag, 0x000c0101)
        self.assertEqual(anim_node.this_anim_index, 0)
        self.assertEqual(anim_node.anim_size, 52)
        self.assertEqual(anim_node.translate_x, 1.0)
        self.assertEqual(anim_node.translate_y, 2.0)
        self.assertEqual(anim_node.translate_z, 3.0)
        self.assertEqual(anim_node.rotate_axis_x, 4.0)
        self.assertEqual(anim_node.rotate_axis_y, 5.0)
        self.assertEqual(anim_node.rotate_axis_z, 6.0)
        self.assertEqual(anim_node.rotate_expand_flag, 0)
        self.assertEqual(anim_node.scale_x, 7.0)
        self.assertEqual(anim_node.scale_y, 8.0)
        self.assertEqual(anim_node.scale_z, 9.0)

    def test_niff2_anim_node_writer(self):
        anim_node = niff2_anim_node_builder(
            [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
        buf = bytearray()
        niff2_anim_node_writer(anim_node, buf)
        byte_list = [0x00, 0x0C, 0x01, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x34,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00,
                     0x40, 0x80, 0x00, 0x00,
                     0x40, 0xA0, 0x00, 0x00,
                     0x40, 0xC0, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x40, 0xE0, 0x00, 0x00,
                     0x41, 0x00, 0x00, 0x00,
                     0x41, 0x10, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
