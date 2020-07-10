"""NIFF2 Camera."""

#
# Consts
#
TAG_CAM_LIST = 0x000e0000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Cam List
#
class Niff2CamListHeader:
    def __init__(self):
        self.cam_list_tag = TAG_CAM_LIST
        self.cam_list_header_size = 6*4
        self.cam_list_size = 6*4
        self.cam_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.cam_list_size


def niff2_cam_list_header_builder():
    return Niff2CamListHeader()


def niff2_cam_list_header_writer(cam_list_header, buf):
    buf += cam_list_header.cam_list_tag.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.cam_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.cam_list_size.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.cam_num.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += cam_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
