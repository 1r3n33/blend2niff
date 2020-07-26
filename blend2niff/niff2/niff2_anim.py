"""NIFF2 Camera."""

import struct

#
# Consts
#
TAG_ANIM_LIST = 0x000c0000
TAG_ANIM_GROUP = 0x000c0100
TAG_ANIM_STATIC = 0x000c0101

ANIM_TYPE_STATIC = 0x00000000
ANIM_TYPE_FULL = 0x00000002
ANIM_TYPE_KEY = 0x00000003
ANIM_TYPE_BILLBOARD_OBJ = 0x00000004

ANIM_ROT_ORDER_XYZ = 0x00010203
ANIM_ROT_ORDER_XZY = 0x00010302
ANIM_ROT_ORDER_YXZ = 0x00020103
ANIM_ROT_ORDER_YZX = 0x00030102
ANIM_ROT_ORDER_ZXY = 0x00020301
ANIM_ROT_ORDER_ZYX = 0x00030201

NIFF2_ANIM_CHANNEL_NO_USE = 0x00000000
NIFF2_ANIM_CHANNEL_ROTATE_AXIS = 0x00000001
NIFF2_ANIM_CHANNEL_ROTATE_X = 0x00000002
NIFF2_ANIM_CHANNEL_ROTATE_Y = 0x00000004
NIFF2_ANIM_CHANNEL_ROTATE_Z = 0x00000008
NIFF2_ANIM_CHANNEL_ORIENTATION_XY = 0x00000010
NIFF2_ANIM_CHANNEL_TRANSLATION = 0x00000020
NIFF2_ANIM_CHANNEL_UNIQUE_SCALE = 0x00000040
NIFF2_ANIM_CHANNEL_CLASSICAL_SCALE = 0x00000080
NIFF2_ANIM_CHANNEL_ORIENTATION_CONSTRAINT = 0x00000100
NIFF2_ANIM_CHANNEL_DIRECTION_CONSTRAINT = 0x00000200
NIFF2_ANIM_CHANNEL_UPVECTOR_CONSTRAINT = 0x00000400
NIFF2_ANIM_CHANNEL_PREFERRED_AXIS_CONSTRAINT = 0x00000800
NIFF2_ANIM_CHANNEL_POSITION_CONSTRAINT = 0x00001000
NIFF2_ANIM_CHANNEL_UNIQUE_SCALE_CONSTRAINT = 0x00002000
NIFF2_ANIM_CHANNEL_CLASSICAL_SCALE_CONSTRAINT = 0x00004000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Anim List
#
class Niff2AnimListHeader:
    def __init__(self, anim_group_num, anim_list_size):
        self.anim_list_tag = TAG_ANIM_LIST
        self.anim_list_header_size = (6*4) + (anim_group_num*4)
        self.anim_list_size = (6*4) + (anim_group_num*4) + anim_list_size
        self.anim_group_num = anim_group_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.anim_list_size


def niff2_anim_list_header_builder(anim_groups):
    anim_group_num = len(anim_groups)
    anim_list_size = sum(
        map(lambda anim_group: anim_group.anim_group_size, anim_groups))
    return Niff2AnimListHeader(anim_group_num, anim_list_size)


def niff2_anim_list_header_writer(anim_list_header, anim_groups, buf):
    buf += anim_list_header.anim_list_tag.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.anim_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.anim_list_size.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.anim_group_num.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += anim_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for anim_group in anim_groups:
        buf += anim_group.anim_group_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Anim Group
#
class Niff2AnimGroup:
    def __init__(self, index, name_index, anim_node):
        self.anim_group_tag = TAG_ANIM_GROUP
        self.this_anim_group_index = index
        self.anim_group_header_size = (49*4)
        self.anim_group_size = (49*4) + anim_node.anim_size
        self.anim_name_index = name_index
        self.anim_type = ANIM_TYPE_STATIC
        self.frame_rate = 0
        self.anim_num = 1
        self.anim_loop = 0
        self.anim_rot_mtx_order = ANIM_ROT_ORDER_XYZ
        self.nintendo_extension_block_size = 37*4
        self.user_extension_block_size = 0
        self.use_animation_channel = NIFF2_ANIM_CHANNEL_NO_USE
        self.rotate_axis_num = 0
        self.rotate_x_num = 0
        self.rotate_y_num = 0
        self.rotate_z_num = 0
        self.orientation_xy_num = 0
        self.translation_num = 0
        self.unique_scale_num = 0
        self.classical_scale_num = 0
        self.kind_of_orientation_constraint_node = BAD_INDEX
        self.orientation_constraint_node = BAD_INDEX
        self.kind_of_direction_constraint_node = BAD_INDEX
        self.direction_constraint_node = BAD_INDEX
        self.kind_of_up_vector_constraint_node = BAD_INDEX
        self.up_vector_constraint_node = BAD_INDEX
        self.kind_of_preferred_axis_constraint_node = BAD_INDEX
        self.preferred_axis_constraint_node = BAD_INDEX
        self.kind_of_position_constrint_node = BAD_INDEX
        self.position_constraint_node = BAD_INDEX
        self.kind_of_unique_scale_constraint_node = BAD_INDEX
        self.unique_scale_constraint_node = BAD_INDEX
        self.kind_of_classical_scale_constraint_node = BAD_INDEX
        self.classical_scale_constraint_node = BAD_INDEX
        self.external_orientation_constraint_file_name_index = BAD_INDEX
        self.external_orientation_constraint_obj_name_index = BAD_INDEX
        self.external_direction_constraint_file_name_index = BAD_INDEX
        self.external_direction_consrtaint_obj_name_index = BAD_INDEX
        self.external_upvector_constraint_file_name_index = BAD_INDEX
        self.external_upvector_constraint_obj_name_index = BAD_INDEX
        self.external_perferred_axis_constraint_file_name_index = BAD_INDEX
        self.external_preferred_axis_constraint_obj_name_index = BAD_INDEX
        self.external_position_constraint_file_name_index = BAD_INDEX
        self.external_position_constraint_obj_name_index = BAD_INDEX
        self.external_unique_scale_constraint_file_name_index = BAD_INDEX
        self.external_unique_scale_constraint_obj_name_index = BAD_INDEX
        self.external_classical_scale_constraint_file_name_index = BAD_INDEX
        self.external_classical_scale_constraint_obj_name_index = BAD_INDEX
        self.anim_node = anim_node

    def index(self):
        return self.this_anim_group_index


def niff2_anim_group_builder(index, name_index, anim_node):
    return Niff2AnimGroup(index, name_index, anim_node)


def niff2_anim_group_writer(anim_group, buf):
    buf += anim_group.anim_group_tag.to_bytes(4, BYTE_ORDER)
    buf += anim_group.this_anim_group_index.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_group_header_size.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_group_size.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_name_index.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_type.to_bytes(4, BYTE_ORDER)
    buf += anim_group.frame_rate.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_loop.to_bytes(4, BYTE_ORDER)
    buf += anim_group.anim_rot_mtx_order.to_bytes(4, BYTE_ORDER)
    buf += anim_group.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += anim_group.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf = niff2_anim_node_writer(anim_group.anim_node, buf)
    buf += anim_group.use_animation_channel.to_bytes(4, BYTE_ORDER)
    buf += anim_group.rotate_axis_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.rotate_x_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.rotate_y_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.rotate_z_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.orientation_xy_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.translation_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.unique_scale_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.classical_scale_num.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_orientation_constraint_node.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.orientation_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_direction_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.direction_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_up_vector_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.up_vector_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_preferred_axis_constraint_node.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.preferred_axis_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_position_constrint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.position_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_unique_scale_constraint_node.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.unique_scale_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.kind_of_classical_scale_constraint_node.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.classical_scale_constraint_node.to_bytes(4, BYTE_ORDER)
    buf += anim_group.external_orientation_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_orientation_constraint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_direction_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_direction_consrtaint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_upvector_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_upvector_constraint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_perferred_axis_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_preferred_axis_constraint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_position_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_position_constraint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_unique_scale_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_unique_scale_constraint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_classical_scale_constraint_file_name_index.to_bytes(
        4, BYTE_ORDER)
    buf += anim_group.external_classical_scale_constraint_obj_name_index.to_bytes(
        4, BYTE_ORDER)
    return buf


#
# Anim Node
#
class Niff2AnimNode:
    def __init__(self, translation, rotation, scale):
        self.anim_tag = TAG_ANIM_STATIC
        self.this_anim_index = 0
        self.anim_size = 13*4
        self.translate_x = translation[0]
        self.translate_y = translation[1]
        self.translate_z = translation[2]
        self.rotate_axis_x = rotation[0]
        self.rotate_axis_y = rotation[1]
        self.rotate_axis_z = rotation[2]
        self.rotate_expand_flag = 0
        self.scale_x = scale[0]
        self.scale_y = scale[1]
        self.scale_z = scale[2]


def niff2_anim_node_builder(translation, rotation, scale):
    return Niff2AnimNode(translation, rotation, scale)


def niff2_anim_node_writer(anim_node, buf):
    buf += anim_node.anim_tag.to_bytes(4, BYTE_ORDER)
    buf += anim_node.this_anim_index.to_bytes(4, BYTE_ORDER)
    buf += anim_node.anim_size.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", anim_node.translate_x))
    buf += bytearray(struct.pack(">f", anim_node.translate_y))
    buf += bytearray(struct.pack(">f", anim_node.translate_z))
    buf += bytearray(struct.pack(">f", anim_node.rotate_axis_x))
    buf += bytearray(struct.pack(">f", anim_node.rotate_axis_y))
    buf += bytearray(struct.pack(">f", anim_node.rotate_axis_z))
    buf += anim_node.rotate_expand_flag.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", anim_node.scale_x))
    buf += bytearray(struct.pack(">f", anim_node.scale_y))
    buf += bytearray(struct.pack(">f", anim_node.scale_z))
    return buf
