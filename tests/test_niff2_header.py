"""NIFF2 File Header Tests."""

import unittest
from blend2niff.niff2.niff2_header import(
    niff2_file_header_builder, niff2_file_header_writer)


class TestNiff2Header(unittest.TestCase):
    def test_niff2_file_header_builder(self):
        file_header = niff2_file_header_builder(123)
        self.assertEqual(file_header.version, 0xFF000200)
        self.assertEqual(file_header.file_size, 123)
        self.assertEqual(file_header.header_tag, 0)
        self.assertEqual(file_header.file_header_num_byte, 136)
        self.assertEqual(file_header.scene_list_num_byte, 0)
        self.assertEqual(file_header.env_list_num_byte, 0)
        self.assertEqual(file_header.cam_list_num_byte, 0)
        self.assertEqual(file_header.light_list_num_byte, 0)
        self.assertEqual(file_header.obj_list_num_byte, 0)
        self.assertEqual(file_header.shape_list_num_byte, 0)
        self.assertEqual(file_header.vtx_list_num_byte, 0)
        self.assertEqual(file_header.color_list_num_byte, 0)
        self.assertEqual(file_header.vector_list_num_byte, 0)
        self.assertEqual(file_header.st_list_num_byte, 0)
        self.assertEqual(file_header.tri_list_num_byte, 0)
        self.assertEqual(file_header.part_list_num_byte, 0)
        self.assertEqual(file_header.mat_list_num_byte, 0)
        self.assertEqual(file_header.tex_list_num_byte, 0)
        self.assertEqual(file_header.tex_img_list_num_byte, 0)
        self.assertEqual(file_header.anim_list_num_byte, 0)
        self.assertEqual(file_header.coll_list_num_byte, 0)
        self.assertEqual(file_header.switch_list_num_byte, 0)
        self.assertEqual(file_header.name_list_num_byte, 0)
        self.assertEqual(file_header.nintendo_extension_block_size, 36)
        self.assertEqual(file_header.user_extension_block_size, 0)
        self.assertEqual(file_header.ci_img_list_num_byte, 0)
        self.assertEqual(file_header.color_palette_list_num_byte, 0)
        self.assertEqual(file_header.envelope_list_num_byte, 0)
        self.assertEqual(file_header.cluster_list_num_byte, 0)
        self.assertEqual(file_header.weight_list_num_byte, 0)
        self.assertEqual(file_header.chain_root_list_num_byte, 0)
        self.assertEqual(file_header.joint_list_num_byte, 0)
        self.assertEqual(file_header.effector_list_num_byte, 0)
        self.assertEqual(file_header.external_name_list_num_byte, 0)

    def test_niff2_file_header_writer(self):
        file_header = niff2_file_header_builder(123)
        buf = bytearray()
        niff2_file_header_writer(file_header, buf)
        byte_list = [0xFF, 0x00, 0x02, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x88,
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
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x24,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
