"""NIFF2 File Header."""

#
# Consts
#
MAKER_CODE = 0xFF
TOOL_CODE = 0x00
NIFF_MAJOR_VERSION = 0x02
NIFF_MINOR_VERSION = 0x00

TAG_HEADER = 0x00000000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# File Header
#
class Niff2FileHeader:
    def __init__(self, file_size):
        self.version = MAKER_CODE << 24 | TOOL_CODE << 16 | NIFF_MAJOR_VERSION << 8 | NIFF_MINOR_VERSION
        self.file_size = file_size
        self.header_tag = TAG_HEADER
        self.file_header_num_byte = (25*4) + (9*4)
        self.scene_list_num_byte = 0
        self.env_list_num_byte = 0
        self.cam_list_num_byte = 0
        self.light_list_num_byte = 0
        self.obj_list_num_byte = 0
        self.shape_list_num_byte = 0
        self.vtx_list_num_byte = 0
        self.color_list_num_byte = 0
        self.vector_list_num_byte = 0
        self.st_list_num_byte = 0
        self.tri_list_num_byte = 0
        self.part_list_num_byte = 0
        self.mat_list_num_byte = 0
        self.tex_list_num_byte = 0
        self.tex_img_list_num_byte = 0
        self.anim_list_num_byte = 0
        self.coll_list_num_byte = 0
        self.switch_list_num_byte = 0
        self.name_list_num_byte = 0
        self.nintendo_extension_block_size = 9*4
        self.user_extension_block_size = 0
        self.ci_img_list_num_byte = 0
        self.color_palette_list_num_byte = 0
        self.envelope_list_num_byte = 0
        self.cluster_list_num_byte = 0
        self.weight_list_num_byte = 0
        self.chain_root_list_num_byte = 0
        self.joint_list_num_byte = 0
        self.effector_list_num_byte = 0
        self.external_name_list_num_byte = 0

    @staticmethod
    def num_bytes():
        return (25*4) + (9*4)


def niff2_file_header_builder(file_size):
    return Niff2FileHeader(file_size)


def niff2_file_header_writer(file_header, buf):
    buf += file_header.version.to_bytes(4, BYTE_ORDER)
    buf += file_header.file_size.to_bytes(4, BYTE_ORDER)
    buf += file_header.header_tag.to_bytes(4, BYTE_ORDER)
    buf += file_header.file_header_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.scene_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.env_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.cam_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.light_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.obj_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.shape_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.vtx_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.color_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.vector_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.st_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.tri_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.part_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.mat_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.tex_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.tex_img_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.anim_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.coll_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.switch_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.name_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += file_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += file_header.ci_img_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.color_palette_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.envelope_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.cluster_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.weight_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.chain_root_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.joint_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.effector_list_num_byte.to_bytes(4, BYTE_ORDER)
    buf += file_header.external_name_list_num_byte.to_bytes(4, BYTE_ORDER)
    return buf
