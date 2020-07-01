#
# Consts
#
TAG_VTX_LIST = 0x00040000

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

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_vtx_list_header_builder():
    vlh = Niff2VtxListHeader()
    vlh.vtx_list_tag = TAG_VTX_LIST
    vlh.vtx_list_header_size = 6*4
    vlh.vtx_list_size = 6*4
    vlh.vtx_group_num = 0
    vlh.nintendo_extension_block_size = 0
    vlh.user_extension_block_size = 0
    return vlh


def niff2_vtx_list_header_writer(vlh, buf):
    buf += vlh.vtx_list_tag.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_list_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
