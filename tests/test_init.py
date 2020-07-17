"""Test Add-on register/unregister."""

import unittest
from unittest.mock import Mock

import bpy
from blend2niff import register, unregister, menu_func_export
from blend2niff.operator import N64Niff2Export


class TestInit(unittest.TestCase):
    def test_register_addon(self):
        bpy.utils = Mock()
        bpy.types.TOPBAR_MT_file_export = Mock()

        register()
        bpy.utils.register_class.assert_called_once_with(N64Niff2Export)
        bpy.types.TOPBAR_MT_file_export.append.assert_called_once_with(
            menu_func_export)

    def test_unregister_addon(self):
        bpy.utils = Mock()
        bpy.types.TOPBAR_MT_file_export = Mock()

        unregister()
        bpy.utils.unregister_class.assert_called_once_with(N64Niff2Export)
        bpy.types.TOPBAR_MT_file_export.remove.assert_called_once_with(
            menu_func_export)
