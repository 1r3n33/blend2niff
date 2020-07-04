"""NIFF2 Material."""

#
# Consts
#

TAG_MAT_LIST = 0x000a0000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Mat List
#
class Niff2MatListHeader:
    def __init__(self):
        self.mat_list_tag = TAG_MAT_LIST
        self.mat_list_header_size = (6*4)
        self.mat_list_size = (6*4)
        self.mat_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.mat_list_size


def niff2_mat_list_header_builder():
    return Niff2MatListHeader()


def niff2_mat_list_header_writer(mat_list_header, buf):
    buf += mat_list_header.mat_list_tag.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.mat_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.mat_list_size.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.mat_num.to_bytes(4, BYTE_ORDER)
    buf += mat_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += mat_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
