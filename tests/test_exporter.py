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
