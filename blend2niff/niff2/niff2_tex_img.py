"""NIFF2 Texture Image Data."""

TAG_TEX_IMG_LIST = 0x00120000
TAG_TEX_IMG = 0x00120100

NIFF2_NO_MIPMAP = 0x00000000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


class Niff2TexImgListHeader:
    def __init__(self, tex_img_num, tex_img_list_size):
        self.tex_img_list_tag = TAG_TEX_IMG_LIST
        self.tex_img_list_header_size = (6*4) + (tex_img_num*4)
        self.tex_img_list_size = (6*4) + (tex_img_num*4) + tex_img_list_size
        self.tex_img_num = tex_img_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.tex_img_list_size


def niff2_tex_img_list_header_builder(tex_img_nodes):
    tex_img_num = len(tex_img_nodes)
    tex_img_list_size = sum(
        map(lambda tex_img_node: tex_img_node.tex_img_size, tex_img_nodes))
    return Niff2TexImgListHeader(tex_img_num, tex_img_list_size)


def niff2_tex_img_list_header_writer(tex_img_list_header, tex_img_nodes, buf):
    buf += tex_img_list_header.tex_img_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.tex_img_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.tex_img_list_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.tex_img_num.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += tex_img_list_header.user_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    for tex_img_node in tex_img_nodes:
        buf += tex_img_node.tex_img_size.to_bytes(4, BYTE_ORDER)
    return buf


class Niff2TexImgNode:
    def __init__(self, index, tex_img_data):
        self.tex_img_tag = TAG_TEX_IMG
        self.this_tex_img_index = index
        self.tex_img_header_size = (7*4)
        self.tex_img_size = (7*4) + (1*4) + len(tex_img_data)
        self.nintendo_extension_block_size = (1*4)
        self.user_extension_block_size = 0
        self.tex_img_data = tex_img_data
        self.mipmap_max_level = NIFF2_NO_MIPMAP


def niff2_tex_img_node_builder(index, tex_img_data):
    return Niff2TexImgNode(index, tex_img_data)


def niff2_tex_img_node_writer(tex_img_node, buf):
    buf += tex_img_node.tex_img_tag.to_bytes(4, BYTE_ORDER)
    buf += tex_img_node.this_tex_img_index.to_bytes(4, BYTE_ORDER)
    buf += tex_img_node.tex_img_header_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_node.tex_img_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_node.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_node.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += bytearray(tex_img_node.tex_img_data)
    buf += tex_img_node.mipmap_max_level.to_bytes(4, BYTE_ORDER)
    return buf
