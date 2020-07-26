"""NIFF2 Light."""

import struct

TAG_LIGHT_LIST = 0x000f0000
TAG_LIGHT = 0x000f0100

TAG_DIR_LIGHT_DIRECTION = 0x000f0101
TAG_DIR_LIGHT_POSITION = 0x000f0102

LIGHT_TYPE_DIRECTION = 0X00000000
LIGHT_TYPE_POSITION = 0x00000001

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


class Niff2LightListHeader:
    """
    Light List.
    """

    def __init__(self, light_num, light_list_size):
        self.light_list_tag = TAG_LIGHT_LIST
        self.light_list_header_size = (6*4) + (light_num*4)
        self.light_list_size = (6*4) + (light_num*4) + light_list_size
        self.light_num = light_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.light_list_size


def niff2_light_list_header_builder(lights):
    light_num = len(lights)
    light_list_size = sum(map(lambda light: light.light_size, lights))
    return Niff2LightListHeader(light_num, light_list_size)


def niff2_light_list_header_writer(light_list_header, lights, buf):
    buf += light_list_header.light_list_tag.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.light_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.light_list_size.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.light_num.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += light_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for light in lights:
        buf += light.light_size.to_bytes(4, BYTE_ORDER)

    return buf


class Niff2LightNode:
    """
    Light Node.
    Handles 1 ambient light + 1 directional light.
    TODO: Multiple lights support.
    """

    def __init__(self, index, name_index, ambient_rgb, light_rgb, dir_xyz):
        self.light_tag = TAG_LIGHT
        self.this_light_index = index
        self.light_header_size = (12*4)
        self.light_size = (12*4) + (9*4)
        self.light_name_index = name_index
        self.light_type = LIGHT_TYPE_DIRECTION
        self.ambient_r = ambient_rgb[0]
        self.ambient_g = ambient_rgb[1]
        self.ambient_b = ambient_rgb[2]
        self.dir_light_num = 1
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0
        self.dir_light_tag = TAG_DIR_LIGHT_DIRECTION
        self.this_dir_light_index = 0
        self.dir_light_size = 9*4
        self.dir_color_r = light_rgb[0]
        self.dir_color_g = light_rgb[1]
        self.dir_color_b = light_rgb[2]
        self.dir_x = dir_xyz[0]
        self.dir_y = dir_xyz[1]
        self.dir_z = dir_xyz[2]


def niff2_light_node_builder(index, name_index, ambient_rgb, light_rgb, dir_xyz):
    return Niff2LightNode(index, name_index, ambient_rgb, light_rgb, dir_xyz)


def niff2_light_node_writer(light_node, buf):
    buf += light_node.light_tag.to_bytes(4, BYTE_ORDER)
    buf += light_node.this_light_index.to_bytes(4, BYTE_ORDER)
    buf += light_node.light_header_size.to_bytes(4, BYTE_ORDER)
    buf += light_node.light_size.to_bytes(4, BYTE_ORDER)
    buf += light_node.light_name_index.to_bytes(4, BYTE_ORDER)
    buf += light_node.light_type.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", light_node.ambient_r))
    buf += bytearray(struct.pack(">f", light_node.ambient_g))
    buf += bytearray(struct.pack(">f", light_node.ambient_b))
    buf += light_node.dir_light_num.to_bytes(4, BYTE_ORDER)
    buf += light_node.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += light_node.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += light_node.dir_light_tag.to_bytes(4, BYTE_ORDER)
    buf += light_node.this_dir_light_index.to_bytes(4, BYTE_ORDER)
    buf += light_node.dir_light_size.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", light_node.dir_color_r))
    buf += bytearray(struct.pack(">f", light_node.dir_color_g))
    buf += bytearray(struct.pack(">f", light_node.dir_color_b))
    buf += bytearray(struct.pack(">f", light_node.dir_x))
    buf += bytearray(struct.pack(">f", light_node.dir_y))
    buf += bytearray(struct.pack(">f", light_node.dir_z))
    return buf
