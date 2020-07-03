#
# Consts
#
TAG_TRI_LIST = 0x00080000
TAG_TRI_GROUP = 0x00080100

TRI_ANIM_NONE = 0x00000000
TRI_ANIM_VTX_FULL = 0x00000001
TRI_ANIM_VTX_KEY = 0x00000002
TRI_ANIM_TRI_COLOR_FULL = 0x00000010
TRI_ANIM_TRI_COLOR_KEY = 0x00000020
TRI_ANIM_VTX_COLOR_FULL = 0x00000100
TRI_ANIM_VTX_COLOR_KEY = 0x00000200
TRI_ANIM_TRI_NV_FULL = 0x00001000
TRI_ANIM_TRI_NV_KEY = 0x00002000
TRI_ANIM_VTX_NV_FULL = 0x00010000
TRI_ANIM_VTX_NV_KEY = 0x00020000
TRI_ANIM_ST_FULL = 0x00100000
TRI_ANIM_ST_KEY = 0x00200000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Tri List
#
class Niff2TriListHeader:
    tri_list_tag: int
    tri_list_header_size: int
    tri_list_size: int
    tri_group_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    def num_bytes(self):
        return self.tri_list_size


def niff2_tri_list_header_builder(tri_groups):
    tri_group_num = len(tri_groups)
    tri_group_list_size = sum(
        map(lambda tri_group: tri_group.tri_group_size, tri_groups))

    tlh = Niff2TriListHeader()
    tlh.tri_list_tag = TAG_TRI_LIST
    tlh.tri_list_header_size = (6*4) + (tri_group_num*4)
    tlh.tri_list_size = (6*4) + (tri_group_num*4) + tri_group_list_size
    tlh.tri_group_num = tri_group_num
    tlh.nintendo_extension_block_size = 0
    tlh.user_extension_block_size = 0
    return tlh


def niff2_tri_list_header_writer(tlh, tri_groups, buf):
    buf += tlh.tri_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tlh.tri_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.tri_list_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.tri_group_num.to_bytes(4, BYTE_ORDER)
    buf += tlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for tri_group in tri_groups:
        buf += tri_group.tri_group_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# TriGroup Node
#
class Niff2TriGroupNode:
    def __init__(self, index, name_index, vtx_group_index):
        self.tri_group_tag = TAG_TRI_GROUP
        self.this_tri_group_index = index
        self.tri_group_header_size = (8*4)
        self.tri_group_size = (8*4) + (6*4)
        self.tri_group_name_index = name_index
        self.tri_anim_type = TRI_ANIM_NONE
        self.tri_anim_frame_num = 0
        self.tri_num = 0
        self.vtx_group_index = vtx_group_index
        self.tri_color_group_index = BAD_INDEX
        self.vtx_color_group_index = BAD_INDEX
        self.tri_nv_group_index = BAD_INDEX
        self.vtx_nv_group_index = BAD_INDEX
        self.st_group_index = BAD_INDEX

    def index(self):
        return self.this_tri_group_index


def niff2_tri_group_node_builder(tri_group_index, tri_group_name_index, vtx_group_index):
    return Niff2TriGroupNode(tri_group_index, tri_group_name_index, vtx_group_index)


def niff2_tri_group_node_writer(tri_group, buf):
    buf += tri_group.tri_group_tag.to_bytes(4, BYTE_ORDER)
    buf += tri_group.this_tri_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_group_header_size.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_group_size.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_group_name_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_anim_type.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_anim_frame_num.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_num.to_bytes(4, BYTE_ORDER)
    buf += tri_group.vtx_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_color_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.vtx_color_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.tri_nv_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.vtx_nv_group_index.to_bytes(4, BYTE_ORDER)
    buf += tri_group.st_group_index.to_bytes(4, BYTE_ORDER)
    return buf
