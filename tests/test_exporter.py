"""Tests about creating .nif file from Blender data."""

import unittest
from bpy.types import (Material, Mesh, Object)
from blend2niff.exporter import Exporter


class TestExporter(unittest.TestCase):
    def test_create_name(self):
        exporter = Exporter()

        hello = exporter.create_name("hello")
        world = exporter.create_name("world")
        self.assertEqual(exporter.names, [hello, world])

    def test_create_materials(self):
        exporter = Exporter()

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
