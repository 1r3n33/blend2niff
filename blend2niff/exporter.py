"""Create .nif file from Blender data."""

import bpy
from bpy.types import (Camera, Light, Mesh, ShaderNodeTexImage)

import png

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
    niff2_st_group_builder, niff2_st_group_writer)
from blend2niff.niff2.niff2_tex import (
    niff2_tex_list_header_builder, niff2_tex_list_header_writer,
    niff2_tex_node_builder, niff2_tex_node_writer)
from blend2niff.niff2.niff2_tex_img import (
    niff2_tex_img_list_header_builder, niff2_tex_img_list_header_writer,
    niff2_tex_img_node_builder, niff2_tex_img_node_writer)
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
    niff2_weight_list_header_builder, niff2_weight_list_header_writer)

from blend2niff.helpers import correct_gamma

BAD_INDEX = 0xFFFFFFFF


class Exporter:
    def __init__(self):
        self.names = []  # All names
        self.textures = []  # All textures
        self.tex_images = []  # All texture images
        self.materials = []  # All materials, 0 is default material
        self.materials_by_mesh = {}  # NIFF2 materials by Blender mesh
        self.vtx_groups = []  # All vertex groups
        self.vtx_group_by_mesh = {}  # NIFF2 vertex group by Blender mesh
        self.tri_color_groups = []  # All triangle color groups
        self.vtx_color_groups = []  # All vertex color groups
        self.tri_nv_groups = []  # All triangle normal groups
        self.vtx_nv_groups = []  # All vertex normal groups
        self.normal_indices_by_mesh = {}  # vertex normal indices by Blender mesh
        self.st_groups = []  # All vertex texture coord groups
        self.st_indices_by_mesh = {}  # tex coord indices by Blender mesh
        self.tri_groups = []  # All triangle groups
        self.tri_group_by_mesh = {}  # NIFF2 triangle group by Blender mesh
        self.parts = []  # All shape parts
        self.parts_by_mesh = {}  # NIFF2 parts by Blender mesh
        self.shapes = []  # All shapes
        self.shape_by_mesh = {}  # NIFF2 shape by Blender mesh
        self.anim_groups = []  # All anim groups
        self.anim_group_by_mesh = {}  # NIFF2 anim group by Blender mesh
        self.objs = []  # All objects

    def create_name(self, name):
        """
        Create, register and return a name.
        """
        name_node = niff2_name_node_builder(len(self.names), name)
        self.names.append(name_node)
        return name_node

    def create_textures(self, objs):
        """
        Create and register all textures.
        """
        meshes = [obj.data for obj in objs if isinstance(obj.data, Mesh)]

        for mesh in meshes:
            for mat in mesh.materials:
                if mat.use_nodes and mat.node_tree:
                    tex_img_nodes = [node for node in mat.node_tree.nodes if isinstance(
                        node, ShaderNodeTexImage)]
                    for tex_img_node in tex_img_nodes:
                        filepath = bpy.path.abspath(
                            tex_img_node.image.filepath, library=tex_img_node.image.library)
                        png_reader = png.Reader(filepath)
                        image = png_reader.read()

                        tex_img = niff2_tex_img_node_builder(
                            len(self.tex_images), [byte for row in image[2] for byte in row])
                        self.tex_images.append(tex_img)

                        tex_name = self.create_name(
                            bpy.path.display_name_from_filepath(filepath)+".tex")

                        tex = niff2_tex_node_builder(len(self.textures),
                                                     tex_name.index(),
                                                     tex_img.index,
                                                     width=image[0],
                                                     height=image[1])
                        self.textures.append(tex)

    def create_materials(self, objs):
        """
        Create and register all scene materials including the default material (index 0).
        TODO: Revise the interface to remove objs as the goal is to create all mats from scene.
        """
        # Create full red default material
        default_material_name = self.create_name("default_material.mat")
        default_material = niff2_mat_node_builder(0,
                                                  default_material_name.index(),
                                                  [1.0, 0.0, 0.0, 1.0])
        self.materials.append(default_material)

        # For each mesh
        for obj in objs:
            if isinstance(obj.data, Mesh):
                mesh = obj.data
                self.materials_by_mesh[mesh] = []

                # Create mesh materials
                for mat in mesh.materials:
                    mat_name = self.create_name(mat.name+".mat")
                    mat_node = niff2_mat_node_builder(len(self.materials),
                                                      mat_name.index(),
                                                      correct_gamma(mat.diffuse_color))
                    self.materials.append(mat_node)
                    self.materials_by_mesh[mesh].append(mat_node)

    def get_default_material(self):
        """
        Return default material.
        """
        return self.materials[0]

    def create_vertex_groups(self, objs):
        """
        Create and register all vertex groups.
        """
        # For each mesh
        for obj in objs:
            if isinstance(obj.data, Mesh):
                mesh = obj.data

                vtx_group_name = self.create_name(mesh.name+".vtx")

                vtx_floats = []
                for vtx in mesh.vertices:
                    vtx_floats += list(vtx.co)

                vtx_group = niff2_vtx_group_node_builder(len(self.vtx_groups),
                                                         vtx_group_name.index(),
                                                         vtx_floats)
                self.vtx_groups.append(vtx_group)
                self.vtx_group_by_mesh[mesh] = vtx_group

    def create_color_groups(self, objs):
        """
        Create and register all vertex color groups and all triangle color groups.
        Also create default grey-ish color.
        Make sure to have the same number of tri_color_groups & vtx_color_groups.
        This prevents nifftools/checknb2.exe from crashing.
        Do not support smooth groups: 1 color per vertex!
        Indices are all aligned on both vertex coords and vertex colors.
        """
        default_color = correct_gamma([0.8, 0.8, 0.8, 1.0])  # rgba
        default_tri_color_group = niff2_tri_color_group_node_builder(
            0, default_color)
        default_vtx_color_group = niff2_vtx_color_group_node_builder(
            0, default_color)
        self.tri_color_groups.append(default_tri_color_group)
        self.vtx_color_groups.append(default_vtx_color_group)

        for obj in objs:
            if isinstance(obj.data, Mesh):
                mesh = obj.data

                # Add vertex colors if exists
                if len(mesh.vertex_colors) > 0:
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

                    vtx_color_group = niff2_vtx_color_group_node_builder(
                        len(self.vtx_color_groups), vtx_colors)
                    self.vtx_color_groups.append(vtx_color_group)

                # Add default color if vertex colors do not exist
                else:
                    vtx_color_group = niff2_vtx_color_group_node_builder(
                        len(self.vtx_color_groups), default_color)
                    self.vtx_color_groups.append(vtx_color_group)

                # Add default color for triangles
                tri_color_group = niff2_tri_color_group_node_builder(
                    len(self.tri_color_groups), default_color)
                self.tri_color_groups.append(tri_color_group)

    def create_vector_groups(self, objs):
        """
        Create and register all vertex normal groups and triangle normal groups.
        Also create default up normal.
        Make sure to have the same number of tri_vector_groups & vtx_vector_groups.
        This prevents nifftools/checknb2.exe from crashing.
        """
        default_nv = [0.0, 1.0, 0.0]  # up
        default_tri_nv_group = niff2_tri_nv_group_builder(0, default_nv)
        default_vtx_nv_group = niff2_vtx_nv_group_builder(0, default_nv)
        self.tri_nv_groups.append(default_tri_nv_group)
        self.vtx_nv_groups.append(default_vtx_nv_group)

        meshes = [obj.data for obj in objs if isinstance(obj.data, Mesh)]

        for mesh in meshes:
            mesh.calc_loop_triangles()
            mesh.calc_normals_split()

            # Collect unique normals in index_by_normal with undefined indices
            index_by_normal = {}
            for tri in mesh.loop_triangles:
                for i in range(3):
                    loop_index = tri.loops[i]
                    normal = tuple(mesh.loops[loop_index].normal)
                    index_by_normal[normal] = -1

            # Map keys to normals and set indices
            normals = list(index_by_normal.keys())
            for index, normal in zip(range(len(normals)), normals):
                index_by_normal[normal] = index

            # Create mesh normals indices
            normal_indices = []
            for tri in mesh.loop_triangles:
                for i in range(3):
                    loop_index = tri.loops[i]
                    normal = tuple(mesh.loops[loop_index].normal)
                    normal_indices.append(index_by_normal[normal])
            self.normal_indices_by_mesh[mesh] = normal_indices

            # Create NIFF2 data
            tri_nv_group = niff2_tri_nv_group_builder(
                len(self.tri_nv_groups), default_nv)
            self.tri_nv_groups.append(tri_nv_group)

            vtx_nv_group = niff2_vtx_nv_group_builder(
                len(self.vtx_nv_groups), [value for normal in normals for value in normal])
            self.vtx_nv_groups.append(vtx_nv_group)

    def create_st_groups(self, objs):
        """
        Create and register texture coord groups.
        """
        default_st = [0.5, 0.5]  # center
        default_st_group = niff2_st_group_builder(0, default_st)
        self.st_groups.append(default_st_group)

        meshes = [obj.data for obj in objs if isinstance(obj.data, Mesh)]

        for mesh in meshes:
            if mesh.uv_layers:
                mesh.calc_loop_triangles()

                # Collect unique tex coords in index_by_st with undefined indices
                index_by_st = {}
                for tri in mesh.loop_triangles:
                    for i in range(3):
                        loop_index = tri.loops[i]
                        s_t = tuple(mesh.uv_layers[0].data[loop_index].uv)
                        index_by_st[s_t] = -1

                # Map keys to st and set indices
                st_list = list(index_by_st.keys())
                for index, s_t in zip(range(len(st_list)), st_list):
                    index_by_st[s_t] = index

                # Create mesh st indices
                st_indices = []
                for tri in mesh.loop_triangles:
                    for i in range(3):
                        loop_index = tri.loops[i]
                        s_t = tuple(mesh.uv_layers[0].data[loop_index].uv)
                        st_indices.append(index_by_st[s_t])
                self.st_indices_by_mesh[mesh] = st_indices

                # Create NIFF2 data
                st_group = niff2_st_group_builder(
                    len(self.st_groups), [value for st in st_list for value in st])
                self.st_groups.append(st_group)

            else:
                self.st_indices_by_mesh[mesh] = [0]*len(mesh.loop_triangles)*3
                st_group = niff2_st_group_builder(
                    len(self.st_groups), default_st)
                self.st_groups.append(st_group)

    def create_tri_groups(self, objs):
        """
        Create and register all triangle groups.
        """
        meshes = [obj.data for obj in objs if isinstance(obj.data, Mesh)]

        for mesh in meshes:
            mesh.calc_loop_triangles()

            tri_group_name = self.create_name(mesh.name+".tri")
            vtx_group = self.vtx_group_by_mesh[mesh]
            vtx_indices = [
                index for tri in mesh.loop_triangles for index in tri.vertices]
            normal_indices = self.normal_indices_by_mesh[mesh]
            st_indices = self.st_indices_by_mesh[mesh]

            tri_group = niff2_tri_group_builder(len(self.tri_groups),
                                                tri_group_name.index(),
                                                vtx_group.index(),
                                                vtx_indices,
                                                normal_indices,
                                                st_indices)

            self.tri_groups.append(tri_group)
            self.tri_group_by_mesh[mesh] = tri_group

    def create_parts(self, objs):
        """
        Create and register shape parts.
        """
        meshes = [obj.data for obj in objs if isinstance(obj.data, Mesh)]

        for mesh in meshes:
            mesh.calc_loop_triangles()

            self.parts_by_mesh[mesh] = []

            for mat_index in range(len(mesh.materials)):
                tri_indices = []

                for tri_index, tri in zip(range(len(mesh.loop_triangles)), mesh.loop_triangles):
                    if tri.material_index == mat_index:
                        tri_indices.append(tri_index)

                tri_group_index = self.tri_group_by_mesh[mesh].index()
                part_name = self.create_name(
                    mesh.name+".part."+str(mat_index).zfill(2))
                mat_index = self.materials_by_mesh[mesh][mat_index].index()

                part_node = niff2_part_node_builder(
                    len(self.parts), part_name.index(), tri_group_index, mat_index, tri_indices)

                self.parts.append(part_node)
                self.parts_by_mesh[mesh].append(part_node)

    def create_shapes(self, objs):
        """
        Create and register shapes from meshes.
        """
        meshes = [obj.data for obj in objs if isinstance(obj.data, Mesh)]

        for mesh in meshes:
            shape_name = self.create_name(mesh.name+".shape")
            tri_group = self.tri_group_by_mesh[mesh]
            material = self.get_default_material()
            parts = self.parts_by_mesh[mesh]

            shape = niff2_shape_node_builder(len(self.shapes),
                                             shape_name.index(),
                                             tri_group.index(),
                                             material.index(),
                                             parts)

            self.shapes.append(shape)
            self.shape_by_mesh[mesh] = shape

    def create_anim_groups(self, objs):
        """
        Create and register anim matrix groups.
        """
        mesh_objs = [obj for obj in objs if isinstance(obj.data, Mesh)]

        for obj in mesh_objs:
            anim_name = self.create_name(obj.name+".anim")

            anim_node = niff2_anim_node_builder(
                obj.location, obj.rotation_euler, obj.scale)

            anim_group = niff2_anim_group_builder(
                len(self.anim_groups), anim_name.index(), anim_node)

            self.anim_groups.append(anim_group)
            self.anim_group_by_mesh[obj.data] = anim_group

    def create_objects(self, objs):
        """
        Create and register all 3D objects.
        """
        mesh_objs = [obj for obj in objs if isinstance(obj.data, Mesh)]

        for obj in mesh_objs:
            obj_name = self.create_name(obj.name+".obj")
            obj_shape = self.shape_by_mesh[obj.data]
            obj_material = self.get_default_material()
            obj_anim_group = self.anim_group_by_mesh[obj.data]

            obj = niff2_obj_node_builder(len(self.objs),
                                         obj_name.index(),
                                         obj_shape.index(),
                                         obj_material.index(),
                                         obj_anim_group.index())
            self.objs.append(obj)


#
# Writer entry point
#
def write_niff2(data, filepath):
    print("running write_niff2...")
    exporter = Exporter()

    filename = bpy.path.display_name_from_filepath(filepath)

    mesh_objs = list(
        filter(lambda obj: isinstance(obj.data, Mesh), data.objects))

    scene_name = exporter.create_name(filename+".scene")

    exporter.create_textures(mesh_objs)

    exporter.create_materials(mesh_objs)

    exporter.create_vertex_groups(mesh_objs)

    exporter.create_color_groups(mesh_objs)

    exporter.create_vector_groups(mesh_objs)

    exporter.create_st_groups(mesh_objs)

    exporter.create_tri_groups(mesh_objs)

    exporter.create_parts(mesh_objs)

    exporter.create_shapes(mesh_objs)

    exporter.create_anim_groups(mesh_objs)

    exporter.create_objects(mesh_objs)

    # NIFF2 Cam.
    cam_objs = list(
        filter(lambda obj: isinstance(obj.data, Camera), data.objects))

    cams = []
    for cam_index, obj in zip(range(len(cam_objs)), cam_objs):
        cam = obj.data
        matrix = obj.matrix_world.transposed()

        eye_anim_name = exporter.create_name(cam.name+".eye.anim")
        eye_anim_node = niff2_anim_node_builder(
            obj.location, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        eye_anim_group = niff2_anim_group_builder(
            len(exporter.anim_groups), eye_anim_name.index(), eye_anim_node)
        exporter.anim_groups.append(eye_anim_group)

        lookat_anim_name = exporter.create_name(cam.name+".lookat.anim")
        lookat_anim_node = niff2_anim_node_builder(
            obj.location-matrix[2].xyz, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        lookat_anim_group = niff2_anim_group_builder(
            len(exporter.anim_groups), lookat_anim_name.index(), lookat_anim_node)
        exporter.anim_groups.append(lookat_anim_group)

        up_anim_name = exporter.create_name(cam.name+".up.anim")
        up_anim_node = niff2_anim_node_builder(
            obj.location+matrix[1].xyz, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
        up_anim_group = niff2_anim_group_builder(
            len(exporter.anim_groups), up_anim_name.index(), up_anim_node)
        exporter.anim_groups.append(up_anim_group)

        eye_obj_name = exporter.create_name(cam.name+".eye.obj")
        eye_obj = niff2_obj_node_builder(
            len(exporter.objs), eye_obj_name.index(), BAD_INDEX, BAD_INDEX, eye_anim_group.index())
        exporter.objs.append(eye_obj)

        lookat_obj_name = exporter.create_name(cam.name+".lookat.obj")
        lookat_obj = niff2_obj_node_builder(len(exporter.objs),
                                            lookat_obj_name.index(),
                                            BAD_INDEX,
                                            BAD_INDEX,
                                            lookat_anim_group.index())
        exporter.objs.append(lookat_obj)

        up_obj_name = exporter.create_name(cam.name+".up.obj")
        up_obj = niff2_obj_node_builder(
            len(exporter.objs), up_obj_name.index(), BAD_INDEX, BAD_INDEX, up_anim_group.index())
        exporter.objs.append(up_obj)

        cam_name = exporter.create_name(cam.name+".cam")
        cam_node = niff2_cam_node_builder(
            cam_index, cam_name.index(), eye_obj.index(), lookat_obj.index(), up_obj.index())
        cams.append(cam_node)

    # NIFF2 Env
    envs = []
    env_name = exporter.create_name(filename+".env")
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

        light_name = exporter.create_name(light.name+".light")

        light_node = niff2_light_node_builder(len(lights),
                                              light_name.index(),
                                              correct_gamma(
                                                  [0.05, 0.05, 0.05]),
                                              correct_gamma(light.color),
                                              matrix[2].xyz)
        lights.append(light_node)

    # NIFF2 Header
    scene_header = niff2_scene_header_builder(
        scene_name.index(), exporter.objs, cams, envs, lights)
    env_list_header = niff2_env_list_header_builder(envs)
    cam_list_header = niff2_cam_list_header_builder(cams)
    light_list_header = niff2_light_list_header_builder(lights)
    obj_list_header = niff2_obj_list_header_builder(exporter.objs)
    shape_list_header = niff2_shape_list_header_builder(exporter.shapes)
    vtx_list_header = niff2_vtx_list_header_builder(exporter.vtx_groups)
    tri_list_header = niff2_tri_list_header_builder(exporter.tri_groups)
    color_list_header = niff2_color_list_header_builder(
        exporter.tri_color_groups, exporter.vtx_color_groups)
    vector_list_header = niff2_vector_list_header_builder(
        exporter.tri_nv_groups, exporter.vtx_nv_groups)
    st_list_header = niff2_st_list_header_builder(exporter.st_groups)
    part_list_header = niff2_part_list_header_builder(exporter.parts)
    mat_list_header = niff2_mat_list_header_builder(exporter.materials)
    tex_list_header = niff2_tex_list_header_builder(exporter.textures)
    tex_img_list_header = niff2_tex_img_list_header_builder(
        exporter.tex_images)
    anim_list_header = niff2_anim_list_header_builder(exporter.anim_groups)
    coll_list_header = niff2_coll_list_header_builder()
    switch_list_header = niff2_switch_list_header_builder()
    name_list_header = niff2_name_list_header_builder(exporter.names)
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

    file_header = niff2_file_header_builder(file_size)
    file_header.scene_list_num_byte = scene_header.num_bytes()
    file_header.env_list_num_byte = env_list_header.num_bytes()
    file_header.cam_list_num_byte = cam_list_header.num_bytes()
    file_header.light_list_num_byte = light_list_header.num_bytes()
    file_header.obj_list_num_byte = obj_list_header.num_bytes()
    file_header.shape_list_num_byte = shape_list_header.num_bytes()
    file_header.vtx_list_num_byte = vtx_list_header.num_bytes()
    file_header.tri_list_num_byte = tri_list_header.num_bytes()
    file_header.color_list_num_byte = color_list_header.num_bytes()
    file_header.vector_list_num_byte = vector_list_header.num_bytes()
    file_header.st_list_num_byte = st_list_header.num_bytes()
    file_header.part_list_num_byte = part_list_header.num_bytes()
    file_header.mat_list_num_byte = mat_list_header.num_bytes()
    file_header.tex_list_num_byte = tex_list_header.num_bytes()
    file_header.tex_img_list_num_byte = tex_img_list_header.num_bytes()
    file_header.anim_list_num_byte = anim_list_header.num_bytes()
    file_header.coll_list_num_byte = coll_list_header.num_bytes()
    file_header.switch_list_num_byte = switch_list_header.num_bytes()
    file_header.name_list_num_byte = name_list_header.num_bytes()
    file_header.ci_img_list_num_byte = ci_img_list_header.num_bytes()
    file_header.color_palette_list_num_byte = color_palette_list_header.num_bytes()
    file_header.envelope_list_num_byte = envelope_list_header.num_bytes()
    file_header.cluster_list_num_byte = cluster_list_header.num_bytes()
    file_header.weight_list_num_byte = weight_list_header.num_bytes()
    file_header.chain_root_list_num_byte = chain_root_list_header.num_bytes()
    file_header.joint_list_num_byte = joint_list_header.num_bytes()
    file_header.effector_list_num_byte = effector_list_header.num_bytes()
    file_header.external_name_list_num_byte = external_name_list_header.num_bytes()

    buf = bytearray()
    niff2_file_header_writer(file_header, buf)

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

    niff2_obj_list_header_writer(obj_list_header, exporter.objs, buf)
    for obj in exporter.objs:
        niff2_obj_node_writer(obj, buf)

    niff2_shape_list_header_writer(shape_list_header, exporter.shapes, buf)
    for shape in exporter.shapes:
        niff2_shape_node_writer(shape, buf)

    niff2_vtx_list_header_writer(vtx_list_header, exporter.vtx_groups, buf)
    for vtx_group in exporter.vtx_groups:
        niff2_vtx_group_node_writer(vtx_group, buf)

    niff2_tri_list_header_writer(tri_list_header, exporter.tri_groups, buf)
    for tri_group in exporter.tri_groups:
        niff2_tri_group_writer(tri_group, buf)

    niff2_color_list_header_writer(
        color_list_header, exporter.tri_color_groups, exporter.vtx_color_groups, buf)
    for tri_color_group in exporter.tri_color_groups:
        niff2_tri_color_group_node_writer(tri_color_group, buf)
    for vtx_color_group in exporter.vtx_color_groups:
        niff2_vtx_color_group_node_writer(vtx_color_group, buf)

    niff2_vector_list_header_writer(
        vector_list_header, exporter.tri_nv_groups, exporter.vtx_nv_groups, buf)
    for tri_nv_group in exporter.tri_nv_groups:
        niff2_tri_nv_group_writer(tri_nv_group, buf)
    for vtx_nv_group in exporter.vtx_nv_groups:
        niff2_vtx_nv_group_writer(vtx_nv_group, buf)

    niff2_st_list_header_writer(st_list_header, exporter.st_groups, buf)
    for st_group in exporter.st_groups:
        niff2_st_group_writer(st_group, buf)

    niff2_part_list_header_writer(part_list_header, exporter.parts, buf)
    for part in exporter.parts:
        niff2_part_node_writer(part, buf)

    niff2_mat_list_header_writer(mat_list_header, exporter.materials, buf)
    for mat in exporter.materials:
        niff2_mat_node_writer(mat, buf)

    niff2_tex_list_header_writer(tex_list_header, exporter.textures, buf)
    for tex in exporter.textures:
        niff2_tex_node_writer(tex, buf)

    niff2_tex_img_list_header_writer(
        tex_img_list_header, exporter.tex_images, buf)
    for tex_img in exporter.tex_images:
        niff2_tex_img_node_writer(tex_img, buf)

    niff2_anim_list_header_writer(anim_list_header, exporter.anim_groups, buf)
    for anim_group in exporter.anim_groups:
        niff2_anim_group_writer(anim_group, buf)

    niff2_coll_list_header_writer(coll_list_header, buf)
    niff2_switch_list_header_writer(switch_list_header, buf)

    niff2_name_list_header_writer(name_list_header, exporter.names, buf)
    for name in exporter.names:
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

    file = open(filepath, 'wb')
    file.write(buf)
    file.close()

    return {'FINISHED'}
