"""Create .nif file from Blender data."""

import bpy
from bpy.types import (Camera, Light, Mesh)
from blend2niff.niff2.niff2_anim import (
    niff2_anim_list_header_builder, niff2_anim_list_header_writer,
    niff2_anim_group_builder, niff2_anim_group_writer,
    niff2_anim_node_builder)
from blend2niff.niff2.niff2_camera import (
    niff2_cam_list_header_builder, niff2_cam_list_header_writer,
    niff2_cam_node_builder, niff2_cam_node_writer)
from blend2niff.niff2.niff2_color import (
    niff2_color_list_header_builder, niff2_color_list_header_writer,
    niff2_tri_color_group_node_builder, niff2_tri_color_group_node_writer,
    niff2_vtx_color_group_node_builder, niff2_vtx_color_group_node_writer)
from blend2niff.niff2.niff2_env import (
    niff2_env_list_header_builder, niff2_env_list_header_writer,
    niff2_env_node_builder, niff2_env_node_writer)
from blend2niff.niff2.niff2_header import (
    Niff2FileHeader,
    niff2_file_header_builder, niff2_file_header_writer)
from blend2niff.niff2.niff2_light import (
    niff2_light_list_header_builder, niff2_light_list_header_writer,
    niff2_light_node_builder, niff2_light_node_writer)
from blend2niff.niff2.niff2_mat import (
    niff2_mat_list_header_builder, niff2_mat_list_header_writer,
    niff2_mat_node_builder, niff2_mat_node_writer)
from blend2niff.niff2.niff2_name import (
    niff2_name_list_header_builder, niff2_name_list_header_writer,
    niff2_name_node_builder, niff2_name_node_writer)
from blend2niff.niff2.niff2_obj import (
    niff2_obj_list_header_builder,
    niff2_obj_list_header_writer, niff2_obj_node_builder, niff2_obj_node_writer)
from blend2niff.niff2.niff2_part import (
    niff2_part_list_header_builder, niff2_part_list_header_writer,
    niff2_part_node_builder, niff2_part_node_writer)
from blend2niff.niff2.niff2_scene import (
    niff2_scene_header_builder,
    niff2_scene_header_writer)
from blend2niff.niff2.niff2_shape import (
    niff2_shape_list_header_builder, niff2_shape_list_header_writer,
    niff2_shape_node_builder, niff2_shape_node_writer)
from blend2niff.niff2.niff2_st import (
    niff2_st_list_header_builder, niff2_st_list_header_writer,
    niff2_st_group_node_builder, niff2_st_group_node_writer)
from blend2niff.niff2.niff2_tri import (
    niff2_tri_list_header_builder, niff2_tri_list_header_writer,
    niff2_tri_group_builder, niff2_tri_group_writer)
from blend2niff.niff2.niff2_vector import (
    niff2_vector_list_header_builder, niff2_vector_list_header_writer,
    niff2_tri_nv_group_builder, niff2_tri_nv_group_writer,
    niff2_vtx_nv_group_builder, niff2_vtx_nv_group_writer)
from blend2niff.niff2.niff2_vtx import (
    niff2_vtx_list_header_builder, niff2_vtx_list_header_writer,
    niff2_vtx_group_node_builder, niff2_vtx_group_node_writer)
from blend2niff.niff2.niff2_misc import (
    niff2_chain_root_list_header_builder, niff2_chain_root_list_header_writer,
    niff2_ci_img_list_header_builder, niff2_ci_img_list_header_writer,
    niff2_cluster_list_header_builder, niff2_cluster_list_header_writer,
    niff2_coll_list_header_builder, niff2_coll_list_header_writer,
    niff2_color_palette_list_header_builder, niff2_color_palette_list_header_writer,
    niff2_effector_list_header_builder, niff2_effector_list_header_writer,
    niff2_envelope_list_header_builder, niff2_envelope_list_header_writer,
    niff2_external_name_list_header_builder, niff2_external_name_list_header_writer,
    niff2_joint_list_header_builder, niff2_joint_list_header_writer,
    niff2_switch_list_header_builder, niff2_switch_list_header_writer,
    niff2_tex_img_list_header_builder, niff2_tex_img_list_header_writer,
    niff2_tex_list_header_builder, niff2_tex_list_header_writer,
    niff2_weight_list_header_builder, niff2_weight_list_header_writer)

from blend2niff.helpers import correct_gamma

BAD_INDEX = 0xFFFFFFFF


#
# Writer entry point
#
def write_niff2(data, filepath):
    print("running write_niff2...")

    filename = bpy.path.display_name_from_filepath(filepath)

    mesh_objs = list(
        filter(lambda obj: isinstance(obj.data, Mesh), data.objects))

    names = []
    scene_name = niff2_name_node_builder(len(names), filename+".scene")
    names.append(scene_name)

    # NIFF2 Materials: Create a single default material
    materials = []
    default_material_name = niff2_name_node_builder(
        len(names), "default_material.mat")
    names.append(default_material_name)
    default_material = niff2_mat_node_builder(0, default_material_name.index(),
                                              [1.0, 0.0, 0.0, 1.0])
    materials.append(default_material)

    # NIFF2 Materials: Create meshes materials
    materials_by_mesh = {}
    for obj in mesh_objs:
        mesh = obj.data
        materials_by_mesh[mesh] = []
        for mat in mesh.materials:
            mat_name = niff2_name_node_builder(len(names), mat.name+".mat")
            names.append(mat_name)
            mat_node = niff2_mat_node_builder(
                len(materials), mat_name.index(), correct_gamma(mat.diffuse_color))
            materials.append(mat_node)
            materials_by_mesh[mesh].append(mat_node)

    # NIFF2 VtxGroup <-> Blender Mesh (1 vtx_group per mesh)
    vtx_groups = []
    for vtx_group_index, obj in zip(range(len(mesh_objs)), mesh_objs):
        mesh = obj.data
        vtx_group_name = niff2_name_node_builder(len(names), mesh.name+".vtx")
        names.append(vtx_group_name)
        vtx_floats = []
        for vtx in mesh.vertices:
            vtx_floats += list(vtx.co)
        vtx_group = niff2_vtx_group_node_builder(
            vtx_group_index, vtx_group_name.index(), vtx_floats)
        vtx_groups.append(vtx_group)

    # Niff2 ColorGroup: Create a single default color
    tri_color_groups = []
    vtx_color_groups = []
    default_color = correct_gamma([0.8, 0.8, 0.8, 1.0])  # rgba
    default_tri_color_group = niff2_tri_color_group_node_builder(
        0, default_color)
    default_vtx_color_group = niff2_vtx_color_group_node_builder(
        0, default_color)
    tri_color_groups.append(default_tri_color_group)
    vtx_color_groups.append(default_vtx_color_group)

    # Niff2 ColorGroup: Create mesh vertex color group.
    # (!) Make sure to have the same number of tri_color_groups & vtx_color_groups.
    #     This prevents nifftools/checknb2.exe from crashing.
    # (!) Do not support smooth groups: 1 color per vertex!
    #     Indices are all aligned on both vertex coords and vertex colors.
    for vtx_color_group_index, mesh in zip(range(len(data.meshes)), data.meshes):
        mesh.calc_loop_triangles()
        vtx_colors = [float]*len(mesh.vertices)*4

        for tri in mesh.loop_triangles:
            for i in range(3):
                vtx_index = tri.vertices[i]
                loop_index = tri.loops[i]
                color = correct_gamma(
                    mesh.vertex_colors[0].data[loop_index].color)
                vtx_colors[(vtx_index*4)+0] = color[0]
                vtx_colors[(vtx_index*4)+1] = color[1]
                vtx_colors[(vtx_index*4)+2] = color[2]
                vtx_colors[(vtx_index*4)+3] = color[3]

        tri_color_group = niff2_tri_color_group_node_builder(
            1+vtx_color_group_index, default_color)
        tri_color_groups.append(tri_color_group)

        vtx_color_group = niff2_vtx_color_group_node_builder(
            1+vtx_color_group_index, vtx_colors)
        vtx_color_groups.append(vtx_color_group)

    # Niff2 VectorGroup: Create a single default normal vector
    tri_nv_groups = []
    vtx_nv_groups = []
    default_nv = [0.0, 1.0, 0.0]  # up
    default_tri_nv_group = niff2_tri_nv_group_builder(0, default_nv)
    default_vtx_nv_group = niff2_vtx_nv_group_builder(0, default_nv)
    tri_nv_groups.append(default_tri_nv_group)
    vtx_nv_groups.append(default_vtx_nv_group)

    # Niff2 VectorGroup: Create mesh vertex normals group.
    # (!) Make sure to have the same number of tri_nv_groups & vtx_nv_groups.
    #     This prevents nifftools/checknb2.exe from crashing.
    # (!) Do not support smooth groups: 1 normal per vertex!
    #     Indices are all aligned on both vertex coords and vertex normals.
    for mesh in data.meshes:
        mesh.calc_loop_triangles()
        mesh.calc_normals_split()
        vtx_normals = [float]*len(mesh.vertices)*3

        for tri in mesh.loop_triangles:
            for i in range(3):
                vtx_index = tri.vertices[i]
                loop_index = tri.loops[i]
                normal = mesh.loops[loop_index].normal
                vtx_normals[(vtx_index*3)+0] = normal[0]
                vtx_normals[(vtx_index*3)+1] = normal[1]
                vtx_normals[(vtx_index*3)+2] = normal[2]

        tri_nv_group = niff2_tri_nv_group_builder(
            len(tri_nv_groups), default_nv)
        tri_nv_groups.append(tri_nv_group)

        vtx_nv_group = niff2_vtx_nv_group_builder(
            len(vtx_nv_groups), vtx_normals)
        vtx_nv_groups.append(vtx_nv_group)

    # Niff2 StGroup: Create a single default texture coordinates
    st_groups = []
    default_st = [0.5, 0.5]  # center
    default_st_group = niff2_st_group_node_builder(0, default_st)
    st_groups.append(default_st_group)

    # NIFF2 TriGroup <-> Blender Mesh (1 tri_group per mesh)
    tri_groups = []
    tri_group_by_mesh = {}
    for tri_group_index, mesh, vtx_group in zip(range(len(data.meshes)), data.meshes, vtx_groups):
        tri_group_name = niff2_name_node_builder(len(names), mesh.name+".tri")
        names.append(tri_group_name)
        vtx_indices = []
        mesh.calc_loop_triangles()
        for tri in mesh.loop_triangles:
            vtx_indices += list(tri.vertices)
        tri_group = niff2_tri_group_builder(
            tri_group_index, tri_group_name.index(), vtx_group.index(), vtx_indices)
        tri_groups.append(tri_group)
        tri_group_by_mesh[mesh] = tri_group

    # NIFF2 Parts: Create meshes parts
    parts = []
    parts_by_mesh = {}
    for obj in mesh_objs:
        mesh = obj.data
        parts_by_mesh[mesh] = []
        mesh.calc_loop_triangles()

        for mat_index in range(len(mesh.materials)):
            tri_indices = []

            for tri_index, tri in zip(range(len(mesh.loop_triangles)), mesh.loop_triangles):
                if tri.material_index == mat_index:
                    tri_indices.append(tri_index)

            part_name = niff2_name_node_builder(
                len(names), mesh.name+".part."+str(mat_index).zfill(2))
            names.append(part_name)

            tri_group_index = tri_group_by_mesh[mesh].index()
            mat_index = materials_by_mesh[mesh][mat_index].index()
            part_node = niff2_part_node_builder(
                len(parts), part_name.index(), tri_group_index, mat_index, tri_indices)
            parts.append(part_node)
            parts_by_mesh[mesh].append(part_node)

    # NIFF2 Shape <-> Blender Mesh
    shapes = []
    for shape_index, mesh, tri_group in zip(range(len(data.meshes)), data.meshes, tri_groups):
        shape_name = niff2_name_node_builder(len(names), mesh.name+".shape")
        names.append(shape_name)
        shape = niff2_shape_node_builder(shape_index,
                                         shape_name.index(),
                                         tri_group.index(),
                                         default_material.index(),
                                         parts_by_mesh[mesh])
        shapes.append(shape)

    # NIFF2 Anim: 1 anim per object
    anim_groups = []
    for anim_index, obj, in zip(range(len(mesh_objs)), mesh_objs):
        anim_name = niff2_name_node_builder(len(names), obj.name+".anim")
        names.append(anim_name)
        anim_node = niff2_anim_node_builder(
            obj.location, obj.rotation_euler, obj.scale)
        anim_group = niff2_anim_group_builder(
            anim_index, anim_name.index(), anim_node)
        anim_groups.append(anim_group)

    # NIFF2 Obj: Blender Object
    objs = []
    for obj_index, obj, shape, anim_group in zip(range(len(mesh_objs)), mesh_objs, shapes, anim_groups):
        obj_name = niff2_name_node_builder(len(names), obj.name+".obj")
        names.append(obj_name)
        obj = niff2_obj_node_builder(
            obj_index, obj_name.index(), shape.index(), default_material.index(), anim_group.index())
        objs.append(obj)

    # NIFF2 Cam.
    cam_objs = list(
        filter(lambda obj: isinstance(obj.data, Camera), data.objects))

    cams = []
    for cam_index, obj in zip(range(len(cam_objs)), cam_objs):
        cam = obj.data
        matrix = obj.matrix_world.transposed()

        eye_anim_name = niff2_name_node_builder(
            len(names), cam.name+".eye.anim")
        names.append(eye_anim_name)
        eye_anim_node = niff2_anim_node_builder(
            obj.location, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        eye_anim_group = niff2_anim_group_builder(
            len(anim_groups), eye_anim_name.index(), eye_anim_node)
        anim_groups.append(eye_anim_group)

        lookat_anim_name = niff2_name_node_builder(
            len(names), cam.name+".lookat.anim")
        names.append(lookat_anim_name)
        lookat_anim_node = niff2_anim_node_builder(
            obj.location-matrix[2].xyz, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        lookat_anim_group = niff2_anim_group_builder(
            len(anim_groups), lookat_anim_name.index(), lookat_anim_node)
        anim_groups.append(lookat_anim_group)

        up_anim_name = niff2_name_node_builder(
            len(names), cam.name+".up.anim")
        names.append(up_anim_name)
        up_anim_node = niff2_anim_node_builder(
            obj.location+matrix[1].xyz, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        up_anim_group = niff2_anim_group_builder(
            len(anim_groups), up_anim_name.index(), up_anim_node)
        anim_groups.append(up_anim_group)

        eye_obj_name = niff2_name_node_builder(len(names), cam.name+".eye.obj")
        names.append(eye_obj_name)
        eye_obj = niff2_obj_node_builder(
            len(objs), eye_obj_name.index(), BAD_INDEX, BAD_INDEX, eye_anim_group.index())
        objs.append(eye_obj)

        lookat_obj_name = niff2_name_node_builder(
            len(names), cam.name+".lookat.obj")
        names.append(lookat_obj_name)
        lookat_obj = niff2_obj_node_builder(
            len(objs), lookat_obj_name.index(), BAD_INDEX, BAD_INDEX, lookat_anim_group.index())
        objs.append(lookat_obj)

        up_obj_name = niff2_name_node_builder(len(names), cam.name+".up.obj")
        names.append(up_obj_name)
        up_obj = niff2_obj_node_builder(
            len(objs), up_obj_name.index(), BAD_INDEX, BAD_INDEX, up_anim_group.index())
        objs.append(up_obj)

        cam_name = niff2_name_node_builder(len(names), cam.name+".cam")
        names.append(cam_name)
        cam_node = niff2_cam_node_builder(
            cam_index, cam_name.index(), eye_obj.index(), lookat_obj.index(), up_obj.index())
        cams.append(cam_node)

    # NIFF2 Env
    envs = []
    env_name = niff2_name_node_builder(len(names), filename+".env")
    names.append(env_name)
    env_node = niff2_env_node_builder(
        0, env_name.index(), correct_gamma(data.worlds[0].color))
    envs.append(env_node)

    # NIFF2 Light
    light_objs = list(
        filter(lambda obj: isinstance(obj.data, Light), data.objects))

    lights = []
    for obj in light_objs:
        light = obj.data
        matrix = obj.matrix_world.transposed()

        light_name = niff2_name_node_builder(len(names), light.name+".light")
        names.append(light_name)

        light_node = niff2_light_node_builder(len(lights),
                                              light_name.index(),
                                              correct_gamma(
                                                  [0.05, 0.05, 0.05]),
                                              correct_gamma(light.color),
                                              matrix[2].xyz)
        lights.append(light_node)

    # NIFF2 Header
    scene_header = niff2_scene_header_builder(
        scene_name.index(), objs, cams, envs, lights)
    env_list_header = niff2_env_list_header_builder(envs)
    cam_list_header = niff2_cam_list_header_builder(cams)
    light_list_header = niff2_light_list_header_builder(lights)
    obj_list_header = niff2_obj_list_header_builder(objs)
    shape_list_header = niff2_shape_list_header_builder(shapes)
    vtx_list_header = niff2_vtx_list_header_builder(vtx_groups)
    tri_list_header = niff2_tri_list_header_builder(tri_groups)
    color_list_header = niff2_color_list_header_builder(
        tri_color_groups, vtx_color_groups)
    vector_list_header = niff2_vector_list_header_builder(
        tri_nv_groups, vtx_nv_groups)
    st_list_header = niff2_st_list_header_builder(st_groups)
    part_list_header = niff2_part_list_header_builder(parts)
    mat_list_header = niff2_mat_list_header_builder(materials)
    tex_list_header = niff2_tex_list_header_builder()
    tex_img_list_header = niff2_tex_img_list_header_builder()
    anim_list_header = niff2_anim_list_header_builder(anim_groups)
    coll_list_header = niff2_coll_list_header_builder()
    switch_list_header = niff2_switch_list_header_builder()
    name_list_header = niff2_name_list_header_builder(names)
    ci_img_list_header = niff2_ci_img_list_header_builder()
    color_palette_list_header = niff2_color_palette_list_header_builder()
    envelope_list_header = niff2_envelope_list_header_builder()
    cluster_list_header = niff2_cluster_list_header_builder()
    weight_list_header = niff2_weight_list_header_builder()
    chain_root_list_header = niff2_chain_root_list_header_builder()
    joint_list_header = niff2_joint_list_header_builder()
    effector_list_header = niff2_effector_list_header_builder()
    external_name_list_header = niff2_external_name_list_header_builder()

    file_size = Niff2FileHeader.num_bytes() \
        + scene_header.num_bytes() \
        + env_list_header.num_bytes() \
        + cam_list_header.num_bytes() \
        + light_list_header.num_bytes() \
        + obj_list_header.num_bytes() \
        + shape_list_header.num_bytes() \
        + vtx_list_header.num_bytes() \
        + tri_list_header.num_bytes() \
        + color_list_header.num_bytes() \
        + vector_list_header.num_bytes() \
        + st_list_header.num_bytes() \
        + part_list_header.num_bytes() \
        + mat_list_header.num_bytes() \
        + tex_list_header.num_bytes() \
        + tex_img_list_header.num_bytes() \
        + anim_list_header.num_bytes() \
        + coll_list_header.num_bytes() \
        + switch_list_header.num_bytes() \
        + name_list_header.num_bytes() \
        + ci_img_list_header.num_bytes() \
        + color_palette_list_header.num_bytes() \
        + envelope_list_header.num_bytes() \
        + cluster_list_header.num_bytes() \
        + weight_list_header.num_bytes() \
        + chain_root_list_header.num_bytes() \
        + joint_list_header.num_bytes() \
        + effector_list_header.num_bytes() \
        + external_name_list_header.num_bytes()

    fh = niff2_file_header_builder(file_size)
    fh.scene_list_num_byte = scene_header.num_bytes()
    fh.env_list_num_byte = env_list_header.num_bytes()
    fh.cam_list_num_byte = cam_list_header.num_bytes()
    fh.light_list_num_byte = light_list_header.num_bytes()
    fh.obj_list_num_byte = obj_list_header.num_bytes()
    fh.shape_list_num_byte = shape_list_header.num_bytes()
    fh.vtx_list_num_byte = vtx_list_header.num_bytes()
    fh.tri_list_num_byte = tri_list_header.num_bytes()
    fh.color_list_num_byte = color_list_header.num_bytes()
    fh.vector_list_num_byte = vector_list_header.num_bytes()
    fh.st_list_num_byte = st_list_header.num_bytes()
    fh.part_list_num_byte = part_list_header.num_bytes()
    fh.mat_list_num_byte = mat_list_header.num_bytes()
    fh.tex_list_num_byte = tex_list_header.num_bytes()
    fh.tex_img_list_num_byte = tex_img_list_header.num_bytes()
    fh.anim_list_num_byte = anim_list_header.num_bytes()
    fh.coll_list_num_byte = coll_list_header.num_bytes()
    fh.switch_list_num_byte = switch_list_header.num_bytes()
    fh.name_list_num_byte = name_list_header.num_bytes()
    fh.ci_img_list_num_byte = ci_img_list_header.num_bytes()
    fh.color_palette_list_num_byte = color_palette_list_header.num_bytes()
    fh.envelope_list_num_byte = envelope_list_header.num_bytes()
    fh.cluster_list_num_byte = cluster_list_header.num_bytes()
    fh.weight_list_num_byte = weight_list_header.num_bytes()
    fh.chain_root_list_num_byte = chain_root_list_header.num_bytes()
    fh.joint_list_num_byte = joint_list_header.num_bytes()
    fh.effector_list_num_byte = effector_list_header.num_bytes()
    fh.external_name_list_num_byte = external_name_list_header.num_bytes()

    buf = bytearray()
    niff2_file_header_writer(fh, buf)

    niff2_scene_header_writer(scene_header, buf)

    niff2_env_list_header_writer(env_list_header, envs, buf)
    for env in envs:
        niff2_env_node_writer(env, buf)

    niff2_cam_list_header_writer(cam_list_header, cams, buf)
    for cam in cams:
        niff2_cam_node_writer(cam, buf)

    niff2_light_list_header_writer(light_list_header, lights, buf)
    for light in lights:
        niff2_light_node_writer(light, buf)

    niff2_obj_list_header_writer(obj_list_header, objs, buf)
    for obj in objs:
        niff2_obj_node_writer(obj, buf)

    niff2_shape_list_header_writer(shape_list_header, shapes, buf)
    for shape in shapes:
        niff2_shape_node_writer(shape, buf)

    niff2_vtx_list_header_writer(vtx_list_header, vtx_groups, buf)
    for vtx_group in vtx_groups:
        niff2_vtx_group_node_writer(vtx_group, buf)

    niff2_tri_list_header_writer(tri_list_header, tri_groups, buf)
    for tri_group in tri_groups:
        niff2_tri_group_writer(tri_group, buf)

    niff2_color_list_header_writer(
        color_list_header, tri_color_groups, vtx_color_groups, buf)
    for tri_color_group in tri_color_groups:
        niff2_tri_color_group_node_writer(tri_color_group, buf)
    for vtx_color_group in vtx_color_groups:
        niff2_vtx_color_group_node_writer(vtx_color_group, buf)

    niff2_vector_list_header_writer(
        vector_list_header, tri_nv_groups, vtx_nv_groups, buf)
    for tri_nv_group in tri_nv_groups:
        niff2_tri_nv_group_writer(tri_nv_group, buf)
    for vtx_nv_group in vtx_nv_groups:
        niff2_vtx_nv_group_writer(vtx_nv_group, buf)

    niff2_st_list_header_writer(st_list_header, st_groups, buf)
    for st_group in st_groups:
        niff2_st_group_node_writer(st_group, buf)

    niff2_part_list_header_writer(part_list_header, parts, buf)
    for part in parts:
        niff2_part_node_writer(part, buf)

    niff2_mat_list_header_writer(mat_list_header, materials, buf)
    for mat in materials:
        niff2_mat_node_writer(mat, buf)

    niff2_tex_list_header_writer(tex_list_header, buf)
    niff2_tex_img_list_header_writer(tex_img_list_header, buf)

    niff2_anim_list_header_writer(anim_list_header, anim_groups, buf)
    for anim_group in anim_groups:
        niff2_anim_group_writer(anim_group, buf)

    niff2_coll_list_header_writer(coll_list_header, buf)
    niff2_switch_list_header_writer(switch_list_header, buf)

    niff2_name_list_header_writer(name_list_header, names, buf)
    for name in names:
        niff2_name_node_writer(name, buf)

    niff2_ci_img_list_header_writer(ci_img_list_header, buf)
    niff2_color_palette_list_header_writer(color_palette_list_header, buf)
    niff2_envelope_list_header_writer(envelope_list_header, buf)
    niff2_cluster_list_header_writer(cluster_list_header, buf)
    niff2_weight_list_header_writer(weight_list_header, buf)
    niff2_chain_root_list_header_writer(chain_root_list_header, buf)
    niff2_joint_list_header_writer(joint_list_header, buf)
    niff2_effector_list_header_writer(effector_list_header, buf)
    niff2_external_name_list_header_writer(external_name_list_header, buf)

    f = open(filepath, 'wb')
    f.write(buf)
    f.close()

    return {'FINISHED'}
