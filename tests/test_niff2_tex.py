"""NIFF2 Texture Configuration Tests."""

import unittest

from blend2niff.niff2.niff2_tex import (
    niff2_tex_list_header_builder, niff2_tex_list_header_writer,
    niff2_tex_node_builder, niff2_tex_node_writer)


class TestNiff2Tex(unittest.TestCase):
    def test_niff2_tex_list_header_builder(self):
        tex_node = niff2_tex_node_builder(12, 34, 56, 78, 90)
        tex_nodes = [tex_node]*4
        tex_list_header = niff2_tex_list_header_builder(tex_nodes)
        self.assertEqual(tex_list_header.tex_list_tag, 0x000B0000)
        self.assertEqual(tex_list_header.tex_list_header_size, 40)
        self.assertEqual(tex_list_header.tex_list_size, 440)
        self.assertEqual(tex_list_header.tex_num, 4)
        self.assertEqual(tex_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(tex_list_header.user_extension_block_size, 0)

    def test_niff2_tex_list_header_writer(self):
        tex_node = niff2_tex_node_builder(12, 34, 56, 78, 90)
        tex_nodes = [tex_node]*4
        tex_list_header = niff2_tex_list_header_builder(tex_nodes)
        buf = niff2_tex_list_header_writer(
            tex_list_header, tex_nodes, bytearray())
        byte_list = [0x00, 0x0B, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x28,
                     0x00, 0x00, 0x01, 0xB8,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x64]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_tex_node_builder(self):
        tex_node = niff2_tex_node_builder(12, 34, 56, 78, 90)
        self.assertEqual(tex_node.tex_tag, 0x000B0100)
        self.assertEqual(tex_node.this_tex_index, 12)
        self.assertEqual(tex_node.tex_header_size, 52)
        self.assertEqual(tex_node.tex_size, 100)
        self.assertEqual(tex_node.tex_name_index, 34)
        self.assertEqual(tex_node.tex_type, 0x00000405)
        self.assertEqual(tex_node.tex_wrap_s, 0)
        self.assertEqual(tex_node.tex_wrap_t, 0)
        self.assertEqual(tex_node.tex_anim, 0)
        self.assertEqual(tex_node.tex_data_area_size, 28)
        self.assertEqual(tex_node.tex_anim_frame_rate, 0)
        self.assertEqual(tex_node.nintendo_extension_block_size, 20)
        self.assertEqual(tex_node.user_extension_block_size, 0)
        self.assertEqual(tex_node.tex_img_width, 78)
        self.assertEqual(tex_node.tex_img_height, 90)
        self.assertEqual(tex_node.tex_tile_width, 78)
        self.assertEqual(tex_node.tex_tile_height, 90)
        self.assertEqual(tex_node.tex_offset_x, 0)
        self.assertEqual(tex_node.tex_offset_y, 0)
        self.assertEqual(tex_node.tex_img_index, 56)
        self.assertEqual(tex_node.tex_filter, 1)
        self.assertEqual(tex_node.use_perspective_correction, 1)
        self.assertEqual(tex_node.mipmap_level, 0)
        self.assertEqual(tex_node.use_color_palette, 0)
        self.assertEqual(tex_node.external_tex_img_num, 0)

    def test_niff2_tex_node_writer(self):
        tex_node = niff2_tex_node_builder(12, 34, 56, 78, 90)
        buf = niff2_tex_node_writer(tex_node, bytearray())
        byte_list = [0x00, 0x0B, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x0C,
                     0x00, 0x00, 0x00, 0x34,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x22,
                     0x00, 0x00, 0x04, 0x05,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x1C,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x14,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x4E,
                     0x00, 0x00, 0x00, 0x5A,
                     0x00, 0x00, 0x00, 0x4E,
                     0x00, 0x00, 0x00, 0x5A,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
