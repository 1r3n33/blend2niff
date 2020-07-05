"""NIFF2 Color Tests."""

import unittest
from blend2niff.exporter.niff2_color import (niff2_color_list_header_builder)


class TestNiff2Color(unittest.TestCase):
    def test_niff2_color_list_header_builder(self):
        color_list_header = niff2_color_list_header_builder()
        self.assertEqual(color_list_header.color_list_tag, 0x00050000)
        self.assertEqual(color_list_header.color_list_header_size, 28)
        self.assertEqual(color_list_header.color_list_size, 28)
        self.assertEqual(color_list_header.tri_color_group_num, 0)
        self.assertEqual(color_list_header.vtx_color_group_num, 0)
        self.assertEqual(color_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(color_list_header.user_extension_block_size, 0)


if __name__ == '__main__':
    unittest.main()
