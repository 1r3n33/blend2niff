"""NIFF2 Vector Tests."""

import unittest
from blend2niff.exporter.niff2_vector import (
    niff2_vector_list_header_builder, niff2_vector_list_header_writer,
    niff2_tri_nv_group_builder, niff2_tri_nv_group_writer,
    niff2_vtx_nv_group_builder, niff2_vtx_nv_group_writer)


class TestNiff2Vector(unittest.TestCase):
    def test_niff2_vector_list_header_builder(self):
        nv_floats = [1.0, 2.0, 3.0]
        tri_nv_group = niff2_tri_nv_group_builder(123, nv_floats)
        vtx_nv_group = niff2_vtx_nv_group_builder(123, nv_floats)
        vector_list_header = niff2_vector_list_header_builder(
            [tri_nv_group], [vtx_nv_group])
        self.assertEqual(vector_list_header.vector_list_tag, 0x00060000)
        self.assertEqual(vector_list_header.vector_list_header_size, 36)
        self.assertEqual(vector_list_header.vector_list_size, 100)
        self.assertEqual(vector_list_header.tri_nv_group_num, 1)
        self.assertEqual(vector_list_header.vtx_nv_group_num, 1)
        self.assertEqual(vector_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(vector_list_header.user_extension_block_size, 0)

    def test_niff2_vector_list_header_writer(self):
        nv_floats = [1.0, 2.0, 3.0]
        tri_nv_group = niff2_tri_nv_group_builder(123, nv_floats)
        vtx_nv_group = niff2_vtx_nv_group_builder(123, nv_floats)
        vector_list_header = niff2_vector_list_header_builder(
            [tri_nv_group], [vtx_nv_group])
        buf = niff2_vector_list_header_writer(
            vector_list_header, [tri_nv_group], [vtx_nv_group], bytearray())
        byte_list = [0x00, 0x06, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x24,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0x20]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_tri_nv_group_builder(self):
        nv_floats = [1.0, 2.0, 3.0]
        tri_nv_group = niff2_tri_nv_group_builder(123, nv_floats)
        self.assertEqual(tri_nv_group.tri_nv_group_tag, 0x0060100)
        self.assertEqual(tri_nv_group.this_tri_nv_group_index, 123)
        self.assertEqual(tri_nv_group.tri_nv_group_header_size, 20)
        self.assertEqual(tri_nv_group.tri_nv_group_size, 32)
        self.assertEqual(tri_nv_group.tri_nv_num, 1)

    def test_niff2_tri_nv_group_writer(self):
        nv_floats = [1.0, 2.0, 3.0]
        tri_nv_group = niff2_tri_nv_group_builder(123, nv_floats)
        buf = niff2_tri_nv_group_writer(tri_nv_group, bytearray())
        byte_list = [0x00, 0x06, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x14,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0x01,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_vtx_nv_group_builder(self):
        nv_floats = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        vtx_nv_group = niff2_vtx_nv_group_builder(123, nv_floats)
        self.assertEqual(vtx_nv_group.vtx_nv_group_tag, 0x0060200)
        self.assertEqual(vtx_nv_group.this_vtx_nv_group_index, 123)
        self.assertEqual(vtx_nv_group.vtx_nv_group_header_size, 20)
        self.assertEqual(vtx_nv_group.vtx_nv_group_size, 44)
        self.assertEqual(vtx_nv_group.vtx_nv_num, 2)

    def test_niff2_vtx_nv_group_writer(self):
        nv_floats = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        vtx_nv_group = niff2_vtx_nv_group_builder(123, nv_floats)
        buf = niff2_vtx_nv_group_writer(vtx_nv_group, bytearray())
        byte_list = [0x00, 0x06, 0x02, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x14,
                     0x00, 0x00, 0x00, 0x2C,
                     0x00, 0x00, 0x00, 0x02,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00,
                     0x40, 0x80, 0x00, 0x00,
                     0x40, 0xA0, 0x00, 0x00,
                     0x40, 0xC0, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
