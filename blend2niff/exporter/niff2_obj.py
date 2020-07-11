"""NIFF2 Object."""

#
# Consts
#
TAG_OBJ_LIST = 0x00020000
TAG_OBJ = 0x00020100

OBJ_STATE_CLEAR = 0x00000000
OBJ_STATE_ACTIVE = 0x00000001

OBJ_TYPE_NULL = 0x00000000
OBJ_TYPE_3D = 0x00000001
OBJ_TYPE_BILLBOARD = 0x00000002

OBJ_GROUP_NONE = 0x00000000

OBJ_RENDER_CYC_1CYC = 0x00000000
OBJ_RENDER_CYC_2CYC = 0x00000001

OBJ_RENDER_FLAG_NIFF = 0x00
OBJ_RENDER_FLAG_N64GBI = 0x04

OBJ_RENDER_NIFF_OPA_SURF = 0xd00000
OBJ_RENDER_NIFF_OPA_INTER = 0xb00000
OBJ_RENDER_NIFF_OPA_DECAL = 0x900000
OBJ_RENDER_NIFF_TEX_EDGE = 0x700000
OBJ_RENDER_NIFF_XLU_SURF = 0x500000
OBJ_RENDER_NIFF_XLU_INTER = 0x300000
OBJ_RENDER_NIFF_XLU_DECAL = 0x100000

NO_LINK_BILLBOARD = 0x00000000
ANY_LINK_BILLBOARD = 0x00000001

BAD_INDEX = 0xFFFFFFFF

BYTE_ORDER = 'big'


#
# Obj List
#
class Niff2ObjListHeader:
    obj_list_tag: int
    obj_list_header_size: int
    obj_list_size: int
    obj_num: int
    nintendo_extension_block_size: int
    user_extension_block_size: int

    def num_bytes(self):
        return self.obj_list_size


def niff2_obj_list_header_builder(objs):
    obj_num = len(objs)
    obj_list_size = sum(map(lambda obj: obj.obj_size, objs))

    olh = Niff2ObjListHeader()
    olh.obj_list_tag = TAG_OBJ_LIST
    olh.obj_list_header_size = (6*4) + (obj_num*4)
    olh.obj_list_size = (6*4) + (obj_num*4) + obj_list_size
    olh.obj_num = obj_num
    olh.nintendo_extension_block_size = 0
    olh.user_extension_block_size = 0
    return olh


def niff2_obj_list_header_writer(olh, objs, buf):
    buf += olh.obj_list_tag.to_bytes(4, BYTE_ORDER)
    buf += olh.obj_list_header_size.to_bytes(4, BYTE_ORDER)
    buf += olh.obj_list_size.to_bytes(4, BYTE_ORDER)
    buf += olh.obj_num.to_bytes(4, BYTE_ORDER)
    buf += olh.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += olh.user_extension_block_size.to_bytes(4, BYTE_ORDER)

    for obj in objs:
        buf += obj.obj_size.to_bytes(4, BYTE_ORDER)

    return buf


#
# Obj Node
#
class Niff2ObjNode:
    obj_tag: int
    this_obj_index: int
    obj_size: int
    obj_name_index: int
    obj_state: int
    obj_type: int
    obj_group: int
    obj_pri: int
    obj_render_cycle_type: int
    obj_render_pri: int
    obj_render_type0: int
    obj_render_type1: int
    have_link_billboard: int
    obj_lod_num: int
    obj_child_num: int
    obj_parent_link: int
    obj_shape_link: int
    obj_mat_link: int
    obj_anim_link: int
    obj_coll_link: int
    nintendo_extension_block_size: int
    user_extension_block_size: int
    obj_render_cycle_type_for_fog: int
    obj_render_pri_for_fog: int
    obj_render_type0_for_fog: int
    obj_render_type1_for_fog: int
    obj_chain_root_link_num: int
    external_obj_lod_num: int
    external_obj_num: int


def niff2_obj_node_builder(obj_index, obj_name_index, obj_shape_index, obj_mat_index, anim_group_index):
    obj = Niff2ObjNode()
    obj.obj_tag = TAG_OBJ
    obj.this_obj_index = obj_index
    obj.obj_size = (22*4) + (7*4)
    obj.obj_name_index = obj_name_index
    obj.obj_state = OBJ_STATE_ACTIVE
    obj.obj_type = OBJ_TYPE_3D
    obj.obj_group = OBJ_GROUP_NONE
    obj.obj_pri = 0
    obj.obj_render_cycle_type = OBJ_RENDER_CYC_1CYC
    obj.obj_render_pri = OBJ_RENDER_FLAG_NIFF << 24 | OBJ_RENDER_NIFF_OPA_SURF
    obj.obj_render_type0 = 0
    obj.obj_render_type1 = 0
    obj.have_link_billboard = NO_LINK_BILLBOARD
    obj.obj_lod_num = 0
    obj.obj_child_num = 0
    obj.obj_parent_link = BAD_INDEX
    obj.obj_shape_link = obj_shape_index
    obj.obj_mat_link = obj_mat_index
    obj.obj_anim_link = anim_group_index
    obj.obj_coll_link = BAD_INDEX
    obj.nintendo_extension_block_size = 7*4
    obj.user_extension_block_size = 0
    obj.obj_render_cycle_type_for_fog = OBJ_RENDER_CYC_2CYC
    obj.obj_render_pri_for_fog = OBJ_RENDER_FLAG_NIFF << 24 | OBJ_RENDER_NIFF_OPA_SURF
    obj.obj_render_type0_for_fog = 0
    obj.obj_render_type1_for_fog = 0
    obj.obj_chain_root_link_num = 0
    obj.external_obj_lod_num = 0
    obj.external_obj_num = 0
    return obj


def niff2_obj_node_writer(obj, buf):
    buf += obj.obj_tag.to_bytes(4, BYTE_ORDER)
    buf += obj.this_obj_index.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_size.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_name_index.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_state.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_type.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_group.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_pri.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_cycle_type.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_pri.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_type0.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_type1.to_bytes(4, BYTE_ORDER)
    buf += obj.have_link_billboard.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_lod_num.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_child_num.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_parent_link.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_shape_link.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_mat_link.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_anim_link.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_coll_link.to_bytes(4, BYTE_ORDER)
    buf += obj.nintendo_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += obj.user_extension_block_size.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_cycle_type_for_fog.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_pri_for_fog.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_type0_for_fog.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_render_type1_for_fog.to_bytes(4, BYTE_ORDER)
    buf += obj.obj_chain_root_link_num.to_bytes(4, BYTE_ORDER)
    buf += obj.external_obj_lod_num.to_bytes(4, BYTE_ORDER)
    buf += obj.external_obj_num.to_bytes(4, BYTE_ORDER)
    return buf
