"""NIFF2 Environment."""

#
# Consts
#
TAG_ENV_LIST = 0x00100000

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Env List
#
class Niff2EnvListHeader:
    def __init__(self):
        self.env_list_tag = TAG_ENV_LIST
        self.env_list_header_size = 6*4
        self.env_list_size = 6*4
        self.env_num = 0
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.env_list_size


def niff2_env_list_header_builder():
    return Niff2EnvListHeader()


def niff2_env_list_header_writer(env_list_header, buf):
    buf += env_list_header.env_list_tag.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.env_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.env_list_size.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.env_num.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += env_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
