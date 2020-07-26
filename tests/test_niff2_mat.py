"""NIFF2 Material Tests."""

import unittest
from blend2niff.niff2.niff2_mat import (
    niff2_mat_list_header_builder, niff2_mat_list_header_writer,
    niff2_mat_node_builder, niff2_mat_node_writer)


class TestNiff2Mat(unittest.TestCase):
    def test_niff2_mat_list_header_builder(self):
        mat_node = niff2_mat_node_builder(123, 456, [1.0, 2.0, 3.0, 4.0])
        mat_list_header = niff2_mat_list_header_builder([mat_node])
        self.assertEqual(mat_list_header.mat_list_tag, 0x000a0000)
        self.assertEqual(mat_list_header.mat_list_header_size, 28)
        self.assertEqual(mat_list_header.mat_list_size, 236)
        self.assertEqual(mat_list_header.mat_num, 1)
        self.assertEqual(mat_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(mat_list_header.user_extension_block_size, 0)

    def test_niff2_mat_list_header_writer(self):
        mat_node = niff2_mat_node_builder(123, 456, [1.0, 2.0, 3.0, 4.0])
        mat_list_header = niff2_mat_list_header_builder([mat_node])
        buf = niff2_mat_list_header_writer(
            mat_list_header, [mat_node], bytearray())
        byte_list = [0x00, 0x0A, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x1C,
                     0x00, 0x00, 0x00, 0xEC,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0xD0]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_mat_node_builder(self):
        mat_node = niff2_mat_node_builder(123, 456, [1.0, 2.0, 3.0, 4.0])
        self.assertEqual(mat_node.mat_tag, 0x000a0100)
        self.assertEqual(mat_node.this_mat_index, 123)
        self.assertEqual(mat_node.mat_size, 208)
        self.assertEqual(mat_node.mat_name_index, 456)
        self.assertEqual(mat_node.mat_type, 0)
        self.assertEqual(mat_node.mat_shade_type, 0x00000011)
        self.assertEqual(mat_node.mat_color_type0, 0x00000004)
        self.assertEqual(mat_node.mat_color_type1, 0xFFFFFFFF)
        self.assertEqual(mat_node.mat_alpha_type0, 0x00040000)
        self.assertEqual(mat_node.mat_alpha_type1, 0xFFFFFFFF)
        self.assertEqual(mat_node.prim_red, 1.0)
        self.assertEqual(mat_node.prim_green, 2.0)
        self.assertEqual(mat_node.prim_blue, 3.0)
        self.assertEqual(mat_node.prim_alpha, 4.0)
        self.assertEqual(mat_node.user_flag0, 0)
        self.assertEqual(mat_node.user_flag1, 0)
        self.assertEqual(mat_node.user_flag2, 0)
        self.assertEqual(mat_node.user_flag3, 0)
        self.assertEqual(mat_node.user_flag4, 0)
        self.assertEqual(mat_node.user_flag5, 0)
        self.assertEqual(mat_node.user_flag6, 0)
        self.assertEqual(mat_node.user_flag7, 0)
        self.assertEqual(mat_node.local_light_index, 0)
        self.assertEqual(mat_node.tex_num, 0)
        self.assertEqual(mat_node.nintendo_extension_block_size, 104)
        self.assertEqual(mat_node.user_extension_block_size, 0)
        self.assertEqual(mat_node.ambient_red, 1.0)
        self.assertEqual(mat_node.ambient_green, 1.0)
        self.assertEqual(mat_node.ambient_blue, 1.0)
        self.assertEqual(mat_node.ambient_alpha, 1.0)
        self.assertEqual(mat_node.emission_red, 0.0)
        self.assertEqual(mat_node.emission_green, 0.0)
        self.assertEqual(mat_node.emission_blue, 0.0)
        self.assertEqual(mat_node.emission_alpha, 0.0)
        self.assertEqual(mat_node.diffuse_red, 1.0)
        self.assertEqual(mat_node.diffuse_green, 1.0)
        self.assertEqual(mat_node.diffuse_blue, 1.0)
        self.assertEqual(mat_node.diffuse_alpha, 1.0)
        self.assertEqual(mat_node.mat_type_for_fog, 0)
        self.assertEqual(mat_node.mat_color_type0_for_fog, 0x00000004)
        self.assertEqual(mat_node.mat_color_type1_for_fog, 0xFFFFFFFF)
        self.assertEqual(mat_node.mat_alpha_type0_for_fog, 0x00040000)
        self.assertEqual(mat_node.mat_alpha_type1_for_fog, 0xFFFFFFFF)
        self.assertEqual(mat_node.prim_red_for_fog, 0.9)
        self.assertEqual(mat_node.prim_green_for_fog, 0.9)
        self.assertEqual(mat_node.prim_blue_for_fog, 0.9)
        self.assertEqual(mat_node.prim_alpha_for_fog, 1.0)
        self.assertEqual(
            mat_node.external_local_light_file_name_index, 0xFFFFFFFF)
        self.assertEqual(mat_node.external_local_light_name_index, 0xFFFFFFFF)
        self.assertEqual(mat_node.external_tex_num, 0)
        self.assertEqual(mat_node.prim_color_anim_num, 0)
        self.assertEqual(mat_node.prim_color_anim_num_for_fog, 0)

    def test_niff2_mat_node_writer(self):
        mat_node = niff2_mat_node_builder(123, 456, [1.0, 2.0, 3.0, 4.0])
        buf = niff2_mat_node_writer(mat_node, bytearray())
        byte_list = [0x00, 0x0A, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0xD0,
                     0x00, 0x00, 0x01, 0xC8,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x11,
                     0x00, 0x00, 0x00, 0x04,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x04, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00,
                     0x40, 0x80, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x68,
                     0x00, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x04,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x04, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x3F, 0x66, 0x66, 0x66,
                     0x3F, 0x66, 0x66, 0x66,
                     0x3F, 0x66, 0x66, 0x66,
                     0x3F, 0x80, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
