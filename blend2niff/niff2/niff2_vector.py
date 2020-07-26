"""NIFF2 Normal Vector."""

import struct

#
# Consts
#
TAG_VECTOR_LIST = 0x00060000
TAG_TRI_NV_GROUP = 0x00060100
TAG_VTX_NV_GROUP = 0x00060200

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Vector List
#
class Niff2VectorListHeader:
    def __init__(self, tri_nv_group_num, tri_nv_group_size, vtx_nv_group_num, vtx_nv_group_size):
        self.vector_list_tag = TAG_VECTOR_LIST
        self.vector_list_header_size = (7*4) + \
            (tri_nv_group_num*4) + (vtx_nv_group_num*4)
        self.vector_list_size = (7*4) + \
            (tri_nv_group_num*4) + (vtx_nv_group_num*4) + \
            tri_nv_group_size + vtx_nv_group_size
        self.tri_nv_group_num = tri_nv_group_num
        self.vtx_nv_group_num = vtx_nv_group_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.vector_list_size


def niff2_vector_list_header_builder(tri_nv_groups, vtx_nv_groups):
    tri_nv_group_num = len(tri_nv_groups)
    tri_nv_group_size = sum(map(
        lambda tri_nv_group: tri_nv_group.tri_nv_group_size, tri_nv_groups))

    vtx_nv_group_num = len(vtx_nv_groups)
    vtx_nv_group_size = sum(map(
        lambda vtx_nv_group: vtx_nv_group.vtx_nv_group_size, vtx_nv_groups))

    return Niff2VectorListHeader(tri_nv_group_num, tri_nv_group_size,
                                 vtx_nv_group_num, vtx_nv_group_size)


def niff2_vector_list_header_writer(vlh, tri_nv_groups, vtx_nv_groups, buf):
    buf += vlh.vector_list_tag.to_bytes(4, BYTE_ORDER)
    buf += vlh.vector_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vector_list_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.tri_nv_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_nv_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for tri_nv_group in tri_nv_groups:
        buf += tri_nv_group.tri_nv_group_size.to_bytes(4, BYTE_ORDER)

    for vtx_nv_group in vtx_nv_groups:
        buf += vtx_nv_group.vtx_nv_group_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# TriNv Group
#
class Niff2TriNvGroup:
    def __init__(self, index, nv_floats):
        self.tri_nv_group_tag = TAG_TRI_NV_GROUP
        self.this_tri_nv_group_index = index
        self.tri_nv_group_header_size = (5*4)
        self.tri_nv_group_size = (5*4) + (len(nv_floats)*4)
        self.tri_nv_num = len(nv_floats)//3
        self.nv_floats = nv_floats


def niff2_tri_nv_group_builder(index, nv_floats):
    return Niff2TriNvGroup(index, nv_floats)


def niff2_tri_nv_group_writer(tri_nv_group, buf):
    buf += tri_nv_group.tri_nv_group_tag.to_bytes(4, BYTE_ORDER)
    buf += tri_nv_group.this_tri_nv_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_nv_group.tri_nv_group_header_size.to_bytes(4, BYTE_ORDER)
    buf += tri_nv_group.tri_nv_group_size.to_bytes(4, BYTE_ORDER)
    buf += tri_nv_group.tri_nv_num.to_bytes(4, BYTE_ORDER)

    for value in tri_nv_group.nv_floats:
        buf += bytearray(struct.pack(">f", value))

    return buf


#
# VtxNv Group
#
class Niff2VtxNvGroup:
    def __init__(self, index, nv_floats):
        self.vtx_nv_group_tag = TAG_VTX_NV_GROUP
        self.this_vtx_nv_group_index = index
        self.vtx_nv_group_header_size = (5*4)
        self.vtx_nv_group_size = (5*4) + (len(nv_floats)*4)
        self.vtx_nv_num = len(nv_floats)//3
        self.nv_floats = nv_floats


def niff2_vtx_nv_group_builder(index, nv_floats):
    return Niff2VtxNvGroup(index, nv_floats)


def niff2_vtx_nv_group_writer(vtx_nv_group, buf):
    buf += vtx_nv_group.vtx_nv_group_tag.to_bytes(4, BYTE_ORDER)
    buf += vtx_nv_group.this_vtx_nv_group_index.to_bytes(4, BYTE_ORDER)
    buf += vtx_nv_group.vtx_nv_group_header_size.to_bytes(4, BYTE_ORDER)
    buf += vtx_nv_group.vtx_nv_group_size.to_bytes(4, BYTE_ORDER)
    buf += vtx_nv_group.vtx_nv_num.to_bytes(4, BYTE_ORDER)

    for value in vtx_nv_group.nv_floats:
        buf += bytearray(struct.pack(">f", value))

    return buf
