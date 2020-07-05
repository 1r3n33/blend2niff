"""NIFF2 Normal Vector."""

#
# Consts
#
TAG_VECTOR_LIST = 0x00060000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Vector List
#
class Niff2VectorListHeader:
    def __init__(self):
        self.vector_list_tag = TAG_VECTOR_LIST
        self.vector_list_header_size = (7*4)
        self.vector_list_size = (7*4)
        self.tri_nv_group_num = 0
        self.vtx_nv_group_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.vector_list_size


def niff2_vector_list_header_builder():
    return Niff2VectorListHeader()


def niff2_vector_list_header_writer(vlh, buf):
    buf += vlh.vector_list_tag.to_bytes(4, BYTE_ORDER)
    buf += vlh.vector_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vector_list_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.tri_nv_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_nv_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
