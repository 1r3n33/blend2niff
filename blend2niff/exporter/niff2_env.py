"""NIFF2 Environment."""

#
# Consts
#
TAG_ENV_LIST = 0x00100000
TAG_ENV = 0x00100100

ENV_FOG_NONE = 0x00000000
ENV_FOG_USE = 0x00000001

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Env List
#
class Niff2EnvListHeader:
    def __init__(self, env_num, env_list_size):
        self.env_list_tag = TAG_ENV_LIST
        self.env_list_header_size = (6*4) + (env_num*4)
        self.env_list_size = (6*4) + (env_num*4) + env_list_size
        self.env_num = env_num
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0

    def num_bytes(self):
        return self.env_list_size


def niff2_env_list_header_builder(envs):
    env_num = len(envs)
    env_list_size = sum(map(lambda env: env.env_size, envs))
    return Niff2EnvListHeader(env_num, env_list_size)


def niff2_env_list_header_writer(env_list_header, envs, buf):
    buf += env_list_header.env_list_tag.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.env_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.env_list_size.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.env_num.to_bytes(4, BYTE_ORDER)
    buf += env_list_header.nintendo_extension_block_size.to_bytes(
        4, BYTE_ORDER)
    buf += env_list_header.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for env in envs:
        buf += env.env_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Env Node
#
class Niff2EnvNode:
    def __init__(self, index, name_index, fill_color):
        self.env_tag = TAG_ENV
        self.this_env_index = index
        self.env_size = 14*4
        self.env_name_index = name_index
        self.fog = ENV_FOG_NONE
        self.fog_color = 0xFFFFFFFF
        self.fog_near = 1000
        self.fog_far = 1000
        self.fill_color = fill_color
        self.fill_depth = 0x00FFFFFF
        self.bg_sprite_img = BAD_INDEX
        self.bg_sprite_depth = BAD_INDEX
        self.nintendo_extension_block_size = 0
        self.user_extension_block_size = 0


def niff2_env_node_builder(index, name_index, background_color_rgb_f):
    r = int(background_color_rgb_f[0]*255.0)
    g = int(background_color_rgb_f[1]*255.0)
    b = int(background_color_rgb_f[2]*255.0)
    fill_color = (r << 16) | (g << 8) | b
    return Niff2EnvNode(index, name_index, fill_color)


def niff2_env_node_writer(env_node, buf):
    buf += env_node.env_tag.to_bytes(4, BYTE_ORDER)
    buf += env_node.this_env_index.to_bytes(4, BYTE_ORDER)
    buf += env_node.env_size.to_bytes(4, BYTE_ORDER)
    buf += env_node.env_name_index.to_bytes(4, BYTE_ORDER)
    buf += env_node.fog.to_bytes(4, BYTE_ORDER)
    buf += env_node.fog_color.to_bytes(4, BYTE_ORDER)
    buf += env_node.fog_near.to_bytes(4, BYTE_ORDER)
    buf += env_node.fog_far.to_bytes(4, BYTE_ORDER)
    buf += env_node.fill_color.to_bytes(4, BYTE_ORDER)
    buf += env_node.fill_depth.to_bytes(4, BYTE_ORDER)
    buf += env_node.bg_sprite_img.to_bytes(4, BYTE_ORDER)
    buf += env_node.bg_sprite_depth.to_bytes(4, BYTE_ORDER)
    buf += env_node.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += env_node.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    return buf
