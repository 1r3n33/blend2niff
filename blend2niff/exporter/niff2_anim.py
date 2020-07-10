"""NIFF2 Camera."""

#
# Consts
#
TAG_ANIM_LIST = 0x000c0000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Anim List
#
class Niff2AnimListHeader:
    def __init__(self):
        self.anim_list_tag = TAG_ANIM_LIST
        self.anim_list_header_size = 6*4
        self.anim_list_size = 6*4
        self.anim_group_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.anim_list_size


def niff2_anim_list_header_builder():
    return Niff2AnimListHeader()


def niff2_anim_list_header_writer(anim_list_header, buf):
    buf += anim_list_header.anim_list_tag.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.anim_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.anim_list_size.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.anim_group_num.to_bytes(4, BYTE_ORDER)
    buf += anim_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += anim_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
