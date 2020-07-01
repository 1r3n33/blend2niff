#
# Consts
#
TAG_NAME_LIST = 0x00110000
TAG_NAME = 0x00110100

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


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

    def num_bytes(self):
        return self.name_list_size


def niff2_name_list_header_builder(names):
    name_num = len(names)
    name_list_size = sum(map(lambda name: name.name_size, names))

    nlh = Niff2NameListHeader()
    nlh.name_list_tag = TAG_NAME_LIST
    nlh.name_list_header_size = (6*4) + (name_num*4)
    nlh.name_list_size = (6*4) + (name_num*4) + name_list_size
    nlh.name_num = name_num
    nlh.nintendo_extension_block_size = 0
    nlh.user_extension_block_size = 0
    return nlh


def niff2_name_list_header_writer(nlh, names, buf):
    buf += nlh.name_list_tag.to_bytes(4, BYTE_ORDER)
    buf += nlh.name_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += nlh.name_list_size.to_bytes(4, BYTE_ORDER)
    buf += nlh.name_num.to_bytes(4, BYTE_ORDER)
    buf += nlh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += nlh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for name in names:
        buf += name.name_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Name Node
#
class Niff2NameNode:
    name_tag: int
    this_name_index: int
    name_header_size: int
    name_size: int
    node_name: str

    def index(self):
        return self.this_name_index


def niff2_name_node_builder(index, name):
    name_size = len(name)
    if ((name_size % 4) > 0):
        name_size += 4-(name_size % 4)

    node = Niff2NameNode()
    node.name_tag = TAG_NAME
    node.this_name_index = index
    node.name_header_size = (4*4)
    node.name_size = (4*4) + name_size
    node.node_name = name
    return node


def niff2_name_node_writer(name, buf):
    buf += name.name_tag.to_bytes(4, BYTE_ORDER)
    buf += name.this_name_index.to_bytes(4, BYTE_ORDER)
    buf += name.name_header_size.to_bytes(4, BYTE_ORDER)
    buf += name.name_size.to_bytes(4, BYTE_ORDER)

    buf += name.node_name.encode('ascii', 'ignore')
    if ((len(name.node_name) % 4) > 0):
        buf += (0).to_bytes(4-(len(name.node_name) % 4), BYTE_ORDER)

    return buf
