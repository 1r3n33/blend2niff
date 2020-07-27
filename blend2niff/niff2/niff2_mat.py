"""NIFF2 Material."""

import struct

#
# Consts
#
TAG_MAT_LIST = 0x000a0000
TAG_MAT = 0x000a0100

MAT_TYPE_NIFF = 0x00000000
MAT_TYPE_N64 = 0x01010101

MAT_SHADE_LIGHT_OFF = 0x00000000
MAT_SHADE_LIGHT_LOCAL = 0x00000001
MAT_SHADE_LIGHT_GLOBAL = 0x00000002
MAT_SHADE_FLAT = 0x00000000
MAT_SHADE_SMOOTH = 0x00000010
MAT_SHADE_USE_HILIGHT = 0x00000100
MAT_SHADE_USE_REFLECT = 0x00000200

MAT_CC_NIFF_VTX = 0x00000001
MAT_CC_NIFF_TRI = 0x00000002
MAT_CC_NIFF_PRIM = 0x00000004
MAT_CC_NIFF_TEX0 = 0x00000008
MAT_CC_NIFF_TEX1 = 0x00000010
MAT_CC_NIFF_VTX_ALPHA = 0x00010000
MAT_CC_NIFF_TRI_ALPHA = 0x00020000
MAT_CC_NIFF_PRIM_ALPHA = 0x00040000
MAT_CC_NIFF_TEX0_ALPHA = 0x00080000
MAT_CC_NIFF_TEX1_ALPHA = 0x00100000
MAT_CC_NIFF_NONE = 0xffffffff

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Mat List
#
class Niff2MatListHeader:
    def __init__(self, mat_num, mat_list_size):
        self.mat_list_tag = TAG_MAT_LIST
        self.mat_list_header_size = (6*4) + (mat_num*4)
        self.mat_list_size = (6*4) + (mat_num*4) + mat_list_size
        self.mat_num = mat_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.mat_list_size


def niff2_mat_list_header_builder(materials):
    mat_num = len(materials)
    mat_list_size = sum(map(lambda mat: mat.mat_size, materials))
    return Niff2MatListHeader(mat_num, mat_list_size)


def niff2_mat_list_header_writer(mat_list_header, materials, buf):
    buf += mat_list_header.mat_list_tag.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.mat_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.mat_list_size.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.mat_num.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += mat_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for mat in materials:
        buf += mat.mat_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Mat Node
#
class Niff2MatNode:
    def __init__(self, index, name_index, diffuse_rgba):
        self.mat_tag = TAG_MAT
        self.this_mat_index = index
        self.mat_size = (52*4)
        self.mat_name_index = name_index
        self.mat_type = MAT_TYPE_NIFF
        self.mat_shade_type = MAT_SHADE_LIGHT_LOCAL | MAT_SHADE_SMOOTH
        self.mat_color_type0 = MAT_CC_NIFF_PRIM
        self.mat_color_type1 = MAT_CC_NIFF_NONE
        self.mat_alpha_type0 = MAT_CC_NIFF_PRIM_ALPHA
        self.mat_alpha_type1 = MAT_CC_NIFF_NONE
        self.prim_red = diffuse_rgba[0]
        self.prim_green = diffuse_rgba[1]
        self.prim_blue = diffuse_rgba[2]
        self.prim_alpha = diffuse_rgba[3]
        self.user_flag0 = 0
        self.user_flag1 = 0
        self.user_flag2 = 0
        self.user_flag3 = 0
        self.user_flag4 = 0
        self.user_flag5 = 0
        self.user_flag6 = 0
        self.user_flag7 = 0
        self.local_light_index = 0
        self.tex_num = 0
        self.nintendo_extension_block_size = (26*4)
        self.user_extension_block_size = 0
        self.ambient_red = 1.0
        self.ambient_green = 1.0
        self.ambient_blue = 1.0
        self.ambient_alpha = 1.0
        self.emission_red = 0.0
        self.emission_green = 0.0
        self.emission_blue = 0.0
        self.emission_alpha = 0.0
        self.diffuse_red = 1.0
        self.diffuse_green = 1.0
        self.diffuse_blue = 1.0
        self.diffuse_alpha = 1.0
        self.mat_type_for_fog = MAT_TYPE_NIFF
        self.mat_color_type0_for_fog = MAT_CC_NIFF_PRIM
        self.mat_color_type1_for_fog = MAT_CC_NIFF_NONE
        self.mat_alpha_type0_for_fog = MAT_CC_NIFF_PRIM_ALPHA
        self.mat_alpha_type1_for_fog = MAT_CC_NIFF_NONE
        self.prim_red_for_fog = 1.0
        self.prim_green_for_fog = 1.0
        self.prim_blue_for_fog = 1.0
        self.prim_alpha_for_fog = 1.0
        self.external_local_light_file_name_index = BAD_INDEX
        self.external_local_light_name_index = BAD_INDEX
        self.external_tex_num = 0
        self.prim_color_anim_num = 0
        self.prim_color_anim_num_for_fog = 0

    def index(self):
        return self.this_mat_index


def niff2_mat_node_builder(index, name_index, diffuse_rgba):
    return Niff2MatNode(index, name_index, diffuse_rgba)


def niff2_mat_node_writer(mat, buf):
    buf += mat.mat_tag.to_bytes(4, BYTE_ORDER)
    buf += mat.this_mat_index.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_size.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_name_index.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_type.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_shade_type.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_color_type0.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_color_type1.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_alpha_type0.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_alpha_type1.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", mat.prim_red))
    buf += bytearray(struct.pack(">f", mat.prim_green))
    buf += bytearray(struct.pack(">f", mat.prim_blue))
    buf += bytearray(struct.pack(">f", mat.prim_alpha))
    buf += mat.user_flag0.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag1.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag2.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag3.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag4.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag5.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag6.to_bytes(4, BYTE_ORDER)
    buf += mat.user_flag7.to_bytes(4, BYTE_ORDER)
    buf += mat.local_light_index.to_bytes(4, BYTE_ORDER)
    buf += mat.tex_num.to_bytes(4, BYTE_ORDER)
    buf += mat.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += mat.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", mat.ambient_red))
    buf += bytearray(struct.pack(">f", mat.ambient_green))
    buf += bytearray(struct.pack(">f", mat.ambient_blue))
    buf += bytearray(struct.pack(">f", mat.ambient_alpha))
    buf += bytearray(struct.pack(">f", mat.emission_red))
    buf += bytearray(struct.pack(">f", mat.emission_green))
    buf += bytearray(struct.pack(">f", mat.emission_blue))
    buf += bytearray(struct.pack(">f", mat.emission_alpha))
    buf += bytearray(struct.pack(">f", mat.diffuse_red))
    buf += bytearray(struct.pack(">f", mat.diffuse_green))
    buf += bytearray(struct.pack(">f", mat.diffuse_blue))
    buf += bytearray(struct.pack(">f", mat.diffuse_alpha))
    buf += mat.mat_type_for_fog.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_color_type0_for_fog.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_color_type1_for_fog.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_alpha_type0_for_fog.to_bytes(4, BYTE_ORDER)
    buf += mat.mat_alpha_type1_for_fog.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", mat.prim_red_for_fog))
    buf += bytearray(struct.pack(">f", mat.prim_green_for_fog))
    buf += bytearray(struct.pack(">f", mat.prim_blue_for_fog))
    buf += bytearray(struct.pack(">f", mat.prim_alpha_for_fog))
    buf += mat.external_local_light_file_name_index.to_bytes(4, BYTE_ORDER)
    buf += mat.external_local_light_name_index.to_bytes(4, BYTE_ORDER)
    buf += mat.external_tex_num.to_bytes(4, BYTE_ORDER)
    buf += mat.prim_color_anim_num.to_bytes(4, BYTE_ORDER)
    buf += mat.prim_color_anim_num_for_fog.to_bytes(4, BYTE_ORDER)
    return buf
