"""NIFF2 Vector Tests."""

import unittest
from blend2niff.exporter.niff2_vector import (
    niff2_vector_list_header_builder)


class TestNiff2Vector(unittest.TestCase):
    def test_niff2_vector_list_header_builder(self):
        vector_list_header = niff2_vector_list_header_builder()
        self.assertEqual(vector_list_header.vector_list_tag, 0x00060000)
        self.assertEqual(vector_list_header.vector_list_header_size, 28)
        self.assertEqual(vector_list_header.vector_list_size, 28)
        self.assertEqual(vector_list_header.tri_nv_group_num, 0)
        self.assertEqual(vector_list_header.vtx_nv_group_num, 0)
        self.assertEqual(vector_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(vector_list_header.user_extension_block_size, 0)


if __name__ == '__main__':
    unittest.main()
