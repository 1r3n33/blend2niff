"""NIFF2 Camera Tests."""

import unittest
from blend2niff.exporter.niff2_camera import (
    niff2_cam_list_header_builder, niff2_cam_list_header_writer,
    niff2_cam_node_builder, niff2_cam_node_writer)


class TestNiff2Camera(unittest.TestCase):
    def test_niff2_cam_list_header_builder(self):
        cams = [niff2_cam_node_builder(12, 34), niff2_cam_node_builder(56, 78)]
        cam_list_header = niff2_cam_list_header_builder(cams)
        self.assertEqual(cam_list_header.cam_list_tag, 0x00e0000)
        self.assertEqual(cam_list_header.cam_list_header_size, 32)
        self.assertEqual(cam_list_header.cam_list_size, 232)
        self.assertEqual(cam_list_header.cam_num, 2)
        self.assertEqual(cam_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(cam_list_header.user_extension_block_size, 0)

    def test_niff2_cam_list_header_writer(self):
        cams = [niff2_cam_node_builder(12, 34), niff2_cam_node_builder(56, 78)]
        cam_list_header = niff2_cam_list_header_builder(cams)
        buf = bytearray()
        niff2_cam_list_header_writer(cam_list_header, cams, buf)
        byte_list = [0x00, 0x0E, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0xE8,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x64]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_cam_node_builder(self):
        cam_node = niff2_cam_node_builder(123, 456)
        self.assertEqual(cam_node.cam_tag, 0x00e0100)
        self.assertEqual(cam_node.this_cam_index, 123)
        self.assertEqual(cam_node.cam_size, 100)
        self.assertEqual(cam_node.cam_name_index, 456)
        self.assertEqual(cam_node.cam_type, 0)
        self.assertEqual(cam_node.cam_near_clip, 1.0)
        self.assertEqual(cam_node.cam_far_clip, 1000.0)
        self.assertEqual(cam_node.cam_right_clip, 160.0)
        self.assertEqual(cam_node.cam_left_clip, -160.0)
        self.assertEqual(cam_node.cam_top_clip, 120.0)
        self.assertEqual(cam_node.cam_bottom_clip, -120.0)
        self.assertEqual(cam_node.cam_fovy, 40.0)
        self.assertEqual(cam_node.cam_aspect, 4.0/3.0)
        self.assertEqual(cam_node.cam_scale, 1.0)
        self.assertEqual(cam_node.cam_lookat_obj, 0xFFFFFFFF)
        self.assertEqual(cam_node.cam_eye_obj, 0xFFFFFFFF)
        self.assertEqual(cam_node.cam_up_obj, 0xFFFFFFFF)
        self.assertEqual(cam_node.nintendo_extension_block_size, 24)
        self.assertEqual(cam_node.user_extension_block_size, 0)
        self.assertEqual(
            cam_node.external_lookat_obj_file_name_index, 0xFFFFFFFF)
        self.assertEqual(cam_node.external_lookat_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(cam_node.external_eye_obj_file_name_index, 0xFFFFFFFF)
        self.assertEqual(cam_node.external_eye_obj_name_index, 0xFFFFFFFF)
        self.assertEqual(cam_node.external_up_obj_file_name_index, 0xFFFFFFFF)
        self.assertEqual(cam_node.external_up_obj_name_index, 0xFFFFFFFF)

    def test_niff2_cam_node_writer(self):
        cam_node = niff2_cam_node_builder(123, 456)
        buf = bytearray()
        niff2_cam_node_writer(cam_node, buf)
        byte_list = [0x00, 0x0E, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x01, 0xC8,
                     0x00, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x44, 0x7A, 0x00, 0x00,
                     0x43, 0x20, 0x00, 0x00,
                     0xC3, 0x20, 0x00, 0x00,
                     0x42, 0xF0, 0x00, 0x00,
                     0xC2, 0xF0, 0x00, 0x00,
                     0x42, 0x20, 0x00, 0x00,
                     0x3F, 0xAA, 0xAA, 0xAB,
                     0x3F, 0x80, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF]
        self.assertEqual(list(buf), byte_list)
