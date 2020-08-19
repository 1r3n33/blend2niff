"""NIFF2 Texture Image Data Tests."""

import unittest

from blend2niff.niff2.niff2_tex_img import (
    niff2_tex_img_list_header_builder, niff2_tex_img_list_header_writer)


class TestNiff2TexImg(unittest.TestCase):
    def test_niff2_tex_img_list_header_builder(self):
        tex_img_list_header = niff2_tex_img_list_header_builder()
        self.assertEqual(tex_img_list_header.tex_img_list_tag, 0x00120000)
        self.assertEqual(tex_img_list_header.tex_img_list_header_size, 24)
        self.assertEqual(tex_img_list_header.tex_img_list_size, 24)
        self.assertEqual(tex_img_list_header.tex_img_num, 0)
        self.assertEqual(tex_img_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(tex_img_list_header.user_extension_block_size, 0)

    def test_niff2_tex_img_list_header_writer(self):
        tex_img_list_header = niff2_tex_img_list_header_builder()
        buf = niff2_tex_img_list_header_writer(
            tex_img_list_header, bytearray())
        byte_list = [0x00, 0x12, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
