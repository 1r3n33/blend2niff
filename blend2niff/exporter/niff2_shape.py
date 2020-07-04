#
# Consts
#
TAG_SHAPE_LIST = 0x00030000
TAG_SHAPE = 0x00030100

SHAPE_TYPE_CLEAR = 0x00000000
SHAPE_TYPE_AA = 0x00000001
SHAPE_TYPE_RA = 0x00000002
SHAPE_TYPE_ZB = 0x00000004
SHAPE_TYPE_CULL_BACK = 0x00000010
SHAPE_TYPE_CULL_FRONT = 0x00000020
SHAPE_TYPE_CULL_BOTH = 0x00000030
SHAPE_TYPE_USE_VTX_ALPHA_FOR_FOG = 0x00000100

TAG_TRI_GROUP = 0x00080100
TAG_ENVELOPE = 0x00220100
TAG_CLUSTER_SHAPE = 0x00280100

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Shape List
#
class Niff2ShapeListHeader:
    shape_list_tag: int
    shape_list_header_size: int
    shape_list_size: int
    shape_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    def num_bytes(self):
        return self.shape_list_size


def niff2_shape_list_header_builder(shapes):
    shape_num = len(shapes)
    shape_list_size = sum(map(lambda shape: shape.shape_size, shapes))

    slh = Niff2ShapeListHeader()
    slh.shape_list_tag = TAG_SHAPE_LIST
    slh.shape_list_header_size = (6*4) * (shape_num*4)
    slh.shape_list_size = (6*4) + (shape_num*4) + shape_list_size
    slh.shape_num = shape_num
    slh.nintendo_extension_block_size = 0
    slh.user_extension_block_size = 0
    return slh


def niff2_shape_list_header_writer(slh, shapes, buf):
    buf += slh.shape_list_tag.to_bytes(4, BYTE_ORDER)
    buf += slh.shape_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += slh.shape_list_size.to_bytes(4, BYTE_ORDER)
    buf += slh.shape_num.to_bytes(4, BYTE_ORDER)
    buf += slh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += slh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for shape in shapes:
        buf += shape.shape_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Shape Node
#
class Niff2ShapeNode:
    shape_tag: int
    this_shape_index: int
    shape_size: int
    shape_name_index: int
    shape_type: int
    shape_tri_link: int
    shape_mat_link: int
    shape_part_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int
    kind_of_node_for_geometry: int
    external_mat_file_name_index: int
    external_mat_name_index: int

    def index(self):
        return self.this_shape_index


def niff2_shape_node_builder(shape_index, shape_name_index, shape_tri_group_index, shape_mat_index):
    part_num = 1

    shape = Niff2ShapeNode()
    shape.shape_tag = TAG_SHAPE
    shape.this_shape_index = shape_index
    shape.shape_size = (10*4) + (part_num*4) + (3*4)
    shape.shape_name_index = shape_name_index
    shape.shape_type = SHAPE_TYPE_ZB | SHAPE_TYPE_CULL_BACK
    shape.shape_tri_link = shape_tri_group_index
    shape.shape_mat_link = shape_mat_index
    shape.shape_part_num = part_num
    shape.nintendo_extension_block_size = (3*4)
    shape.user_extension_block_size = 0
    shape.kind_of_node_for_geometry = TAG_TRI_GROUP
    shape.external_mat_file_name_index = BAD_INDEX
    shape.external_mat_name_index = BAD_INDEX
    return shape


def niff2_shape_node_writer(shape, part_index, buf):
    buf += shape.shape_tag.to_bytes(4, BYTE_ORDER)
    buf += shape.this_shape_index.to_bytes(4, BYTE_ORDER)
    buf += shape.shape_size.to_bytes(4, BYTE_ORDER)
    buf += shape.shape_name_index.to_bytes(4, BYTE_ORDER)
    buf += shape.shape_type.to_bytes(4, BYTE_ORDER)
    buf += shape.shape_tri_link.to_bytes(4, BYTE_ORDER)
    buf += shape.shape_mat_link.to_bytes(4, BYTE_ORDER)
    buf += shape.shape_part_num.to_bytes(4, BYTE_ORDER)
    buf += shape.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += shape.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += part_index.to_bytes(4, BYTE_ORDER)
    buf += shape.kind_of_node_for_geometry.to_bytes(4, BYTE_ORDER)
    buf += shape.external_mat_file_name_index.to_bytes(4, BYTE_ORDER)
    buf += shape.external_mat_name_index.to_bytes(4, BYTE_ORDER)
    return buf
