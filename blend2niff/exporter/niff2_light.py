"""NIFF2 Light."""

#
# Consts
#
TAG_LIGHT_LIST = 0x000f0000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Light List
#
class Niff2LightListHeader:
    def __init__(self):
        self.light_list_tag = TAG_LIGHT_LIST
        self.light_list_header_size = 6*4
        self.light_list_size = 6*4
        self.light_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.light_list_size


def niff2_light_list_header_builder():
    return Niff2LightListHeader()


def niff2_light_list_header_writer(light_list_header, buf):
    buf += light_list_header.light_list_tag.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.light_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.light_list_size.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.light_num.to_bytes(4, BYTE_ORDER)
    buf += light_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += light_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
