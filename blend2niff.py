import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator

#
# Consts
#
MAKER_CODE = 0x00
TOOL_CODE = 0x00
NIFF_MAJOR_VERSION = 0x01
NIFF_MINOR_VERSION = 0x00

TAG_HEADER = 0x00000000
TAG_SCENE_HEADER = 0x00010000
TAG_ENV_LIST = 0x00100000
TAG_CAM_LIST = 0x000e0000
TAG_LIGHT_LIST = 0x000f0000
TAG_OBJ_LIST = 0x00020000
TAG_SHAPE_LIST = 0x00030000
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
TAG_NAME_LIST = 0x00110000

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

    @staticmethod
    def num_bytes():
        return 25*4


def niff2_file_header_builder(file_size):
    fh = Niff2FileHeader()
    fh.version = MAKER_CODE << 24 | TOOL_CODE << 16 | NIFF_MAJOR_VERSION << 8 | NIFF_MINOR_VERSION
    fh.file_size = file_size
    fh.header_tag = TAG_HEADER
    fh.file_header_num_byte = 25*4
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
    fh.nintendo_extension_block_size = 0
    fh.user_extension_block_size = 0
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

    def num_bytes(self):
        return 11*4 + self.scene_obj_link_num*4


def niff2_scene_header_builder(data):
    obj_count = len(data.meshes)

    sh = Niff2SceneHeader()
    sh.scene_header_tag = TAG_SCENE_HEADER
    sh.scene_cfg = SCENE_CFG_VIDEO_NTSC
    sh.scene_name_index = BAD_INDEX
    sh.scene_obj_link_num = obj_count
    sh.scene_env_link_num = 0
    sh.scene_cam_link_num = 0
    sh.scene_light_link_num = 0
    sh.nintendo_extension_block_size = 0
    sh.user_extension_block_size = 0

    sh.scene_header_size = 11*4
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
# Obj List
#
class Niff2ObjListHeader:
    obj_list_tag: int
    obj_list_header_size: int
    obj_list_size: int
    obj_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_obj_list_header_builder(data):
    olh = Niff2ObjListHeader()
    olh.obj_list_tag = TAG_OBJ_LIST
    olh.obj_list_header_size = 6*4
    olh.obj_list_size = 6*4
    olh.obj_num = 0
    olh.nintendo_extension_block_size = 0
    olh.user_extension_block_size = 0
    return olh


def niff2_obj_list_header_writer(olh, buf):
    buf += olh.obj_list_tag.to_bytes(4, BYTE_ORDER)
    buf += olh.obj_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += olh.obj_list_size.to_bytes(4, BYTE_ORDER)
    buf += olh.obj_num.to_bytes(4, BYTE_ORDER)
    buf += olh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += olh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Shape List
#
class Niff2ShapeListHeader:
    shape_list_tag: int
    shape_list_header_size: int
    shape_list_size: int
    shape_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_shape_list_header_builder(data):
    slh = Niff2ShapeListHeader()
    slh.shape_list_tag = TAG_SHAPE_LIST
    slh.shape_list_header_size = 6*4
    slh.shape_list_size = 6*4
    slh.shape_num = 0
    slh.nintendo_extension_block_size = 0
    slh.user_extension_block_size = 0
    return slh


def niff2_shape_list_header_writer(slh, buf):
    buf += slh.shape_list_tag.to_bytes(4, BYTE_ORDER)
    buf += slh.shape_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += slh.shape_list_size.to_bytes(4, BYTE_ORDER)
    buf += slh.shape_num.to_bytes(4, BYTE_ORDER)
    buf += slh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += slh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
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
# Name List
#
class Niff2NameListHeader:
    name_list_tag: int
    name_list_header_size: int
    name_list_size: int
    name_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    @staticmethod
    def num_bytes():
        return 6*4


def niff2_name_list_header_builder(data):
    nlh = Niff2NameListHeader()
    nlh.name_list_tag = TAG_NAME_LIST
    nlh.name_list_header_size = 6*4
    nlh.name_list_size = 6*4
    nlh.name_num = 0
    nlh.nintendo_extension_block_size = 0
    nlh.user_extension_block_size = 0
    return nlh


def niff2_name_list_header_writer(nlh, buf):
    buf += nlh.name_list_tag.to_bytes(4, BYTE_ORDER)
    buf += nlh.name_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += nlh.name_list_size.to_bytes(4, BYTE_ORDER)
    buf += nlh.name_num.to_bytes(4, BYTE_ORDER)
    buf += nlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += nlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf


#
# Writer entry point
#
def write_niff2(data, filepath):
    print("running write_niff2...")

    scene_header = niff2_scene_header_builder(data)
    env_list_header = niff2_env_list_header_builder(data)
    cam_list_header = niff2_cam_list_header_builder(data)
    light_list_header = niff2_light_list_header_builder(data)
    obj_list_header = niff2_obj_list_header_builder(data)
    shape_list_header = niff2_shape_list_header_builder(data)
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
    name_list_header = niff2_name_list_header_builder(data)

    file_size = 100 \
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
        + name_list_header.num_bytes()

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

    buf = bytearray()
    niff2_file_header_writer(fh, buf)
    niff2_scene_header_writer(scene_header, buf)
    niff2_env_list_header_writer(env_list_header, buf)
    niff2_cam_list_header_writer(cam_list_header, buf)
    niff2_light_list_header_writer(light_list_header, buf)
    niff2_obj_list_header_writer(obj_list_header, buf)
    niff2_shape_list_header_writer(shape_list_header, buf)
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
    niff2_name_list_header_writer(name_list_header, buf)

    f = open(filepath, 'wb')
    f.write(buf)
    f.close()

    return {'FINISHED'}


bl_info = {
    "name": "N64 NIFF2 Exporter",
    "description": "Export to N64 NIFF2 format",
    "author": "https://github.com/1r3n33",
    "category": "Import-Export",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "File > Export > N64 NIFF2 (.nif)"
}


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


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(N64Niff2Export.bl_idname, text="N64 NIFF2 (.nif)")


def register():
    bpy.utils.register_class(N64Niff2Export)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(N64Niff2Export)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export.to_n64_niff2('INVOKE_DEFAULT')
