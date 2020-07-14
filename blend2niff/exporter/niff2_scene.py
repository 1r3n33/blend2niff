"""NIFF2 Scene header."""

#
# Consts
#
TAG_SCENE_HEADER = 0x00010000

SCENE_CFG_VIDEO_NTSC = 0x00000000
SCENE_CFG_VIDEO_PAL = 0x00000001
SCENE_CFG_VIDEO_MPAL = 0x00000002
SCENE_CFG_GAMMA = 0x00000004
SCENE_CFG_DITHER = 0x00000008
SCENE_CFG_DIVOT = 0x00000010

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Scene Header
#
class Niff2SceneHeader:
    def __init__(self, scene_name_index, scene_obj_link_num, scene_cam_link_num):
        self.scene_header_tag = TAG_SCENE_HEADER
        self.scene_header_size = (11*4)
        self.scene_size = (11*4) + (5*4) + \
            (scene_obj_link_num*4) + (scene_cam_link_num*4)
        self.scene_cfg = SCENE_CFG_VIDEO_NTSC | SCENE_CFG_DIVOT | SCENE_CFG_DITHER
        self.scene_name_index = scene_name_index
        self.scene_obj_link_num = scene_obj_link_num
        self.scene_env_link_num = 0
        self.scene_cam_link_num = scene_cam_link_num
        self.scene_light_link_num = 0
        self.nintendo_extension_block_size = (5*4)
        self.user_extension_block_size = 0
        self.scene_chain_root_link_num = 0
        self.external_obj_num = 0
        self.external_env_num = 0
        self.external_cam_num = 0
        self.external_light_num = 0

    def num_bytes(self):
        return self.scene_size


def niff2_scene_header_builder(scene_name_index, objs, cams):
    scene_obj_link_num = len(objs)
    scene_cam_link_num = len(cams)
    return Niff2SceneHeader(scene_name_index, scene_obj_link_num, scene_cam_link_num)


def niff2_scene_header_writer(scene_header, buf):
    buf += scene_header.scene_header_tag.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_header_size.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_size.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_cfg.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_name_index.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_obj_link_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_env_link_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_cam_link_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.scene_light_link_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += scene_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for i in range(scene_header.scene_obj_link_num):
        buf += i.to_bytes(4, BYTE_ORDER)
    for i in range(scene_header.scene_cam_link_num):
        buf += i.to_bytes(4, BYTE_ORDER)

    buf += scene_header.scene_chain_root_link_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.external_obj_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.external_env_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.external_cam_num.to_bytes(4, BYTE_ORDER)
    buf += scene_header.external_light_num.to_bytes(4, BYTE_ORDER)

    return buf
