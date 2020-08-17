"""NIFF2 Texture Configuration."""

TAG_TEX_LIST = 0x000b0000
TAG_TEX = 0x000b0100

TEX_FORM_I = 0x00000000
TEX_FORM_IA = 0x00000001
TEX_FORM_CI = 0x00000002
TEX_FORM_YUV = 0x00000003
TEX_FORM_RGB = 0x00000004
TEX_FORM_RGBA = 0x00000005
TEX_DEPTH_4 = 0x00000000
TEX_DEPTH_8 = 0x00000100
TEX_DEPTH_16 = 0x00000200
TEX_DEPTH_32 = 0x00000400

TEX_WRAP_S = 0x00000000
TEX_CLAMP_S = 0x00000001
TEX_MIRROR_S = 0x00000002

TEX_WRAP_T = 0x00000000
TEX_CLAMP_T = 0x00000100
TEX_MIRROR_T = 0x00000200

TEX_ANIM_OFF = 0x00000000
TEX_ANIM_FLIPBOOK = 0x00000001
TEX_ANIM_FLIPBOOK_KEY = 0x00000002
TEX_ANIM_SCROLL_OFFSET = 0x00000010
TEX_ANIM_SCROLL_OFFSET_KEY = 0x00000020
TEX_ANIM_SCROLL_SCALE = 0x00000100
TEX_ANIM_SCROLL_SCALE_KEY = 0x00000200

NIFF2_TEX_FILTER_POINT = 0x00000000
NIFF2_TEX_FILTER_BILERP = 0x00000001
NIFF2_TEX_FILTER_AVERAGE = 0x00000002

NIFF2_NO_PERSPECTIVE_CORRECTION = 0x00000000
NIFF2_PERSPECTIVE_CORRECTION = 0x00000001

NIFF2_NO_MIPMAP = 0x00000000

NIFF2_NO_USE_COLOR_PALETTE = 0x00000000
NIFF2_USE_COLOR_PALETTE = 0x00000001

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


class Niff2TexListHeader:
    def __init__(self, tex_num, tex_list_size):
        self.tex_list_tag = TAG_TEX_LIST
        self.tex_list_header_size = (6*4) + (tex_num*4)
        self.tex_list_size = (6*4) + (tex_num*4) + tex_list_size
        self.tex_num = tex_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.tex_list_size


def niff2_tex_list_header_builder(tex_nodes):
    tex_num = len(tex_nodes)
    tex_list_size = sum(map(lambda tex_node: tex_node.tex_size, tex_nodes))
    return Niff2TexListHeader(tex_num, tex_list_size)


def niff2_tex_list_header_writer(tex_list_header, tex_nodes, buf):
    buf += tex_list_header.tex_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.tex_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.tex_list_size.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.tex_num.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += tex_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    for tex_node in tex_nodes:
        buf += tex_node.tex_size.to_bytes(4, BYTE_ORDER)
    return buf


class Niff2TexNode:
    def __init__(self, index, name_index, width, height):
        self.tex_tag = TAG_TEX
        self.this_tex_index = index
        self.tex_header_size = (13*4)
        self.tex_size = (13*4) + (7*4) + (5*4)
        self.tex_name_index = name_index
        self.tex_type = TEX_FORM_RGBA | TEX_DEPTH_32
        self.tex_wrap_s = TEX_WRAP_S
        self.tex_wrap_t = TEX_WRAP_T
        self.tex_anim = TEX_ANIM_OFF
        self.tex_data_area_size = (7*4)
        self.tex_anim_frame_rate = 0
        self.nintendo_extension_block_size = (5*4)
        self.user_extension_block_size = 0
        self.tex_img_width = width
        self.tex_img_height = height
        self.tex_tile_width = width
        self.tex_tile_height = height
        self.tex_offset_x = 0
        self.tex_offset_y = 0
        self.tex_img_index = BAD_INDEX
        self.tex_filter = NIFF2_TEX_FILTER_BILERP
        self.use_perspective_correction = NIFF2_PERSPECTIVE_CORRECTION
        self.mipmap_level = NIFF2_NO_MIPMAP
        self.use_color_palette = NIFF2_NO_USE_COLOR_PALETTE
        self.external_tex_img_num = 0  # Do not use BAD_INDEX


def niff2_tex_node_builder(index, name_index, width, height):
    return Niff2TexNode(index, name_index, width, height)


def niff2_tex_node_writer(tex_node, buf):
    buf += tex_node.tex_tag.to_bytes(4, BYTE_ORDER)
    buf += tex_node.this_tex_index.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_header_size.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_size.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_name_index.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_type.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_wrap_s.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_wrap_t.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_anim.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_data_area_size.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_anim_frame_rate.to_bytes(4, BYTE_ORDER)
    buf += tex_node.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tex_node.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_img_width.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_img_height.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_tile_width.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_tile_height.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_offset_x.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_offset_y.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_img_index.to_bytes(4, BYTE_ORDER)
    buf += tex_node.tex_filter.to_bytes(4, BYTE_ORDER)
    buf += tex_node.use_perspective_correction.to_bytes(4, BYTE_ORDER)
    buf += tex_node.mipmap_level.to_bytes(4, BYTE_ORDER)
    buf += tex_node.use_color_palette.to_bytes(4, BYTE_ORDER)
    buf += tex_node.external_tex_img_num.to_bytes(4, BYTE_ORDER)
    return buf
