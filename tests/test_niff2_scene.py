"""NIFF2 Scene header."""

import unittest

from blend2niff.exporter.niff2_scene import (
    niff2_scene_header_builder, niff2_scene_header_writer)


class TestNiff2SceneHeader(unittest.TestCase):
    def test_niff2_scene_header_builder(self):
        scene_header = niff2_scene_header_builder(
            12, [None]*34, [None]*56, [None]*78)
        self.assertEqual(scene_header.scene_header_tag, 0x00010000)
        self.assertEqual(scene_header.scene_header_size, 44)
        self.assertEqual(scene_header.scene_size, 736)
        self.assertEqual(scene_header.scene_cfg, 0x00000018)
        self.assertEqual(scene_header.scene_name_index, 12)
        self.assertEqual(scene_header.scene_obj_link_num, 34)
        self.assertEqual(scene_header.scene_env_link_num, 78)
        self.assertEqual(scene_header.scene_cam_link_num, 56)
        self.assertEqual(scene_header.scene_light_link_num, 0)
        self.assertEqual(scene_header.nintendo_extension_block_size, 20)
        self.assertEqual(scene_header.user_extension_block_size, 0)
        self.assertEqual(scene_header.scene_chain_root_link_num, 0)
        self.assertEqual(scene_header.external_obj_num, 0)
        self.assertEqual(scene_header.external_env_num, 0)
        self.assertEqual(scene_header.external_cam_num, 0)
        self.assertEqual(scene_header.external_light_num, 0)

    def test_niff2_scene_header_writer(self):
        scene_header = niff2_scene_header_builder(
            1, [None]*2, [None]*3, [None]*4)
        buf = bytearray()
        niff2_scene_header_writer(scene_header, buf)
        byte_list = [0x00, 0x01, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x2C,
                     0x00, 0x00, 0x00, 0x64,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x03,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x14,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x03,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
