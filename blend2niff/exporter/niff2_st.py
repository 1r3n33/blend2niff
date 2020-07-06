"""NIFF2 s,t Texture Coordinates."""

#
# Consts
#
TAG_ST_LIST = 0x00070000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# St List
#
class Niff2StListHeader:
    def __init__(self):
        self.st_list_tag = TAG_ST_LIST
        self.st_list_header_size = 6*4
        self.st_list_size = 6*4
        self.st_group_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.st_list_size


def niff2_st_list_header_builder():
    return Niff2StListHeader()


def niff2_st_list_header_writer(st_list_header, buf):
    buf += st_list_header.st_list_tag.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.st_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.st_list_size.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.st_group_num.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += st_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
