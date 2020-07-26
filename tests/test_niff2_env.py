"""NIFF2 Environment Tests."""

import unittest

from blend2niff.niff2.niff2_env import (
    niff2_env_list_header_builder, niff2_env_list_header_writer,
    niff2_env_node_builder, niff2_env_node_writer)


class TestEnvironment(unittest.TestCase):
    def test_niff2_env_list_header_builder(self):
        envs = [niff2_env_node_builder(1, 2, [3.0, 4.0, 5.0])]*3
        env_list_header = niff2_env_list_header_builder(envs)
        self.assertEqual(env_list_header.env_list_tag, 0x00100000)
        self.assertEqual(env_list_header.env_list_header_size, 36)
        self.assertEqual(env_list_header.env_list_size, 204)
        self.assertEqual(env_list_header.env_num, 3)
        self.assertEqual(env_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(env_list_header.user_extension_block_size, 0)

    def test_niff2_env_list_header_writer(self):
        envs = [niff2_env_node_builder(1, 2, [3.0, 4.0, 5.0])]*3
        env_list_header = niff2_env_list_header_builder(envs)
        buf = niff2_env_list_header_writer(env_list_header, envs, bytearray())
        byte_list = [0x00, 0x10, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x24,
                     0x00, 0x00, 0x00, 0xCC,
                     0x00, 0x00, 0x00, 0x03,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x00, 0x38]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_env_node_builder(self):
        env_node = niff2_env_node_builder(123, 456, [0.25, 0.5, 0.75])
        self.assertEqual(env_node.env_tag, 0x00100100)
        self.assertEqual(env_node.this_env_index, 123)
        self.assertEqual(env_node.env_size, 56)
        self.assertEqual(env_node.env_name_index, 456)
        self.assertEqual(env_node.fog, 0)
        self.assertEqual(env_node.fog_color, 0xFFFFFFFF)
        self.assertEqual(env_node.fog_near, 1000)
        self.assertEqual(env_node.fog_far, 1000)
        self.assertEqual(env_node.fill_color, 0x003F7FBF)
        self.assertEqual(env_node.fill_depth, 0x00FFFFFF)
        self.assertEqual(env_node.bg_sprite_img, 0xFFFFFFFF)
        self.assertEqual(env_node.bg_sprite_depth, 0xFFFFFFFF)
        self.assertEqual(env_node.nintendo_extension_block_size, 0)
        self.assertEqual(env_node.user_extension_block_size, 0)

    def test_niff2_env_node_writer(self):
        env_node = niff2_env_node_builder(123, 456, [0.25, 0.5, 0.75])
        buf = niff2_env_node_writer(env_node, bytearray())
        byte_list = [0x00, 0x10, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x38,
                     0x00, 0x00, 0x01, 0xC8,
                     0x00, 0x00, 0x00, 0x00,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x03, 0xE8,
                     0x00, 0x00, 0x03, 0xE8,
                     0x00, 0x3F, 0x7F, 0xBF,
                     0x00, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
