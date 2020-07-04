"""NIFF2 Material Tests."""

import unittest
from blend2niff.exporter.niff2_mat import (niff2_mat_list_header_builder)


class TestNiff2Mat(unittest.TestCase):
    def test_niff2_mat_list_header_builder(self):
        mat_list_header = niff2_mat_list_header_builder()
        self.assertEqual(mat_list_header.mat_list_tag, 0x000a0000)
        self.assertEqual(mat_list_header.mat_list_header_size, 24)
        self.assertEqual(mat_list_header.mat_list_size, 24)
        self.assertEqual(mat_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(mat_list_header.user_extension_block_size, 0)


if __name__ == '__main__':
    unittest.main()
