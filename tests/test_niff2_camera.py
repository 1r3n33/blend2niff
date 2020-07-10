"""NIFF2 Camera Tests."""

import unittest
from blend2niff.exporter.niff2_camera import (
    niff2_cam_list_header_builder, niff2_cam_list_header_writer)


class TestNiff2Camera(unittest.TestCase):
    def test_niff2_cam_list_header_builder(self):
        cam_list_header = niff2_cam_list_header_builder()
        self.assertEqual(cam_list_header.cam_list_tag, 0x00e0000)
        self.assertEqual(cam_list_header.cam_list_header_size, 24)
        self.assertEqual(cam_list_header.cam_list_size, 24)
        self.assertEqual(cam_list_header.cam_num, 0)
        self.assertEqual(cam_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(cam_list_header.user_extension_block_size, 0)

    def test_niff2_cam_list_header_writer(self):
        cam_list_header = niff2_cam_list_header_builder()
        buf = bytearray()
        niff2_cam_list_header_writer(cam_list_header, buf)
        self.assertEqual(buf, bytearray(
            b'\x00\x0e\x00\x00\x00\x00\x00\x18\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
