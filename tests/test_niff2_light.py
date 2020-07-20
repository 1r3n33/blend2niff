"""NIFF2 Light Tests."""

import unittest

from blend2niff.exporter.niff2_light import (niff2_light_list_header_builder, niff2_light_list_header_writer,
                                             niff2_light_node_builder, niff2_light_node_writer)


class TestNiff2Light(unittest.TestCase):
    def test_niff2_light_list_header_builder(self):
        lights = [niff2_light_node_builder(123, 456,
                                           [1.0, 2.0, 3.0],
                                           [4.0, 5.0, 6.0],
                                           [7.0, 8.0, 9.0])]*2
        light_list_header = niff2_light_list_header_builder(lights)
        self.assertEqual(light_list_header.light_list_tag, 0x000F0000)
        self.assertEqual(light_list_header.light_list_header_size, 32)
        self.assertEqual(light_list_header.light_list_size, 200)
        self.assertEqual(light_list_header.light_num, 2)
        self.assertEqual(light_list_header.nintendo_extension_block_size, 0)
        self.assertEqual(light_list_header.user_extension_block_size, 0)

    def test_niff2_light_list_header_writer(self):
        lights = [niff2_light_node_builder(123, 456,
                                           [1.0, 2.0, 3.0],
                                           [4.0, 5.0, 6.0],
                                           [7.0, 8.0, 9.0])]*2
        light_list_header = niff2_light_list_header_builder(lights)
        buf = niff2_light_list_header_writer(
            light_list_header, lights, bytearray())
        byte_list = [0x00, 0x0f, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x20,
                     0x00, 0x00, 0x00, 0xC8,
                     0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x54,
                     0x00, 0x00, 0x00, 0x54]
        self.assertEqual(list(buf), byte_list)

    def test_niff2_light_node_builder(self):
        light_node = niff2_light_node_builder(123, 456,
                                              [1.0, 2.0, 3.0],
                                              [4.0, 5.0, 6.0],
                                              [7.0, 8.0, 9.0])
        self.assertEqual(light_node.light_tag, 0x000F0100)
        self.assertEqual(light_node.this_light_index, 123)
        self.assertEqual(light_node.light_header_size, 48)
        self.assertEqual(light_node.light_size, 84)
        self.assertEqual(light_node.light_name_index, 456)
        self.assertEqual(light_node.light_type, 0)
        self.assertEqual(light_node.ambient_r, 1.0)
        self.assertEqual(light_node.ambient_g, 2.0)
        self.assertEqual(light_node.ambient_b, 3.0)
        self.assertEqual(light_node.dir_light_num, 1)
        self.assertEqual(light_node.nintendo_extension_block_size, 0)
        self.assertEqual(light_node.user_extension_block_size, 0)
        self.assertEqual(light_node.dir_light_tag, 0x000F0101)
        self.assertEqual(light_node.this_dir_light_index, 0)
        self.assertEqual(light_node.dir_light_size, 36)
        self.assertEqual(light_node.dir_color_r, 4.0)
        self.assertEqual(light_node.dir_color_g, 5.0)
        self.assertEqual(light_node.dir_color_b, 6.0)
        self.assertEqual(light_node.dir_x, 7.0)
        self.assertEqual(light_node.dir_y, 8.0)
        self.assertEqual(light_node.dir_z, 9.0)

    def test_niff2_light_node_writer(self):
        light_node = niff2_light_node_builder(123, 456,
                                              [1.0, 2.0, 3.0],
                                              [4.0, 5.0, 6.0],
                                              [7.0, 8.0, 9.0])
        buf = niff2_light_node_writer(light_node, bytearray())
        byte_list = [0x00, 0x0F, 0x01, 0x00,
                     0x00, 0x00, 0x00, 0x7B,
                     0x00, 0x00, 0x00, 0x30,
                     0x00, 0x00, 0x00, 0x54,
                     0x00, 0x00, 0x01, 0xC8,
                     0x00, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00,
                     0x40, 0x00, 0x00, 0x00,
                     0x40, 0x40, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x0F, 0x01, 0x01,
                     0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x24,
                     0x40, 0x80, 0x00, 0x00,
                     0x40, 0xA0, 0x00, 0x00,
                     0x40, 0xC0, 0x00, 0x00,
                     0x40, 0xE0, 0x00, 0x00,
                     0x41, 0x00, 0x00, 0x00,
                     0x41, 0x10, 0x00, 0x00]
        self.assertEqual(list(buf), byte_list)
