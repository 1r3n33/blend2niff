"""NIFF2 Shape Parts."""

#
# Consts
#
TAG_PART_LIST = 0x00090000
TAG_PART = 0x00090100

USE_SHAPE_MAT = 0x80000000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Part List
#
class Niff2PartListHeader:
    part_list_tag: int
    part_list_header_size: int
    part_list_size: int
    part_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    def num_bytes(self):
        return self.part_list_size


def niff2_part_list_header_builder(parts):
    part_num = len(parts)
    part_list_size = sum(map(lambda part: part.part_size, parts))

    plh = Niff2PartListHeader()
    plh.part_list_tag = TAG_PART_LIST
    plh.part_list_header_size = (6*4) + (part_num*4)
    plh.part_list_size = (6*4) + (part_num*4) + part_list_size
    plh.part_num = part_num
    plh.nintendo_extension_block_size = 0
    plh.user_extension_block_size = 0
    return plh


def niff2_part_list_header_writer(plh, parts, buf):
    buf += plh.part_list_tag.to_bytes(4, BYTE_ORDER)
    buf += plh.part_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += plh.part_list_size.to_bytes(4, BYTE_ORDER)
    buf += plh.part_num.to_bytes(4, BYTE_ORDER)
    buf += plh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += plh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for part in parts:
        buf += part.part_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Part Node
#
class Niff2PartNode:
    def __init__(self, index, name_index, tri_group_index, mat_index, tri_indices):
        self.part_tag = TAG_PART
        self.this_part_index = index
        self.part_size = (9*4) + (len(tri_indices)*4)
        self.part_name_index = name_index
        self.mat_index = mat_index
        self.tri_group_index = tri_group_index
        self.part_tri_num = len(tri_indices)
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0
        self.tri_indices = tri_indices

    def index(self):
        return self.this_part_index


def niff2_part_node_builder(index, name_index, tri_group_index, mat_index, tri_indices):
    return Niff2PartNode(index, name_index, tri_group_index, mat_index, tri_indices)


def niff2_part_node_writer(part, buf):
    buf += part.part_tag.to_bytes(4, BYTE_ORDER)
    buf += part.this_part_index.to_bytes(4, BYTE_ORDER)
    buf += part.part_size.to_bytes(4, BYTE_ORDER)
    buf += part.part_name_index.to_bytes(4, BYTE_ORDER)
    buf += part.mat_index.to_bytes(4, BYTE_ORDER)
    buf += part.tri_group_index.to_bytes(4, BYTE_ORDER)
    buf += part.part_tri_num.to_bytes(4, BYTE_ORDER)
    buf += part.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += part.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    for index in part.tri_indices:
        buf += index.to_bytes(4, BYTE_ORDER)
    return buf
