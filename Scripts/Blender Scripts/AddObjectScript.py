import bpy

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    
    def execute(self, context):
        bpy.context.scene.render.image_settings.file_format = 'JPEG'
        bpy.context.scene.render.filepath = '/afs/csl.tjhsst.edu/students/2023/2023ojeyapra/Blender/TestImages/'
        bpy.ops.render.render(use_viewport = True, write_still = True) 
        
        print("Someone Clicked Me!")
        self.report({'INFO'}, "Yo")
        return {'FINISHED'}
    
class TestPanel(bpy.types.Panel):
    bl_label = "Test Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NewTab'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        row.label(text = "Sample Text", icon = 'CUBE')
        row = layout.row()
        row.operator("object.simple_operator", text = "Render and Export", icon = 'RENDER_STILL')      
        
#def menu_func(self, context):
#    self.layout.operator(SimpleOperator.bl_idname, text = "It's me, an Operator") 
#    
#bpy.types.VIEW3D_MT_view.append(menu_func)

def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(SimpleOperator)

def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(SimpleOperator)
    
if __name__ == "__main__":
    register()
