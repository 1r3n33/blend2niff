"""NIFF2 Texture Configuration."""

TAG_TEX_LIST = 0x000b0000

BYTE_ORDER = 'big'


class Niff2TexListHeader:
    def __init__(self):
        self.tex_list_tag = TAG_TEX_LIST
        self.tex_list_header_size = 6*4
        self.tex_list_size = 6*4
        self.tex_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.tex_list_size


def niff2_tex_list_header_builder():
    return Niff2TexListHeader()


def niff2_tex_list_header_writer(tex_list_header, buf):
    buf += tex_list_header.tex_list_tag.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.tex_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.tex_list_size.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.tex_num.to_bytes(4, BYTE_ORDER)
    buf += tex_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += tex_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
