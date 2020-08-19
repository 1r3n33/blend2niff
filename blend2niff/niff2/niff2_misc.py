#
# Consts
#
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

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


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
