"""NIFF2 Camera."""

import struct

#
# Consts
#
TAG_CAM_LIST = 0x000e0000
TAG_CAM = 0x000e0100

CAM_TYPE_PERSP = 0x00000000
CAM_TYPE_ORTHO = 0x00000001

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Cam List
#
class Niff2CamListHeader:
    def __init__(self, cam_num, cam_list_size):
        self.cam_list_tag = TAG_CAM_LIST
        self.cam_list_header_size = (6*4) + (cam_num*4)
        self.cam_list_size = (6*4) + (cam_num*4) + cam_list_size
        self.cam_num = cam_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.cam_list_size


def niff2_cam_list_header_builder(cams):
    cam_num = len(cams)
    cam_list_size = sum(map(lambda cam: cam.cam_size, cams))
    return Niff2CamListHeader(cam_num, cam_list_size)


def niff2_cam_list_header_writer(cam_list_header, cams, buf):
    buf += cam_list_header.cam_list_tag.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.cam_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.cam_list_size.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.cam_num.to_bytes(4, BYTE_ORDER)
    buf += cam_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += cam_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for cam in cams:
        buf += cam.cam_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Cam Node
#
class Niff2CamNode:
    def __init__(self, index, name_index):
        self.cam_tag = TAG_CAM
        self.this_cam_index = index
        self.cam_size = 25*4
        self.cam_name_index = name_index
        self.cam_type = CAM_TYPE_PERSP
        self.cam_near_clip = 1.0
        self.cam_far_clip = 1000.0
        self.cam_right_clip = 160.0
        self.cam_left_clip = -160.0
        self.cam_top_clip = 120.0
        self.cam_bottom_clip = -120.0
        self.cam_fovy = 40.0
        self.cam_aspect = 320.0/240.0
        self.cam_scale = 1.0
        self.cam_lookat_obj = BAD_INDEX
        self.cam_eye_obj = BAD_INDEX
        self.cam_up_obj = BAD_INDEX
        self.nintendo_extension_block_size = 6*4
        self.user_extension_block_size = 0
        self.external_lookat_obj_file_name_index = BAD_INDEX
        self.external_lookat_obj_name_index = BAD_INDEX
        self.external_eye_obj_file_name_index = BAD_INDEX
        self.external_eye_obj_name_index = BAD_INDEX
        self.external_up_obj_file_name_index = BAD_INDEX
        self.external_up_obj_name_index = BAD_INDEX


def niff2_cam_node_builder(index, name_index):
    return Niff2CamNode(index, name_index)


def niff2_cam_node_writer(cam_node, buf):
    buf += cam_node.cam_tag.to_bytes(4, BYTE_ORDER)
    buf += cam_node.this_cam_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.cam_size.to_bytes(4, BYTE_ORDER)
    buf += cam_node.cam_name_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.cam_type.to_bytes(4, BYTE_ORDER)
    buf += bytearray(struct.pack(">f", cam_node.cam_near_clip))
    buf += bytearray(struct.pack(">f", cam_node.cam_far_clip))
    buf += bytearray(struct.pack(">f", cam_node.cam_right_clip))
    buf += bytearray(struct.pack(">f", cam_node.cam_left_clip))
    buf += bytearray(struct.pack(">f", cam_node.cam_top_clip))
    buf += bytearray(struct.pack(">f", cam_node.cam_bottom_clip))
    buf += bytearray(struct.pack(">f", cam_node.cam_fovy))
    buf += bytearray(struct.pack(">f", cam_node.cam_aspect))
    buf += bytearray(struct.pack(">f", cam_node.cam_scale))
    buf += cam_node.cam_lookat_obj.to_bytes(4, BYTE_ORDER)
    buf += cam_node.cam_eye_obj.to_bytes(4, BYTE_ORDER)
    buf += cam_node.cam_up_obj.to_bytes(4, BYTE_ORDER)
    buf += cam_node.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += cam_node.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += cam_node.external_lookat_obj_file_name_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.external_lookat_obj_name_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.external_eye_obj_file_name_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.external_eye_obj_name_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.external_up_obj_file_name_index.to_bytes(4, BYTE_ORDER)
    buf += cam_node.external_up_obj_name_index.to_bytes(4, BYTE_ORDER)
    return buf
