"""NIFF2 s,t Texture Coordinates."""

import struct

#
# Consts
#
TAG_ST_LIST = 0x00070000
TAG_ST_GROUP = 0x00070100

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# St List
#
class Niff2StListHeader:
    def __init__(self, st_group_num, st_group_size):
        self.st_list_tag = TAG_ST_LIST
        self.st_list_header_size = (6*4) + (st_group_num*4)
        self.st_list_size = (6*4) + (st_group_num*4) + st_group_size
        self.st_group_num = st_group_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.st_list_size


def niff2_st_list_header_builder(st_groups):
    st_group_num = len(st_groups)
    st_group_size = sum(
        map(lambda st_group: st_group.st_group_size, st_groups))
    return Niff2StListHeader(st_group_num, st_group_size)


def niff2_st_list_header_writer(st_list_header, st_groups, buf):
    buf += st_list_header.st_list_tag.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.st_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.st_list_size.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.st_group_num.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for st_group in st_groups:
        buf += st_group.st_group_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# StGroup Node
#
class Niff2StGroupNode:
    def __init__(self, index, st_floats):
        self.st_group_tag = TAG_ST_GROUP
        self.this_st_group_index = index
        self.st_group_header_size = (5*4)
        self.st_group_size = (5*4) + (len(st_floats)*4)
        self.st_num = len(st_floats)//2
        self.st_floats = st_floats


def niff2_st_group_node_builder(index, st_floats):
    return Niff2StGroupNode(index, st_floats)


def niff2_st_group_node_writer(st_group_node, buf):
    buf += st_group_node.st_group_tag.to_bytes(4, BYTE_ORDER)
    buf += st_group_node.this_st_group_index.to_bytes(4, BYTE_ORDER)
    buf += st_group_node.st_group_header_size.to_bytes(4, BYTE_ORDER)
    buf += st_group_node.st_group_size.to_bytes(4, BYTE_ORDER)
    buf += st_group_node.st_num.to_bytes(4, BYTE_ORDER)

    for value in st_group_node.st_floats:
        buf += bytearray(struct.pack(">f", value))

    return buf
