"""Exporter operator."""

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import (Mesh, Operator)
from .niff2_anim import (niff2_anim_list_header_builder, niff2_anim_list_header_writer,
                         niff2_anim_group_builder, niff2_anim_group_writer,
                         niff2_anim_node_builder)
from .niff2_camera import (niff2_cam_list_header_builder,
                           niff2_cam_list_header_writer)
from .niff2_color import (niff2_color_list_header_builder, niff2_color_list_header_writer,
                          niff2_tri_color_group_node_builder, niff2_tri_color_group_node_writer,
                          niff2_vtx_color_group_node_builder, niff2_vtx_color_group_node_writer)
from .niff2_header import (Niff2FileHeader,
                           niff2_file_header_builder, niff2_file_header_writer)
from .niff2_mat import (niff2_mat_list_header_builder, niff2_mat_list_header_writer,
                        niff2_mat_node_builder, niff2_mat_node_writer)
from .niff2_name import (niff2_name_list_header_builder, niff2_name_list_header_writer,
                         niff2_name_node_builder, niff2_name_node_writer)
from .niff2_obj import (niff2_obj_list_header_builder,
                        niff2_obj_list_header_writer, niff2_obj_node_builder, niff2_obj_node_writer)
from .niff2_part import (niff2_part_list_header_builder, niff2_part_list_header_writer,
                         niff2_part_node_writer)
from .niff2_shape import (niff2_shape_list_header_builder, niff2_shape_list_header_writer,
                          niff2_shape_node_builder, niff2_shape_node_writer)
from .niff2_st import (niff2_st_list_header_builder, niff2_st_list_header_writer,
                       niff2_st_group_node_builder, niff2_st_group_node_writer)
from .niff2_tri import (niff2_tri_list_header_builder, niff2_tri_list_header_writer,
                        niff2_tri_group_node_builder, niff2_tri_group_node_writer)
from .niff2_vector import (niff2_vector_list_header_builder, niff2_vector_list_header_writer,
                           niff2_tri_nv_group_node_builder, niff2_tri_nv_group_node_writer,
                           niff2_vtx_nv_group_node_builder, niff2_vtx_nv_group_node_writer)
from .niff2_vtx import (niff2_vtx_list_header_builder, niff2_vtx_list_header_writer,
                        niff2_vtx_group_node_builder, niff2_vtx_group_node_writer)

#
# Consts
#
TAG_SCENE_HEADER = 0x00010000
TAG_ENV_LIST = 0x00100000
TAG_LIGHT_LIST = 0x000f0000
TAG_TEX_LIST = 0x000b0000
TAG_TEX_IMG_LIST = 0x00120000
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


def niff2_env_list_header_builder():
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


def niff2_light_list_header_builder():
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


def niff2_tex_list_header_builder():
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


def niff2_tex_img_list_header_builder():
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


def niff2_coll_list_header_builder():
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


def niff2_switch_list_header_builder():
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


def niff2_ci_img_list_header_builder():
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


def niff2_color_palette_list_header_builder():
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


def niff2_envelope_list_header_builder():
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


def niff2_cluster_list_header_builder():
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


def niff2_weight_list_header_builder():
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


def niff2_chain_root_list_header_builder():
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


def niff2_joint_list_header_builder():
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


def niff2_effector_list_header_builder():
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


def niff2_external_name_list_header_builder():
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

    mesh_objs = list(
        filter(lambda obj: isinstance(obj.data, Mesh), data.objects))

    names = []
    scene_name = niff2_name_node_builder(
        len(names), bpy.path.display_name_from_filepath(filepath))
    names.append(scene_name)

    # Niff2 Material: Create a single default material
    materials = []
    default_material_name = niff2_name_node_builder(
        len(names), "default_material.mat")
    names.append(default_material_name)
    default_material = niff2_mat_node_builder(0, default_material_name.index())
    materials.append(default_material)

    # NIFF2 VtxGroup <-> Blender Mesh (1 vtx_group per mesh)
    vtx_groups = []
    for vtx_group_index, obj in zip(range(len(mesh_objs)), mesh_objs):
        mesh = obj.data
        vtx_group_name = niff2_name_node_builder(len(names), mesh.name+".vtx")
        names.append(vtx_group_name)
        vtx_floats = []
        for vtx in mesh.vertices:
            vtx_floats += list(vtx.co)
        vtx_group = niff2_vtx_group_node_builder(
            vtx_group_index, vtx_group_name.index(), vtx_floats)
        vtx_groups.append(vtx_group)

    # Niff2 ColorGroup: Create a single default color
    tri_color_groups = []
    vtx_color_groups = []
    default_color = [0.8, 0.8, 0.8, 1.0]  # rgba
    default_tri_color_group = niff2_tri_color_group_node_builder(
        0, default_color)
    default_vtx_color_group = niff2_vtx_color_group_node_builder(
        0, default_color)
    tri_color_groups.append(default_tri_color_group)
    vtx_color_groups.append(default_vtx_color_group)

    # Niff2 ColorGroup: Create mesh vertex color group.
    # (!) Make sure to have the same number of tri_color_groups & vtx_color_group.
    #     This prevents nifftools/checknb2.exe from crashing.
    # (!) Do not support smooth groups: 1 color per vertex!
    #     Indices are all aligned both for vertex coords and vertex colors.
    for vtx_color_group_index, mesh in zip(range(len(data.meshes)), data.meshes):
        mesh.calc_loop_triangles()
        vtx_colors = [float]*len(mesh.vertices)*4

        mesh.calc_loop_triangles()
        for tri in mesh.loop_triangles:
            for i in range(3):
                vtx_index = tri.vertices[i]
                loop_index = tri.loops[i]
                color = mesh.vertex_colors[0].data[loop_index].color
                vtx_colors[(vtx_index*4)+0] = color[0]
                vtx_colors[(vtx_index*4)+1] = color[1]
                vtx_colors[(vtx_index*4)+2] = color[2]
                vtx_colors[(vtx_index*4)+3] = color[3]

        tri_color_group = niff2_tri_color_group_node_builder(
            1+vtx_color_group_index, default_color)
        tri_color_groups.append(tri_color_group)

        vtx_color_group = niff2_vtx_color_group_node_builder(
            1+vtx_color_group_index, vtx_colors)
        vtx_color_groups.append(vtx_color_group)

    # Niff2 VectorGroup: Create a single default normal vector
    tri_nv_groups = []
    vtx_nv_groups = []
    default_nv = [0.0, 1.0, 0.0]  # up
    default_tri_nv_group = niff2_tri_nv_group_node_builder(
        0, default_nv)
    default_vtx_nv_group = niff2_vtx_nv_group_node_builder(
        0, default_nv)
    tri_nv_groups.append(default_tri_nv_group)
    vtx_nv_groups.append(default_vtx_nv_group)

    # Niff2 StGroup: Create a single default texture coordinates
    st_groups = []
    default_st = [0.5, 0.5]  # center
    default_st_group = niff2_st_group_node_builder(0, default_st)
    st_groups.append(default_st_group)

    # NIFF2 TriGroup <-> Blender Mesh (1 tri_group per mesh)
    tri_groups = []
    for tri_group_index, mesh, vtx_group in zip(range(len(data.meshes)), data.meshes, vtx_groups):
        tri_group_name = niff2_name_node_builder(len(names), mesh.name+".tri")
        names.append(tri_group_name)
        vtx_indices = []
        mesh.calc_loop_triangles()
        for tri in mesh.loop_triangles:
            vtx_indices += list(tri.vertices)
        tri_group = niff2_tri_group_node_builder(
            tri_group_index, tri_group_name.index(), vtx_group.index(), vtx_indices)
        tri_groups.append(tri_group)

    # NIFF2 Part: Not supported
    parts = []

    # NIFF2 Shape <-> Blender Mesh
    shapes = []
    for shape_index, mesh, tri_group in zip(range(len(data.meshes)), data.meshes, tri_groups):
        shape_name = niff2_name_node_builder(len(names), mesh.name+".shape")
        names.append(shape_name)
        shape = niff2_shape_node_builder(
            shape_index, shape_name.index(), tri_group.index(), default_material.index())
        shapes.append(shape)

    # NIFF2 Anim: 1 anim per object
    anim_groups = []
    for anim_index, obj, in zip(range(len(mesh_objs)), mesh_objs):
        anim_name = niff2_name_node_builder(len(names), obj.name+".anim")
        names.append(anim_name)
        anim_node = niff2_anim_node_builder(
            obj.location, obj.rotation_euler, obj.scale)
        anim_group = niff2_anim_group_builder(
            anim_index, anim_name.index(), anim_node)
        anim_groups.append(anim_group)

    # NIFF2 Obj: Blender Object
    objs = []
    for obj_index, obj, shape, anim_group in zip(range(len(mesh_objs)), mesh_objs, shapes, anim_groups):
        obj_name = niff2_name_node_builder(len(names), obj.name+".obj")
        names.append(obj_name)
        obj = niff2_obj_node_builder(
            obj_index, obj_name.index(), shape.index(), default_material.index(), anim_group.index())
        objs.append(obj)

    scene_header = niff2_scene_header_builder(scene_name.index(), objs)
    env_list_header = niff2_env_list_header_builder()
    cam_list_header = niff2_cam_list_header_builder()
    light_list_header = niff2_light_list_header_builder()
    obj_list_header = niff2_obj_list_header_builder(objs)
    shape_list_header = niff2_shape_list_header_builder(shapes)
    vtx_list_header = niff2_vtx_list_header_builder(vtx_groups)
    tri_list_header = niff2_tri_list_header_builder(tri_groups)
    color_list_header = niff2_color_list_header_builder(
        tri_color_groups, vtx_color_groups)
    vector_list_header = niff2_vector_list_header_builder(
        tri_nv_groups, vtx_nv_groups)
    st_list_header = niff2_st_list_header_builder(st_groups)
    part_list_header = niff2_part_list_header_builder(parts)
    mat_list_header = niff2_mat_list_header_builder(materials)
    tex_list_header = niff2_tex_list_header_builder()
    tex_img_list_header = niff2_tex_img_list_header_builder()
    anim_list_header = niff2_anim_list_header_builder(anim_groups)
    coll_list_header = niff2_coll_list_header_builder()
    switch_list_header = niff2_switch_list_header_builder()
    name_list_header = niff2_name_list_header_builder(names)
    ci_img_list_header = niff2_ci_img_list_header_builder()
    color_palette_list_header = niff2_color_palette_list_header_builder()
    envelope_list_header = niff2_envelope_list_header_builder()
    cluster_list_header = niff2_cluster_list_header_builder()
    weight_list_header = niff2_weight_list_header_builder()
    chain_root_list_header = niff2_chain_root_list_header_builder()
    joint_list_header = niff2_joint_list_header_builder()
    effector_list_header = niff2_effector_list_header_builder()
    external_name_list_header = niff2_external_name_list_header_builder()

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

    niff2_vtx_list_header_writer(vtx_list_header, vtx_groups, buf)
    for vtx_group in vtx_groups:
        niff2_vtx_group_node_writer(vtx_group, buf)

    niff2_tri_list_header_writer(tri_list_header, tri_groups, buf)
    for tri_group in tri_groups:
        niff2_tri_group_node_writer(tri_group, buf)

    niff2_color_list_header_writer(
        color_list_header, tri_color_groups, vtx_color_groups, buf)
    for tri_color_group in tri_color_groups:
        niff2_tri_color_group_node_writer(tri_color_group, buf)
    for vtx_color_group in vtx_color_groups:
        niff2_vtx_color_group_node_writer(vtx_color_group, buf)

    niff2_vector_list_header_writer(
        vector_list_header, tri_nv_groups, vtx_nv_groups, buf)
    for tri_nv_group in tri_nv_groups:
        niff2_tri_nv_group_node_writer(tri_nv_group, buf)
    for vtx_nv_group in vtx_nv_groups:
        niff2_vtx_nv_group_node_writer(vtx_nv_group, buf)

    niff2_st_list_header_writer(st_list_header, st_groups, buf)
    for st_group in st_groups:
        niff2_st_group_node_writer(st_group, buf)

    niff2_part_list_header_writer(part_list_header, parts, buf)
    for part in parts:
        niff2_part_node_writer(part, buf)

    niff2_mat_list_header_writer(mat_list_header, materials, buf)
    for mat in materials:
        niff2_mat_node_writer(mat, buf)

    niff2_tex_list_header_writer(tex_list_header, buf)
    niff2_tex_img_list_header_writer(tex_img_list_header, buf)

    niff2_anim_list_header_writer(anim_list_header, anim_groups, buf)
    for anim_group in anim_groups:
        niff2_anim_group_writer(anim_group, buf)

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
    """Blender operator to export to N64 NIFF2 format"""

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

    def execute(self, _):
        return write_niff2(bpy.data, self.filepath)
