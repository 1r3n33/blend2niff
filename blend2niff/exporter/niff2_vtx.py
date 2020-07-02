import struct

#
# Consts
#
TAG_VTX_LIST = 0x00040000
TAG_VTX_GROUP = 0x00040100

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Vtx List
#
class Niff2VtxListHeader:
    vtx_list_tag: int
    vtx_list_header_size: int
    vtx_list_size: int
    vtx_group_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    def num_bytes(self):
        return self.vtx_list_size


def niff2_vtx_list_header_builder(vtx_groups):
    vtx_group_num = len(vtx_groups)
    vtx_group_list_size = sum(
        map(lambda vtx_group: vtx_group.vtx_group_size, vtx_groups))

    vlh = Niff2VtxListHeader()
    vlh.vtx_list_tag = TAG_VTX_LIST
    vlh.vtx_list_header_size = (6*4) + (vtx_group_num*4)
    vlh.vtx_list_size = (6*4) + (vtx_group_num*4) + vtx_group_list_size
    vlh.vtx_group_num = vtx_group_num
    vlh.nintendo_extension_block_size = 0
    vlh.user_extension_block_size = 0
    return vlh


def niff2_vtx_list_header_writer(vlh, vtx_groups, buf):
    buf += vlh.vtx_list_tag.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_list_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for vtx_group in vtx_groups:
        buf += vtx_group.vtx_group_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# VtxGroup Node
#
class Niff2VtxGroupNode:
    def __init__(self, index, name_index, vtx_floats):
        self.vtx_group_tag = TAG_VTX_GROUP
        self.this_vtx_group_index = index
        self.vtx_group_header_size = (6*4)
        self.vtx_group_size = (6*4) + (len(vtx_floats)*4)
        self.vtx_group_name_index = name_index
        self.vtx_num = len(vtx_floats)//3
        self.vtx_floats = vtx_floats

    def index(self):
        return self.this_vtx_group_index


def niff2_vtx_group_node_builder(vtx_group_index, vtx_group_name_index, vtx_floats):
    return Niff2VtxGroupNode(vtx_group_index, vtx_group_name_index, vtx_floats)


def niff2_vtx_group_node_writer(vtx_group, buf):
    buf += vtx_group.vtx_group_tag.to_bytes(4, BYTE_ORDER)
    buf += vtx_group.this_vtx_group_index.to_bytes(4, BYTE_ORDER)
    buf += vtx_group.vtx_group_header_size.to_bytes(4, BYTE_ORDER)
    buf += vtx_group.vtx_group_size.to_bytes(4, BYTE_ORDER)
    buf += vtx_group.vtx_group_name_index.to_bytes(4, BYTE_ORDER)
    buf += vtx_group.vtx_num.to_bytes(4, BYTE_ORDER)

    for f in vtx_group.vtx_floats:
        buf += bytearray(struct.pack(">f", f))

    return buf
