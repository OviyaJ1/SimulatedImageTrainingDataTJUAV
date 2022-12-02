import bpy


def write_some_data(context, filepath, use_some_setting):
    bpy.context.scene.render.filepath = '/afs/csl.tjhsst.edu/students/2023/2023ojeyapra/Blender/TestImages/'
    bpy.ops.render.render(animation = False, write_still = True, use_viewport = True)
    bpy.ops.render.view_show()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    def execute(self, context):
        bpy.context.scene.render.filepath = '/afs/csl.tjhsst.edu/students/2023/2023ojeyapra/Blender/TestImages/'
        bpy.ops.render.render(animation = False, write_still = True, use_viewport = True)
        bpy.ops.render.view_show()

        return {'FINISHED'}


class RenderPanel(bpy.types.Panel):
    bl_label = "New Render Panel"
    bl_idname = "PT_RenderPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NewTab'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        row.label(text = "Sample Text", icon = 'SPHERE')
        row = layout.row()
        row.operator("export_test.some_data", text = "Render and Export", icon = 'RENDER_STILL')  

# Only needed if you want to add into a dynamic menu  
#def menu_func_export(self, context):
    #self.layout.operator(ExportSomeData.bl_idname, text="Text Export Operator")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(RenderPanel)


def unregister():
    bpy.utils.unregister_class(RenderPanel)


if __name__ == "__main__":
    register()
