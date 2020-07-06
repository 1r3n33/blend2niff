"""NIFF2 s,t Texture Coordinates Tests."""

import unittest
from blend2niff.exporter.niff2_st import (niff2_st_list_header_builder)


class TestNiff2St(unittest.TestCase):
    def test_niff2_st_list_header_builder(self):
        st_list_header = niff2_st_list_header_builder()
        self.assertEqual(st_list_header.st_list_tag, 0x00070000)
        self.assertEqual(st_list_header.st_list_header_size, 24)
        self.assertEqual(st_list_header.st_list_size, 24)
        self.assertEqual(st_list_header.st_group_num, 0)
        self.assertEqual(st_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(st_list_header.user_extension_block_size, 0)
