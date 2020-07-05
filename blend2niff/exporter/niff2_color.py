"""NIFF2 Color."""

#
# Consts
#
TAG_COLOR_LIST = 0x00050000

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

    @staticmethod
    def num_bytes():
        return 7*4


def niff2_color_list_header_builder():
    clh = Niff2ColorListHeader()
    clh.color_list_tag = TAG_COLOR_LIST
    clh.color_list_header_size = 7*4
    clh.color_list_size = 7*4
    clh.tri_color_group_num = 0
    clh.vtx_color_group_num = 0
    clh.nintendo_extension_block_size = 0
    clh.user_extension_block_size = 0
    return clh


def niff2_color_list_header_writer(clh, buf):
    buf += clh.color_list_tag.to_bytes(4, BYTE_ORDER)
    buf += clh.color_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += clh.color_list_size.to_bytes(4, BYTE_ORDER)
    buf += clh.tri_color_group_num.to_bytes(4, BYTE_ORDER)
    buf += clh.vtx_color_group_num.to_bytes(4, BYTE_ORDER)
    buf += clh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += clh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
