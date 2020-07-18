"""Blender operator to export to N64 NIFF2 format."""

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from blend2niff.exporter.niff2_exporter import write_niff2


class N64Niff2Export(Operator, ExportHelper):

    # Used to call bpy.ops.export.to_n64_niff2
    bl_idname = "export.to_n64_niff2"

    bl_label = "Export to N64 NIFF2"

    bl_description = "Export to N64 NIFF2"

    # ExportHelper mixin class uses this
    filename_ext = ".nif"

    filter_glob: StringProperty(
        default="*.nif",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, _):
        return write_niff2(bpy.data, self.filepath)
