"""Add-on entry point."""

if "bpy" in locals():
    from importlib import reload
    reload(blend2niff.operator)
    del reload

import bpy
from blend2niff.operator import N64Niff2Export


bl_info = {
    "name": "N64 NIFF2 Exporter",
    "description": "Export to N64 NIFF2 format",
    "author": "https://github.com/1r3n33",
    "category": "Import-Export",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "File > Export > N64 NIFF2 (.nif)"
}


def menu_func_export(self, _):
    self.layout.operator(N64Niff2Export.bl_idname,
                         text="N64 NIFF2 (.nif)")


def register():
    bpy.utils.register_class(N64Niff2Export)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(N64Niff2Export)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
    bpy.ops.export.to_n64_niff2('INVOKE_DEFAULT')
