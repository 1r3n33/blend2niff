"""NIFF2 Texture Image Data Tests."""

import unittest

from blend2niff.niff2.niff2_tex_img import (
    niff2_tex_img_list_header_builder, niff2_tex_img_list_header_writer,
    niff2_tex_img_node_builder, niff2_tex_img_node_writer)


class TestNiff2TexImg(unittest.TestCase):
    def test_niff2_tex_img_list_header_builder(self):
        tex_img_node = niff2_tex_img_node_builder(
            123, [0x00, 0x01, 0x02, 0x03])
        tex_img_list_header = niff2_tex_img_list_header_builder([tex_img_node])
        self.assertEqual(tex_img_list_header.tex_img_list_tag, 0x00120000)
        self.assertEqual(tex_img_list_header.tex_img_list_header_size, 28)
        self.assertEqual(tex_img_list_header.tex_img_list_size, 60)
        self.assertEqual(tex_img_list_header.tex_img_num, 1)
        self.assertEqual(tex_img_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(tex_img_list_header.user_extension_block_size, 0)

    def test_niff2_tex_img_list_header_writer(self):
        tex_img_node = niff2_tex_img_node_builder(
            123, [0x00, 0x01, 0x02, 0x03])
        tex_img_list_header = niff2_tex_img_list_header_builder([tex_img_node])
        buf = niff2_tex_img_list_header_writer(
            tex_img_list_header, [tex_img_node], bytearray())
        byte_list = [0x00, 0x12, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x1C,
                     0x00, 0x00, 0x00, 0x3C,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_tex_img_node_builder(self):
        tex_img_node = niff2_tex_img_node_builder(
            123, [0x00, 0x01, 0x02, 0x03])
        self.assertEqual(tex_img_node.tex_img_tag, 0x00120100)
        self.assertEqual(tex_img_node.index, 123)
        self.assertEqual(tex_img_node.tex_img_header_size, 24)
        self.assertEqual(tex_img_node.tex_img_size, 32)
        self.assertEqual(tex_img_node.nintendo_extension_block_size, 4)
        self.assertEqual(tex_img_node.user_extension_block_size, 0)
        self.assertEqual(tex_img_node.tex_img_data, [0x00, 0x01, 0x02, 0x03])
        self.assertEqual(tex_img_node.mipmap_max_level, 0)

    def test_niff2_tex_img_node_writer(self):
        tex_img_node = niff2_tex_img_node_builder(
            123, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
        buf = niff2_tex_img_node_writer(tex_img_node, bytearray())
        byte_list = [0x00, 0x12, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x24,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x01, 0x02, 0x03,
                     0x04, 0x05, 0x06, 0x07,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
