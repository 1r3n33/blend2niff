"""NIFF2 Color."""

import struct

#
# Consts
#
TAG_COLOR_LIST = 0x00050000
TAG_TRI_COLOR_GROUP = 0x00050100
TAG_VTX_COLOR_GROUP = 0x00050200

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Color List
#
class Niff2ColorListHeader:
    color_list_tag: int
    color_list_header_size: int
    color_list_size: int
    tri_color_group_num: int
    vtx_color_group_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    def num_bytes(self):
        return self.color_list_size


def niff2_color_list_header_builder(tri_color_groups, vtx_color_groups):
    tri_color_group_num = len(tri_color_groups)
    tri_color_group_size = sum(map(
        lambda tri_color_group: tri_color_group.tri_color_group_size, tri_color_groups))

    vtx_color_group_num = len(vtx_color_groups)
    vtx_color_group_size = sum(map(
        lambda vtx_color_group: vtx_color_group.vtx_color_group_size, vtx_color_groups))

    clh = Niff2ColorListHeader()
    clh.color_list_tag = TAG_COLOR_LIST
    clh.color_list_header_size = (7*4) + \
        (tri_color_group_num*4) + (vtx_color_group_num*4)
    clh.color_list_size = (7*4) + \
        (tri_color_group_num*4) + (vtx_color_group_num*4) + \
        tri_color_group_size + vtx_color_group_size
    clh.tri_color_group_num = tri_color_group_num
    clh.vtx_color_group_num = vtx_color_group_num
    clh.nintendo_extension_block_size = 0
    clh.user_extension_block_size = 0
    return clh


def niff2_color_list_header_writer(clh, tri_color_groups, vtx_color_groups, buf):
    buf += clh.color_list_tag.to_bytes(4, BYTE_ORDER)
    buf += clh.color_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += clh.color_list_size.to_bytes(4, BYTE_ORDER)
    buf += clh.tri_color_group_num.to_bytes(4, BYTE_ORDER)
    buf += clh.vtx_color_group_num.to_bytes(4, BYTE_ORDER)
    buf += clh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += clh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for tri_color_group in tri_color_groups:
        buf += tri_color_group.tri_color_group_size.to_bytes(4, BYTE_ORDER)

    for vtx_color_group in vtx_color_groups:
        buf += vtx_color_group.vtx_color_group_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# TriColorGroup Node
#
class Niff2TriColorGroup:
    def __init__(self, index, color_floats):
        self.tri_color_group_tag = TAG_TRI_COLOR_GROUP
        self.this_tri_color_group_index = index
        self.tri_color_group_header_size = (5*4)
        self.tri_color_group_size = (5*4) + (len(color_floats)*4)
        self.tri_color_num = len(color_floats)//4
        self.color_floats = color_floats


def niff2_tri_color_group_node_builder(index, color_floats):
    return Niff2TriColorGroup(index, color_floats)


def niff2_tri_color_group_node_writer(tri_color_group_node, buf):
    buf += tri_color_group_node.tri_color_group_tag.to_bytes(4, BYTE_ORDER)
    buf += tri_color_group_node.this_tri_color_group_index.to_bytes(
        4, BYTE_ORDER)
    buf += tri_color_group_node.tri_color_group_header_size.to_bytes(
        4, BYTE_ORDER)
    buf += tri_color_group_node.tri_color_group_size.to_bytes(4, BYTE_ORDER)
    buf += tri_color_group_node.tri_color_num.to_bytes(4, BYTE_ORDER)

    for value in tri_color_group_node.color_floats:
        buf += bytearray(struct.pack(">f", value))

    return buf


#
# VtxColorGroup Node
#
class Niff2VtxColorGroup:
    def __init__(self, index, color_floats):
        self.vtx_color_group_tag = TAG_VTX_COLOR_GROUP
        self.this_vtx_color_group_index = index
        self.vtx_color_group_header_size = (5*4)
        self.vtx_color_group_size = (5*4) + (len(color_floats)*4)
        self.vtx_color_num = len(color_floats)//4
        self.color_floats = color_floats


def niff2_vtx_color_group_node_builder(index, color_floats):
    return Niff2VtxColorGroup(index, color_floats)


def niff2_vtx_color_group_node_writer(vtx_color_group_node, buf):
    buf += vtx_color_group_node.vtx_color_group_tag.to_bytes(4, BYTE_ORDER)
    buf += vtx_color_group_node.this_vtx_color_group_index.to_bytes(
        4, BYTE_ORDER)
    buf += vtx_color_group_node.vtx_color_group_header_size.to_bytes(
        4, BYTE_ORDER)
    buf += vtx_color_group_node.vtx_color_group_size.to_bytes(4, BYTE_ORDER)
    buf += vtx_color_group_node.vtx_color_num.to_bytes(4, BYTE_ORDER)

    for value in vtx_color_group_node.color_floats:
        buf += bytearray(struct.pack(">f", value))

    return buf
