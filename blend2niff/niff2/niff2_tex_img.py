"""NIFF2 Texture Image Data."""

TAG_TEX_IMG_LIST = 0x00120000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


class Niff2TexImgListHeader:
    def __init__(self):
        self.tex_img_list_tag = TAG_TEX_IMG_LIST
        self.tex_img_list_header_size = 6*4
        self.tex_img_list_size = 6*4
        self.tex_img_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.tex_img_list_size


def niff2_tex_img_list_header_builder():
    return Niff2TexImgListHeader()


def niff2_tex_img_list_header_writer(tex_img_list_header, buf):
    buf += tex_img_list_header.tex_img_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.tex_img_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.tex_img_list_size.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.tex_img_num.to_bytes(4, BYTE_ORDER)
    buf += tex_img_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += tex_img_list_header.user_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    return buf
