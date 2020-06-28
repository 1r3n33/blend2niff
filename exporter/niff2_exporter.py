import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator
from .niff2_name import *
from .niff2_obj import *
from .niff2_shape import *

#
# Consts
#
MAKER_CODE = 0xFF
TOOL_CODE = 0x00
NIFF_MAJOR_VERSION = 0x02
NIFF_MINOR_VERSION = 0x00

TAG_HEADER = 0x00000000
TAG_SCENE_HEADER = 0x00010000
TAG_ENV_LIST = 0x00100000
TAG_CAM_LIST = 0x000e0000
TAG_LIGHT_LIST = 0x000f0000
TAG_VTX_LIST = 0x00040000
TAG_TRI_LIST = 0x00080000
TAG_COLOR_LIST = 0x00050000
TAG_VECTOR_LIST = 0x00060000
TAG_ST_LIST = 0x00070000
TAG_PART_LIST = 0x00090000
TAG_MAT_LIST = 0x000a0000
TAG_TEX_LIST = 0x000b0000
TAG_TEX_IMG_LIST = 0x00120000
TAG_ANIM_LIST = 0x000c0000
TAG_COLL_LIST = 0x000d0000
TAG_SWITCH_LIST = 0x00130000
TAG_CI_IMG_LIST = 0x00200000
TAG_COLOR_PALETTE_LIST = 0x00210000
TAG_ENVELOPE_LIST = 0x00220000
TAG_CLUSTER_LIST = 0x00280000
TAG_WEIGHT_LIST = 0x00230000
TAG_CHAIN_ROOT_LIST = 0x00240000
TAG_JOINT_LIST = 0x00250000
TAG_EFFECTOR_LIST = 0x00260000
TAG_EXTERNAL_NAME_LIST = 0x00270000

SCENE_CFG_VIDEO_NTSC = 0x00000000
SCENE_CFG_VIDEO_PAL = 0x00000001
SCENE_CFG_VIDEO_MPAL = 0x00000002
SCENE_CFG_GAMMA = 0x00000004
SCENE_CFG_DITHER = 0x00000008
SCENE_CFG_DIVOT = 0x00000010

CAM_TYPE_PERSP = 0x00000000
CAM_TYPE_ORTHO = 0x00000001

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# File Header
#
class Niff2FileHeader:
    version: int
    file_size: int
    header_tag: int
    file_header_num_byte: int
    scene_list_num_byte: int
    env_list_num_byte: int
    cam_list_num_byte: int
    light_list_num_byte: int
    obj_list_num_byte: int
    shape_list_num_byte: int
    vtx_list_num_byte: int
    color_list_num_byte: int
    vector_list_num_byte: int
    st_list_num_byte: int
    tri_list_num_byte: int
    part_list_num_byte: int
    mat_list_num_byte: int
    tex_list_num_byte: int
    tex_img_list_num_byte: int
    anim_list_num_byte: int
    coll_list_num_byte: int
    switch_list_num_byte: int
    name_list_num_byte: int
    nintendo_extension_block_size: int
    user_extension_block_size: int
    ci_img_list_num_byte: int
    color_palette_list_num_byte: int
    envelope_list_num_byte: int
    cluster_list_num_byte: int
    weight_list_num_byte: int
    chain_root_list_num_byte: int
    joint_list_num_byte: int
    effector_list_num_byte: int
    external_name_list_num_byte: int

    @staticmethod
    def num_bytes():
        return (25*4) + (9*4)


def niff2_file_header_builder(file_size):
    fh = Niff2FileHeader()
    fh.version = MAKER_CODE << 24 | TOOL_CODE << 16 | NIFF_MAJOR_VERSION << 8 | NIFF_MINOR_VERSION
    fh.file_size = file_size
    fh.header_tag = TAG_HEADER
    fh.file_header_num_byte = (25*4) + (9*4)
    fh.scene_list_num_byte = 0
    fh.env_list_num_byte = 0
    fh.cam_list_num_byte = 0
    fh.light_list_num_byte = 0
    fh.obj_list_num_byte = 0
    fh.shape_list_num_byte = 0
    fh.vtx_list_num_byte = 0
    fh.color_list_num_byte = 0
    fh.vector_list_num_byte = 0
    fh.st_list_num_byte = 0
    fh.tri_list_num_byte = 0
    fh.part_list_num_byte = 0
    fh.mat_list_num_byte = 0
    fh.tex_list_num_byte = 0
    fh.tex_img_list_num_byte = 0
    fh.anim_list_num_byte = 0
    fh.coll_list_num_byte = 0
    fh.switch_list_num_byte = 0
    fh.name_list_num_byte = 0
    fh.nintendo_extension_block_size = 9*4
    fh.user_extension_block_size = 0
    fh.ci_img_list_num_byte = 0
    fh.color_palette_list_num_byte = 0
    fh.envelope_list_num_byte = 0
    fh.cluster_list_num_byte = 0
    fh.weight_list_num_byte = 0
    fh.chain_root_list_num_byte = 0
    fh.joint_list_num_byte = 0
    fh.effector_list_num_byte = 0
    fh.external_name_list_num_byte = 0
    return fh


def niff2_file_header_writer(fh, buf):
    buf += fh.version.to_bytes(4, BYTE_ORDER)
    buf += fh.file_size.to_bytes(4, BYTE_ORDER)
    buf += fh.header_tag.to_bytes(4, BYTE_ORDER)
    buf += fh.file_header_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.scene_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.env_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.cam_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.light_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.obj_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.shape_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.vtx_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.color_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.vector_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.st_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.tri_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.part_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.mat_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.tex_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.tex_img_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.anim_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.coll_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.switch_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.name_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += fh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += fh.ci_img_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.color_palette_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.envelope_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.cluster_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.weight_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.chain_root_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.joint_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.effector_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += fh.external_name_list_num_byte.to_bytes(4, BYTE_ORDER)
    return buf


#
# Scene Header
#
class Niff2SceneHeader:
    scene_header_tag: int
    scene_header_size: int
    scene_size: int
    scene_cfg: int
    scene_name_index: int
    scene_obj_link_num: int
    scene_env_link_num: int
    scene_cam_link_num: int
    scene_light_link_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int
    scene_chain_root_link_num: int
    external_obj_num: int
    external_env_num: int
    external_cam_num: int
    external_light_num: int

    def num_bytes(self):
        return (11*4) + (5*4) + (self.scene_obj_link_num*4)


def niff2_scene_header_builder(scene_name_index, objs):
    scene_obj_link_num = len(objs)

    sh = Niff2SceneHeader()
    sh.scene_header_tag = TAG_SCENE_HEADER
    sh.scene_header_size = 11*4
    sh.scene_cfg = SCENE_CFG_VIDEO_NTSC | SCENE_CFG_DIVOT | SCENE_CFG_DITHER
    sh.scene_name_index = scene_name_index
    sh.scene_obj_link_num = scene_obj_link_num
    sh.scene_env_link_num = 0
    sh.scene_cam_link_num = 0
    sh.scene_light_link_num = 0
    sh.nintendo_extension_block_size = 5*4
    sh.user_extension_block_size = 0
    sh.scene_chain_root_link_num = 0
    sh.external_obj_num = 0
    sh.external_env_num = 0
    sh.external_cam_num = 0
    sh.external_light_num = 0

    sh.scene_size = sh.num_bytes()

    return sh


def niff2_scene_header_writer(sh, buf):
    buf += sh.scene_header_tag.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_header_size.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_size.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_cfg.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_name_index.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_obj_link_num.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_env_link_num.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_cam_link_num.to_bytes(4, BYTE_ORDER)
    buf += sh.scene_light_link_num.to_bytes(4, BYTE_ORDER)
    buf += sh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += sh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for i in range(sh.scene_obj_link_num):
        buf += i.to_bytes(4, BYTE_ORDER)

    buf += sh.scene_chain_root_link_num.to_bytes(4, BYTE_ORDER)
    buf += sh.external_obj_num.to_bytes(4, BYTE_ORDER)
    buf += sh.external_env_num.to_bytes(4, BYTE_ORDER)
    buf += sh.external_cam_num.to_bytes(4, BYTE_ORDER)
    buf += sh.external_light_num.to_bytes(4, BYTE_ORDER)

    return buf


#
# Env List
#
class Niff2EnvListHeader:
    env_list_tag: int
    env_list_header_size: int
    env_list_size: int
    env_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_env_list_header_builder(data):
    elh = Niff2EnvListHeader()
    elh.env_list_tag = TAG_ENV_LIST
    elh.env_list_header_size = 6*4
    elh.env_list_size = 6*4
    elh.env_num = 0
    elh.nintendo_extension_block_size = 0
    elh.user_extension_block_size = 0
    return elh


def niff2_env_list_header_writer(elh, buf):
    buf += elh.env_list_tag.to_bytes(4, BYTE_ORDER)
    buf += elh.env_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += elh.env_list_size.to_bytes(4, BYTE_ORDER)
    buf += elh.env_num.to_bytes(4, BYTE_ORDER)
    buf += elh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += elh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Cam List
#
class Niff2CamListHeader:
    cam_list_tag: int
    cam_list_header_size: int
    cam_list_size: int
    cam_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_cam_list_header_builder(data):
    clh = Niff2CamListHeader()
    clh.cam_list_tag = TAG_CAM_LIST
    clh.cam_list_header_size = 6*4
    clh.cam_list_size = 6*4
    clh.cam_num = 0
    clh.nintendo_extension_block_size = 0
    clh.user_extension_block_size = 0
    return clh


def niff2_cam_list_header_writer(clh, buf):
    buf += clh.cam_list_tag.to_bytes(4, BYTE_ORDER)
    buf += clh.cam_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += clh.cam_list_size.to_bytes(4, BYTE_ORDER)
    buf += clh.cam_num.to_bytes(4, BYTE_ORDER)
    buf += clh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += clh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Light List
#
class Niff2LightListHeader:
    light_list_tag: int
    light_list_header_size: int
    light_list_size: int
    light_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_light_list_header_builder(data):
    llh = Niff2LightListHeader()
    llh.light_list_tag = TAG_LIGHT_LIST
    llh.light_list_header_size = 6*4
    llh.light_list_size = 6*4
    llh.light_num = 0
    llh.nintendo_extension_block_size = 0
    llh.user_extension_block_size = 0
    return llh


def niff2_light_list_header_writer(llh, buf):
    buf += llh.light_list_tag.to_bytes(4, BYTE_ORDER)
    buf += llh.light_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += llh.light_list_size.to_bytes(4, BYTE_ORDER)
    buf += llh.light_num.to_bytes(4, BYTE_ORDER)
    buf += llh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += llh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


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


def niff2_vtx_list_header_builder(data):
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


#
# Tri List
#
class Niff2TriListHeader:
    tri_list_tag: int
    tri_list_header_size: int
    tri_list_size: int
    tri_goup_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_tri_list_header_builder(data):
    tlh = Niff2TriListHeader()
    tlh.tri_list_tag = TAG_TRI_LIST
    tlh.tri_list_header_size = 6*4
    tlh.tri_list_size = 6*4
    tlh.tri_group_num = 0
    tlh.nintendo_extension_block_size = 0
    tlh.user_extension_block_size = 0
    return tlh


def niff2_tri_list_header_writer(tlh, buf):
    buf += tlh.tri_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tlh.tri_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.tri_list_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.tri_group_num.to_bytes(4, BYTE_ORDER)
    buf += tlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Color List
#
class Niff2ColorListHeader:
    color_list_tag: int
    color_list_header_size: int
    color_list_size: int
    tri_color_goup_num: int
    vtx_color_goup_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 7*4


def niff2_color_list_header_builder(data):
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


#
# Vector List
#
class Niff2VectorListHeader:
    vector_list_tag: int
    vector_list_header_size: int
    vector_list_size: int
    tri_nv_goup_num: int
    vtx_nv_goup_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 7*4


def niff2_vector_list_header_builder(data):
    vlh = Niff2VectorListHeader()
    vlh.vector_list_tag = TAG_VECTOR_LIST
    vlh.vector_list_header_size = 7*4
    vlh.vector_list_size = 7*4
    vlh.tri_nv_group_num = 0
    vlh.vtx_nv_group_num = 0
    vlh.nintendo_extension_block_size = 0
    vlh.user_extension_block_size = 0
    return vlh


def niff2_vector_list_header_writer(vlh, buf):
    buf += vlh.vector_list_tag.to_bytes(4, BYTE_ORDER)
    buf += vlh.vector_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.vector_list_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.tri_nv_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.vtx_nv_group_num.to_bytes(4, BYTE_ORDER)
    buf += vlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += vlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# St List
#
class Niff2StListHeader:
    st_list_tag: int
    st_list_header_size: int
    st_list_size: int
    st_goup_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_st_list_header_builder(data):
    stlh = Niff2StListHeader()
    stlh.st_list_tag = TAG_ST_LIST
    stlh.st_list_header_size = 6*4
    stlh.st_list_size = 6*4
    stlh.st_group_num = 0
    stlh.nintendo_extension_block_size = 0
    stlh.user_extension_block_size = 0
    return stlh


def niff2_st_list_header_writer(stlh, buf):
    buf += stlh.st_list_tag.to_bytes(4, BYTE_ORDER)
    buf += stlh.st_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += stlh.st_list_size.to_bytes(4, BYTE_ORDER)
    buf += stlh.st_group_num.to_bytes(4, BYTE_ORDER)
    buf += stlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += stlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Part List
#
class Niff2PartListHeader:
    part_list_tag: int
    part_list_header_size: int
    part_list_size: int
    part_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_part_list_header_builder(data):
    plh = Niff2PartListHeader()
    plh.part_list_tag = TAG_PART_LIST
    plh.part_list_header_size = 6*4
    plh.part_list_size = 6*4
    plh.part_num = 0
    plh.nintendo_extension_block_size = 0
    plh.user_extension_block_size = 0
    return plh


def niff2_part_list_header_writer(plh, buf):
    buf += plh.part_list_tag.to_bytes(4, BYTE_ORDER)
    buf += plh.part_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += plh.part_list_size.to_bytes(4, BYTE_ORDER)
    buf += plh.part_num.to_bytes(4, BYTE_ORDER)
    buf += plh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += plh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Mat List
#
class Niff2MatListHeader:
    mat_list_tag: int
    mat_list_header_size: int
    mat_list_size: int
    mat_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_mat_list_header_builder(data):
    mlh = Niff2MatListHeader()
    mlh.mat_list_tag = TAG_MAT_LIST
    mlh.mat_list_header_size = 6*4
    mlh.mat_list_size = 6*4
    mlh.mat_num = 0
    mlh.nintendo_extension_block_size = 0
    mlh.user_extension_block_size = 0
    return mlh


def niff2_mat_list_header_writer(mlh, buf):
    buf += mlh.mat_list_tag.to_bytes(4, BYTE_ORDER)
    buf += mlh.mat_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += mlh.mat_list_size.to_bytes(4, BYTE_ORDER)
    buf += mlh.mat_num.to_bytes(4, BYTE_ORDER)
    buf += mlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += mlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Tex List
#
class Niff2TexListHeader:
    tex_list_tag: int
    tex_list_header_size: int
    tex_list_size: int
    tex_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_tex_list_header_builder(data):
    tlh = Niff2TexListHeader()
    tlh.tex_list_tag = TAG_TEX_LIST
    tlh.tex_list_header_size = 6*4
    tlh.tex_list_size = 6*4
    tlh.tex_num = 0
    tlh.nintendo_extension_block_size = 0
    tlh.user_extension_block_size = 0
    return tlh


def niff2_tex_list_header_writer(tlh, buf):
    buf += tlh.tex_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tlh.tex_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.tex_list_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.tex_num.to_bytes(4, BYTE_ORDER)
    buf += tlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Tex Img List
#
class Niff2TexImgListHeader:
    tex_img_list_tag: int
    tex_img_list_header_size: int
    tex_img_list_size: int
    tex_img_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_tex_img_list_header_builder(data):
    tilh = Niff2TexImgListHeader()
    tilh.tex_img_list_tag = TAG_TEX_IMG_LIST
    tilh.tex_img_list_header_size = 6*4
    tilh.tex_img_list_size = 6*4
    tilh.tex_img_num = 0
    tilh.nintendo_extension_block_size = 0
    tilh.user_extension_block_size = 0
    return tilh


def niff2_tex_img_list_header_writer(tilh, buf):
    buf += tilh.tex_img_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tilh.tex_img_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tilh.tex_img_list_size.to_bytes(4, BYTE_ORDER)
    buf += tilh.tex_img_num.to_bytes(4, BYTE_ORDER)
    buf += tilh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tilh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Anim List
#
class Niff2AnimListHeader:
    anim_list_tag: int
    anim_list_header_size: int
    anim_list_size: int
    anim_group_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_anim_list_header_builder(data):
    alh = Niff2AnimListHeader()
    alh.anim_list_tag = TAG_ANIM_LIST
    alh.anim_list_header_size = 6*4
    alh.anim_list_size = 6*4
    alh.anim_group_num = 0
    alh.nintendo_extension_block_size = 0
    alh.user_extension_block_size = 0
    return alh


def niff2_anim_list_header_writer(alh, buf):
    buf += alh.anim_list_tag.to_bytes(4, BYTE_ORDER)
    buf += alh.anim_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += alh.anim_list_size.to_bytes(4, BYTE_ORDER)
    buf += alh.anim_group_num.to_bytes(4, BYTE_ORDER)
    buf += alh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += alh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Coll List
#
class Niff2CollListHeader:
    coll_list_tag: int
    coll_list_header_size: int
    coll_list_size: int
    coll_group_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_coll_list_header_builder(data):
    clh = Niff2CollListHeader()
    clh.coll_list_tag = TAG_COLL_LIST
    clh.coll_list_header_size = 6*4
    clh.coll_list_size = 6*4
    clh.coll_group_num = 0
    clh.nintendo_extension_block_size = 0
    clh.user_extension_block_size = 0
    return clh


def niff2_coll_list_header_writer(clh, buf):
    buf += clh.coll_list_tag.to_bytes(4, BYTE_ORDER)
    buf += clh.coll_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += clh.coll_list_size.to_bytes(4, BYTE_ORDER)
    buf += clh.coll_group_num.to_bytes(4, BYTE_ORDER)
    buf += clh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += clh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Switch List
#
class Niff2SwitchListHeader:
    switch_list_tag: int
    switch_list_header_size: int
    switch_list_size: int
    switch_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_switch_list_header_builder(data):
    slh = Niff2SwitchListHeader()
    slh.switch_list_tag = TAG_SWITCH_LIST
    slh.switch_list_header_size = 6*4
    slh.switch_list_size = 6*4
    slh.switch_num = 0
    slh.nintendo_extension_block_size = 0
    slh.user_extension_block_size = 0
    return slh


def niff2_switch_list_header_writer(slh, buf):
    buf += slh.switch_list_tag.to_bytes(4, BYTE_ORDER)
    buf += slh.switch_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += slh.switch_list_size.to_bytes(4, BYTE_ORDER)
    buf += slh.switch_num.to_bytes(4, BYTE_ORDER)
    buf += slh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += slh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# CiImg List
#
class Niff2CiImgListHeader:
    ci_img_list_tag: int
    ci_img_list_header_size: int
    ci_img_list_size: int
    ci_img_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_ci_img_list_header_builder(data):
    cilh = Niff2CiImgListHeader()
    cilh.ci_img_list_tag = TAG_CI_IMG_LIST
    cilh.ci_img_list_header_size = 6*4
    cilh.ci_img_list_size = 6*4
    cilh.ci_img_num = 0
    cilh.nintendo_extension_block_size = 0
    cilh.user_extension_block_size = 0
    return cilh


def niff2_ci_img_list_header_writer(cilh, buf):
    buf += cilh.ci_img_list_tag.to_bytes(4, BYTE_ORDER)
    buf += cilh.ci_img_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += cilh.ci_img_list_size.to_bytes(4, BYTE_ORDER)
    buf += cilh.ci_img_num.to_bytes(4, BYTE_ORDER)
    buf += cilh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += cilh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Color Palette List
#
class Niff2ColorPaletteListHeader:
    color_palette_list_tag: int
    color_palette_list_header_size: int
    color_palette_list_size: int
    color_palette_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_color_palette_list_header_builder(data):
    cplh = Niff2ColorPaletteListHeader()
    cplh.color_palette_list_tag = TAG_COLOR_PALETTE_LIST
    cplh.color_palette_list_header_size = 6*4
    cplh.color_palette_list_size = 6*4
    cplh.color_palette_num = 0
    cplh.nintendo_extension_block_size = 0
    cplh.user_extension_block_size = 0
    return cplh


def niff2_color_palette_list_header_writer(cplh, buf):
    buf += cplh.color_palette_list_tag.to_bytes(4, BYTE_ORDER)
    buf += cplh.color_palette_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += cplh.color_palette_list_size.to_bytes(4, BYTE_ORDER)
    buf += cplh.color_palette_num.to_bytes(4, BYTE_ORDER)
    buf += cplh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += cplh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Envelope List
#
class Niff2EnvelopeListHeader:
    envelope_list_tag: int
    envelope_list_header_size: int
    envelope_list_size: int
    envelope_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_envelope_list_header_builder(data):
    elh = Niff2EnvelopeListHeader()
    elh.envelope_list_tag = TAG_ENVELOPE_LIST
    elh.envelope_list_header_size = 6*4
    elh.envelope_list_size = 6*4
    elh.envelope_num = 0
    elh.nintendo_extension_block_size = 0
    elh.user_extension_block_size = 0
    return elh


def niff2_envelope_list_header_writer(elh, buf):
    buf += elh.envelope_list_tag.to_bytes(4, BYTE_ORDER)
    buf += elh.envelope_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += elh.envelope_list_size.to_bytes(4, BYTE_ORDER)
    buf += elh.envelope_num.to_bytes(4, BYTE_ORDER)
    buf += elh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += elh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Cluster List
#
class Niff2ClusterListHeader:
    cluster_list_tag: int
    cluster_list_header_size: int
    cluster_list_size: int
    cluster_shape_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_cluster_list_header_builder(data):
    clh = Niff2ClusterListHeader()
    clh.cluster_list_tag = TAG_CLUSTER_LIST
    clh.cluster_list_header_size = 6*4
    clh.cluster_list_size = 6*4
    clh.cluster_shape_num = 0
    clh.nintendo_extension_block_size = 0
    clh.user_extension_block_size = 0
    return clh


def niff2_cluster_list_header_writer(clh, buf):
    buf += clh.cluster_list_tag.to_bytes(4, BYTE_ORDER)
    buf += clh.cluster_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += clh.cluster_list_size.to_bytes(4, BYTE_ORDER)
    buf += clh.cluster_shape_num.to_bytes(4, BYTE_ORDER)
    buf += clh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += clh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Weight List
#
class Niff2WeightListHeader:
    weight_list_tag: int
    weight_list_header_size: int
    weight_list_size: int
    weight_group_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_weight_list_header_builder(data):
    wlh = Niff2WeightListHeader()
    wlh.weight_list_tag = TAG_WEIGHT_LIST
    wlh.weight_list_header_size = 6*4
    wlh.weight_list_size = 6*4
    wlh.weight_group_num = 0
    wlh.nintendo_extension_block_size = 0
    wlh.user_extension_block_size = 0
    return wlh


def niff2_weight_list_header_writer(wlh, buf):
    buf += wlh.weight_list_tag.to_bytes(4, BYTE_ORDER)
    buf += wlh.weight_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += wlh.weight_list_size.to_bytes(4, BYTE_ORDER)
    buf += wlh.weight_group_num.to_bytes(4, BYTE_ORDER)
    buf += wlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += wlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Chain Root List
#
class Niff2ChainRootListHeader:
    chain_root_list_tag: int
    chain_root_list_header_size: int
    chain_root_list_size: int
    chain_root_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_chain_root_list_header_builder(data):
    crlh = Niff2ChainRootListHeader()
    crlh.chain_root_list_tag = TAG_CHAIN_ROOT_LIST
    crlh.chain_root_list_header_size = 6*4
    crlh.chain_root_list_size = 6*4
    crlh.chain_root_num = 0
    crlh.nintendo_extension_block_size = 0
    crlh.user_extension_block_size = 0
    return crlh


def niff2_chain_root_list_header_writer(crlh, buf):
    buf += crlh.chain_root_list_tag.to_bytes(4, BYTE_ORDER)
    buf += crlh.chain_root_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += crlh.chain_root_list_size.to_bytes(4, BYTE_ORDER)
    buf += crlh.chain_root_num.to_bytes(4, BYTE_ORDER)
    buf += crlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += crlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Joint List
#
class Niff2JointListHeader:
    joint_list_tag: int
    joint_list_header_size: int
    joint_list_size: int
    joint_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_joint_list_header_builder(data):
    jlh = Niff2JointListHeader()
    jlh.joint_list_tag = TAG_JOINT_LIST
    jlh.joint_list_header_size = 6*4
    jlh.joint_list_size = 6*4
    jlh.joint_num = 0
    jlh.nintendo_extension_block_size = 0
    jlh.user_extension_block_size = 0
    return jlh


def niff2_joint_list_header_writer(jlh, buf):
    buf += jlh.joint_list_tag.to_bytes(4, BYTE_ORDER)
    buf += jlh.joint_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += jlh.joint_list_size.to_bytes(4, BYTE_ORDER)
    buf += jlh.joint_num.to_bytes(4, BYTE_ORDER)
    buf += jlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += jlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Effector List
#
class Niff2EffectorListHeader:
    effector_list_tag: int
    effector_list_header_size: int
    effector_list_size: int
    effector_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_effector_list_header_builder(data):
    elh = Niff2EffectorListHeader()
    elh.effector_list_tag = TAG_EFFECTOR_LIST
    elh.effector_list_header_size = 6*4
    elh.effector_list_size = 6*4
    elh.effector_num = 0
    elh.nintendo_extension_block_size = 0
    elh.user_extension_block_size = 0
    return elh


def niff2_effector_list_header_writer(elh, buf):
    buf += elh.effector_list_tag.to_bytes(4, BYTE_ORDER)
    buf += elh.effector_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += elh.effector_list_size.to_bytes(4, BYTE_ORDER)
    buf += elh.effector_num.to_bytes(4, BYTE_ORDER)
    buf += elh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += elh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# External Name List
#
class Niff2ExternalNameListHeader:
    external_name_list_tag: int
    external_name_list_header_size: int
    external_name_list_size: int
    external_name_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_external_name_list_header_builder(data):
    enlh = Niff2ExternalNameListHeader()
    enlh.external_name_list_tag = TAG_EXTERNAL_NAME_LIST
    enlh.external_name_list_header_size = 6*4
    enlh.external_name_list_size = 6*4
    enlh.external_name_num = 0
    enlh.nintendo_extension_block_size = 0
    enlh.user_extension_block_size = 0
    return enlh


def niff2_external_name_list_header_writer(enlh, buf):
    buf += enlh.external_name_list_tag.to_bytes(4, BYTE_ORDER)
    buf += enlh.external_name_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += enlh.external_name_list_size.to_bytes(4, BYTE_ORDER)
    buf += enlh.external_name_num.to_bytes(4, BYTE_ORDER)
    buf += enlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += enlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Writer entry point
#
def write_niff2(data, filepath):
    print("running write_niff2...")

    names = []
    scene_name = niff2_name_node_builder(
        len(names), bpy.path.display_name_from_filepath(filepath))
    names.append(scene_name)

    objs = []
    for obj_index, mesh in zip(range(len(data.meshes)), data.meshes):
        obj_name = niff2_name_node_builder(len(names), mesh.name)
        names.append(obj_name)
        obj = niff2_obj_node_builder(obj_index, obj_name.index(), mesh)
        objs.append(obj)

    shapes = []
    for shape_index, mesh in zip(range(len(data.meshes)), data.meshes):
        shape_name = niff2_name_node_builder(len(names), mesh.name)
        names.append(shape_name)
        shape = niff2_shape_node_builder(shape_index, shape_name.index(), mesh)
        shapes.append(shape)

    scene_header = niff2_scene_header_builder(scene_name.index(), objs)
    env_list_header = niff2_env_list_header_builder(data)
    cam_list_header = niff2_cam_list_header_builder(data)
    light_list_header = niff2_light_list_header_builder(data)
    obj_list_header = niff2_obj_list_header_builder(objs)
    shape_list_header = niff2_shape_list_header_builder(shapes)
    vtx_list_header = niff2_vtx_list_header_builder(data)
    tri_list_header = niff2_tri_list_header_builder(data)
    color_list_header = niff2_color_list_header_builder(data)
    vector_list_header = niff2_vector_list_header_builder(data)
    st_list_header = niff2_st_list_header_builder(data)
    part_list_header = niff2_part_list_header_builder(data)
    mat_list_header = niff2_mat_list_header_builder(data)
    tex_list_header = niff2_tex_list_header_builder(data)
    tex_img_list_header = niff2_tex_img_list_header_builder(data)
    anim_list_header = niff2_anim_list_header_builder(data)
    coll_list_header = niff2_coll_list_header_builder(data)
    switch_list_header = niff2_switch_list_header_builder(data)
    name_list_header = niff2_name_list_header_builder(names)
    ci_img_list_header = niff2_ci_img_list_header_builder(data)
    color_palette_list_header = niff2_color_palette_list_header_builder(data)
    envelope_list_header = niff2_envelope_list_header_builder(data)
    cluster_list_header = niff2_cluster_list_header_builder(data)
    weight_list_header = niff2_weight_list_header_builder(data)
    chain_root_list_header = niff2_chain_root_list_header_builder(data)
    joint_list_header = niff2_joint_list_header_builder(data)
    effector_list_header = niff2_effector_list_header_builder(data)
    external_name_list_header = niff2_external_name_list_header_builder(data)

    file_size = Niff2FileHeader.num_bytes() \
        + scene_header.num_bytes() \
        + env_list_header.num_bytes() \
        + cam_list_header.num_bytes() \
        + light_list_header.num_bytes() \
        + obj_list_header.num_bytes() \
        + shape_list_header.num_bytes() \
        + vtx_list_header.num_bytes() \
        + tri_list_header.num_bytes() \
        + color_list_header.num_bytes() \
        + vector_list_header.num_bytes() \
        + st_list_header.num_bytes() \
        + part_list_header.num_bytes() \
        + mat_list_header.num_bytes() \
        + tex_list_header.num_bytes() \
        + tex_img_list_header.num_bytes() \
        + anim_list_header.num_bytes() \
        + coll_list_header.num_bytes() \
        + switch_list_header.num_bytes() \
        + name_list_header.num_bytes() \
        + ci_img_list_header.num_bytes() \
        + color_palette_list_header.num_bytes() \
        + envelope_list_header.num_bytes() \
        + cluster_list_header.num_bytes() \
        + weight_list_header.num_bytes() \
        + chain_root_list_header.num_bytes() \
        + joint_list_header.num_bytes() \
        + effector_list_header.num_bytes() \
        + external_name_list_header.num_bytes()

    fh = niff2_file_header_builder(file_size)
    fh.scene_list_num_byte = scene_header.num_bytes()
    fh.env_list_num_byte = env_list_header.num_bytes()
    fh.cam_list_num_byte = cam_list_header.num_bytes()
    fh.light_list_num_byte = light_list_header.num_bytes()
    fh.obj_list_num_byte = obj_list_header.num_bytes()
    fh.shape_list_num_byte = shape_list_header.num_bytes()
    fh.vtx_list_num_byte = vtx_list_header.num_bytes()
    fh.tri_list_num_byte = tri_list_header.num_bytes()
    fh.color_list_num_byte = color_list_header.num_bytes()
    fh.vector_list_num_byte = vector_list_header.num_bytes()
    fh.st_list_num_byte = st_list_header.num_bytes()
    fh.part_list_num_byte = part_list_header.num_bytes()
    fh.mat_list_num_byte = mat_list_header.num_bytes()
    fh.tex_list_num_byte = tex_list_header.num_bytes()
    fh.tex_img_list_num_byte = tex_img_list_header.num_bytes()
    fh.anim_list_num_byte = anim_list_header.num_bytes()
    fh.coll_list_num_byte = coll_list_header.num_bytes()
    fh.switch_list_num_byte = switch_list_header.num_bytes()
    fh.name_list_num_byte = name_list_header.num_bytes()
    fh.ci_img_list_num_byte = ci_img_list_header.num_bytes()
    fh.color_palette_list_num_byte = color_palette_list_header.num_bytes()
    fh.envelope_list_num_byte = envelope_list_header.num_bytes()
    fh.cluster_list_num_byte = cluster_list_header.num_bytes()
    fh.weight_list_num_byte = weight_list_header.num_bytes()
    fh.chain_root_list_num_byte = chain_root_list_header.num_bytes()
    fh.joint_list_num_byte = joint_list_header.num_bytes()
    fh.effector_list_num_byte = effector_list_header.num_bytes()
    fh.external_name_list_num_byte = external_name_list_header.num_bytes()

    buf = bytearray()
    niff2_file_header_writer(fh, buf)
    niff2_scene_header_writer(scene_header, buf)
    niff2_env_list_header_writer(env_list_header, buf)
    niff2_cam_list_header_writer(cam_list_header, buf)
    niff2_light_list_header_writer(light_list_header, buf)

    niff2_obj_list_header_writer(obj_list_header, objs, buf)
    for obj in objs:
        niff2_obj_node_writer(obj, buf)

    niff2_shape_list_header_writer(shape_list_header, shapes, buf)
    for shape in shapes:
        niff2_shape_node_writer(shape, buf)

    niff2_vtx_list_header_writer(vtx_list_header, buf)
    niff2_tri_list_header_writer(tri_list_header, buf)
    niff2_color_list_header_writer(color_list_header, buf)
    niff2_vector_list_header_writer(vector_list_header, buf)
    niff2_st_list_header_writer(st_list_header, buf)
    niff2_part_list_header_writer(part_list_header, buf)
    niff2_mat_list_header_writer(mat_list_header, buf)
    niff2_tex_list_header_writer(tex_list_header, buf)
    niff2_tex_img_list_header_writer(tex_img_list_header, buf)
    niff2_anim_list_header_writer(anim_list_header, buf)
    niff2_coll_list_header_writer(coll_list_header, buf)
    niff2_switch_list_header_writer(switch_list_header, buf)

    niff2_name_list_header_writer(name_list_header, names, buf)
    for name in names:
        niff2_name_node_writer(name, buf)

    niff2_ci_img_list_header_writer(ci_img_list_header, buf)
    niff2_color_palette_list_header_writer(color_palette_list_header, buf)
    niff2_envelope_list_header_writer(envelope_list_header, buf)
    niff2_cluster_list_header_writer(cluster_list_header, buf)
    niff2_weight_list_header_writer(weight_list_header, buf)
    niff2_chain_root_list_header_writer(chain_root_list_header, buf)
    niff2_joint_list_header_writer(joint_list_header, buf)
    niff2_effector_list_header_writer(effector_list_header, buf)
    niff2_external_name_list_header_writer(external_name_list_header, buf)

    f = open(filepath, 'wb')
    f.write(buf)
    f.close()

    return {'FINISHED'}


class N64Niff2Export(Operator, ExportHelper):
    """Export to N64 NIFF2 format"""

    # important since its how bpy.ops.export.to_n64_niff2 is constructed
    bl_idname = "export.to_n64_niff2"
    bl_label = "Export to N64 NIFF2"

    # ExportHelper mixin class uses this
    filename_ext = ".nif"

    filter_glob: StringProperty(
        default="*.nif",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_niff2(bpy.data, self.filepath)
