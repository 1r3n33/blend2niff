"""Test Blender operator to export to N64 NIFF2 format."""

import unittest
from unittest.mock import patch

import bpy
from blend2niff.operator import N64Niff2Export


class TestOperator(unittest.TestCase):
    @patch('blend2niff.operator.write_niff2', return_value={'FINISHED'})
    def test_execute_operator(self, write_niff2):
        operator = N64Niff2Export()
        operator.filepath = "path/to/file"

        res = operator.execute(None)

        self.assertEqual(res, {'FINISHED'})
        write_niff2.assert_called_once_with(bpy.data, "path/to/file")
