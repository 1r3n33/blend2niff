"""Tests about creating .nif data from Blender data."""

import unittest
from bpy.types import (Material,
                       Mesh,
                       MeshLoop,
                       MeshLoopColor,
                       MeshLoopColorLayer,
                       MeshLoopTriangle,
                       MeshVertex,
                       Object)
from blend2niff.exporter import Exporter


class TestExporter(unittest.TestCase):
    def test_create_name(self):
        exporter = Exporter()
        hello = exporter.create_name("hello")
        world = exporter.create_name("world")

        self.assertEqual(exporter.names, [hello, world])

    def test_create_materials(self):
        not_a_mesh = Object()
        mesh_with_0_mat = Object()
        mesh_with_1_mat = Object()
        mesh_with_2_mat = Object()

        mesh_with_0_mat.data = Mesh()
        mesh_with_1_mat.data = Mesh()
        mesh_with_2_mat.data = Mesh()

        material = Material()
        material.name = "material"
        material.diffuse_color = [1.0, 1.0, 1.0, 1.0]

        mesh_with_0_mat.data.materials = []
        mesh_with_1_mat.data.materials = [material]*1
        mesh_with_2_mat.data.materials = [material]*2

        exporter = Exporter()
        exporter.create_materials([not_a_mesh,
                                   mesh_with_0_mat,
                                   mesh_with_1_mat,
                                   mesh_with_2_mat])

        self.assertEqual(
            len(exporter.names), 4)
        self.assertEqual(
            len(exporter.materials), 4)
        self.assertEqual(
            exporter.materials[0], exporter.get_default_material())
        self.assertEqual(
            not_a_mesh.data in exporter.materials_by_mesh, False)
        self.assertEqual(
            len(exporter.materials_by_mesh[mesh_with_0_mat.data]), 0)
        self.assertEqual(
            len(exporter.materials_by_mesh[mesh_with_1_mat.data]), 1)
        self.assertEqual(
            len(exporter.materials_by_mesh[mesh_with_2_mat.data]), 2)

    def test_get_default_material(self):
        exporter = Exporter()
        exporter.create_materials([])

        self.assertEqual(
            exporter.materials[0], exporter.get_default_material())
        self.assertEqual(
            exporter.materials[0].this_mat_index, 0)

    def test_create_vertex_groups(self):
        not_a_mesh = Object()
        mesh = Object()

        mesh.data = Mesh()
        mesh.data.name = "mesh"

        vertex = MeshVertex()
        vertex.co = [0.0, 0.0, 0.0]

        mesh.data.vertices = [vertex]*10

        exporter = Exporter()
        exporter.create_vertex_groups([not_a_mesh, mesh])

        self.assertEqual(len(exporter.names), 1)
        self.assertEqual(len(exporter.vtx_groups), 1)
        self.assertEqual(
            not_a_mesh.data in exporter.vtx_group_by_mesh, False)
        self.assertEqual(
            exporter.vtx_group_by_mesh[mesh.data], exporter.vtx_groups[0])

    def test_create_color_groups(self):
        not_a_mesh = Object()
        mesh_with_vtx_colors = Object()
        mesh_without_vtx_colors = Object()

        mesh_with_vtx_colors.data = Mesh()
        mesh_without_vtx_colors.data = Mesh()

        vertex = MeshVertex()
        mesh_with_vtx_colors.data.vertices = [vertex]*3
        mesh_without_vtx_colors.data.vertices = [vertex]*3

        red = MeshLoopColor()
        red.color = [1.0, 0.0, 0.0, 1.0]
        green = MeshLoopColor()
        green.color = [0.0, 1.0, 0.0, 1.0]
        blue = MeshLoopColor()
        blue.color = [0.0, 0.0, 1.0, 1.0]

        vertex_colors = MeshLoopColorLayer()
        vertex_colors.data = [red, green, blue]
        mesh_with_vtx_colors.data.vertex_colors = [vertex_colors]
        mesh_without_vtx_colors.data.vertex_colors = []

        tri = MeshLoopTriangle()
        tri.vertices = [0, 1, 2]
        tri.loops = [0, 1, 2]
        mesh_with_vtx_colors.data.loop_triangles = [tri]
        mesh_without_vtx_colors.data.loop_triangles = [tri]

        exporter = Exporter()
        exporter.create_color_groups([not_a_mesh,
                                      mesh_with_vtx_colors,
                                      mesh_without_vtx_colors])

        self.assertEqual(len(exporter.tri_color_groups),
                         len(exporter.vtx_color_groups))
        self.assertEqual(exporter.tri_color_groups[0].tri_color_num, 1)
        self.assertEqual(exporter.tri_color_groups[1].tri_color_num, 1)
        self.assertEqual(exporter.tri_color_groups[2].tri_color_num, 1)
        self.assertEqual(exporter.vtx_color_groups[0].vtx_color_num, 1)
        self.assertEqual(exporter.vtx_color_groups[1].vtx_color_num, 3)
        self.assertEqual(exporter.vtx_color_groups[2].vtx_color_num, 1)

    def test_create_vector_groups(self):
        not_a_mesh = Object()
        mesh = Object()

        mesh.data = Mesh()

        vertex = MeshVertex()
        mesh.data.vertices = [vertex]*3

        n_x = MeshLoop()
        n_x.normal = [1.0, 0.0, 0.0]
        n_y = MeshLoop()
        n_y.normal = [0.0, 1.0, 0.0]
        n_z = MeshLoop()
        n_z.normal = [0.0, 0.0, 1.0]
        mesh.data.loops = [n_x, n_y, n_z]

        tri = MeshLoopTriangle()
        tri.vertices = [0, 1, 2]
        tri.loops = [0, 1, 2]
        mesh.data.loop_triangles = [tri]

        exporter = Exporter()
        exporter.create_vector_groups([not_a_mesh, mesh])

        self.assertEqual(len(exporter.tri_nv_groups),
                         len(exporter.vtx_nv_groups))
        self.assertEqual(exporter.tri_nv_groups[0].tri_nv_num, 1)
        self.assertEqual(exporter.tri_nv_groups[1].tri_nv_num, 1)
        self.assertEqual(exporter.vtx_nv_groups[0].vtx_nv_num, 1)
        self.assertEqual(exporter.vtx_nv_groups[1].vtx_nv_num, 3)

    def test_create_st_groups(self):
        exporter = Exporter()
        exporter.create_st_groups()
        self.assertEqual(exporter.st_groups[0].st_num, 1)

    def test_create_tri_groups(self):
        not_a_mesh = Object()
        mesh = Object()

        mesh.data = Mesh()
        mesh.data.name = "mesh"

        vertex = MeshVertex()
        vertex.co = [0.0, 0.0, 0.0]

        mesh.data.vertices = [vertex]*3

        tri = MeshLoopTriangle()
        tri.vertices = [0, 1, 2]
        mesh.data.loop_triangles = [tri]

        exporter = Exporter()
        exporter.create_vertex_groups([not_a_mesh, mesh])
        exporter.create_tri_groups([not_a_mesh, mesh])

        self.assertEqual(len(exporter.tri_groups), 1)
        self.assertEqual(
            not_a_mesh.data in exporter.tri_group_by_mesh, False)
        self.assertEqual(
            exporter.tri_group_by_mesh[mesh.data], exporter.tri_groups[0])

    def test_create_parts(self):
        obj = Object()

        mesh = Mesh()
        mesh.name = "mesh"
        obj.data = mesh

        mat_red = Material()
        mat_red.name = "red"
        mat_red.diffuse_color = [1.0, 0.0, 0.0, 1.0]

        mat_green = Material()
        mat_green.name = "green"
        mat_green.diffuse_color = [0.0, 1.0, 0.0, 1.0]

        mat_blue = Material()
        mat_blue.name = "blue"
        mat_blue.diffuse_color = [0.0, 0.0, 1.0, 1.0]

        mesh.materials = [mat_red, mat_green, mat_blue]

        vertex = MeshVertex()
        vertex.co = [0.0, 0.0, 0.0]

        mesh.vertices = [vertex]*9

        tri_red = MeshLoopTriangle()
        tri_red.vertices = [0, 1, 2]
        tri_red.material_index = 0

        tri_green = MeshLoopTriangle()
        tri_green.vertices = [3, 4, 5]
        tri_green.material_index = 1

        tri_blue = MeshLoopTriangle()
        tri_blue.vertices = [6, 7, 8]
        tri_blue.material_index = 2

        mesh.loop_triangles = [tri_red, tri_green, tri_blue]

        exporter = Exporter()
        exporter.create_materials([obj])
        exporter.create_vertex_groups([obj])
        exporter.create_tri_groups([obj])
        exporter.create_parts([obj])

        self.assertEqual(
            exporter.parts[0].mat_index, exporter.materials[1].this_mat_index)
        self.assertEqual(
            exporter.parts[1].mat_index, exporter.materials[2].this_mat_index)
        self.assertEqual(
            exporter.parts[2].mat_index, exporter.materials[3].this_mat_index)
        self.assertEqual(
            exporter.parts[0].tri_indices, [exporter.tri_groups[0].tris[0].this_tri_index])
        self.assertEqual(
            exporter.parts[1].tri_indices, [exporter.tri_groups[0].tris[1].this_tri_index])
        self.assertEqual(
            exporter.parts[2].tri_indices, [exporter.tri_groups[0].tris[2].this_tri_index])
        self.assertEqual(exporter.parts_by_mesh[mesh], exporter.parts)

    def test_create_shapes(self):
        obj = Object()

        mesh = Mesh()
        mesh.name = "mesh"
        obj.data = mesh

        mat_red = Material()
        mat_red.name = "red"
        mat_red.diffuse_color = [1.0, 0.0, 0.0, 1.0]

        mesh.materials = [mat_red]

        vertex = MeshVertex()
        vertex.co = [0.0, 0.0, 0.0]

        mesh.vertices = [vertex]*3

        tri_red = MeshLoopTriangle()
        tri_red.vertices = [0, 1, 2]
        tri_red.material_index = 0

        mesh.loop_triangles = [tri_red]

        exporter = Exporter()
        exporter.create_materials([obj])
        exporter.create_vertex_groups([obj])
        exporter.create_tri_groups([obj])
        exporter.create_parts([obj])
        exporter.create_shapes([obj])

        self.assertEqual(
            exporter.shapes[0].shape_tri_link,
            exporter.tri_groups[0].this_tri_group_index)
        self.assertEqual(
            exporter.shapes[0].shape_mat_link,
            exporter.get_default_material().this_mat_index)
        self.assertEqual(exporter.shapes[0].shape_part_num, 1)
        self.assertEqual(exporter.shape_by_mesh[mesh], exporter.shapes[0])

    def test_create_anim_groups(self):
        obj = Object()
        obj.name = "obj"

        obj.data = Mesh()

        obj.location = [1.0, 2.0, 3.0]
        obj.rotation_euler = [4.0, 5.0, 6.0]
        obj.scale = [7.0, 8.0, 9.0]

        exporter = Exporter()
        exporter.create_anim_groups([obj])

        self.assertEqual(exporter.anim_groups[0].anim_node.translate_x, 1.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.translate_y, 2.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.translate_z, 3.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.rotate_axis_x, 4.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.rotate_axis_y, 5.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.rotate_axis_z, 6.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.scale_x, 7.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.scale_y, 8.0)
        self.assertEqual(exporter.anim_groups[0].anim_node.scale_z, 9.0)
        self.assertEqual(
            exporter.anim_group_by_mesh[obj.data], exporter.anim_groups[0])

    def test_create_objects(self):
        obj = Object()
        obj.name = "obj"

        mesh = Mesh()
        mesh.name = "mesh"

        obj.data = mesh
        obj.location = [1.0, 2.0, 3.0]
        obj.rotation_euler = [4.0, 5.0, 6.0]
        obj.scale = [7.0, 8.0, 9.0]

        mat_red = Material()
        mat_red.name = "red"
        mat_red.diffuse_color = [1.0, 0.0, 0.0, 1.0]

        mesh.materials = [mat_red]

        vertex = MeshVertex()
        vertex.co = [0.0, 0.0, 0.0]

        mesh.vertices = [vertex]*3

        tri_red = MeshLoopTriangle()
        tri_red.vertices = [0, 1, 2]
        tri_red.material_index = 0

        mesh.loop_triangles = [tri_red]

        exporter = Exporter()
        exporter.create_materials([obj])
        exporter.create_vertex_groups([obj])
        exporter.create_tri_groups([obj])
        exporter.create_parts([obj])
        exporter.create_shapes([obj])
        exporter.create_anim_groups([obj])
        exporter.create_objects([obj])

        self.assertEqual(
            exporter.objs[0].obj_shape_link,
            exporter.shapes[0].this_shape_index)
        self.assertEqual(
            exporter.objs[0].obj_mat_link,
            exporter.materials[0].this_mat_index)
        self.assertEqual(
            exporter.objs[0].obj_anim_link,
            exporter.anim_groups[0].this_anim_group_index)
        self.assertEqual(
            exporter.objs[0].obj_shape_link,
            exporter.shape_by_mesh[mesh].this_shape_index)
        self.assertEqual(
            exporter.objs[0].obj_mat_link,
            exporter.get_default_material().this_mat_index)
        self.assertEqual(
            exporter.objs[0].obj_anim_link,
            exporter.anim_group_by_mesh[mesh].this_anim_group_index)
