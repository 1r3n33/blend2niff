"""NIFF2 Environment Tests."""

import unittest

from blend2niff.exporter.niff2_env import (
    niff2_env_list_header_builder, niff2_env_list_header_writer)


class TestEnvironment(unittest.TestCase):
    def test_niff2_env_list_header_builder(self):
        env_list_header = niff2_env_list_header_builder()
        self.assertEqual(env_list_header.env_list_tag, 0x00100000)
        self.assertEqual(env_list_header.env_list_header_size, 24)
        self.assertEqual(env_list_header.env_list_size, 24)
        self.assertEqual(env_list_header.env_num, 0)
        self.assertEqual(env_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(env_list_header.user_extension_block_size, 0)

    def test_niff2_env_list_header_writer(self):
        env_list_header = niff2_env_list_header_builder()
        buf = bytearray()
        niff2_env_list_header_writer(env_list_header, buf)
        byte_list = [0x00, 0x10, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x18,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
