import bpy

class ds_3d_view_edit(bpy.types.Operator):
    bl_idname = "ds_3d_view.edit"
    bl_label = "ds_3d_view.edit"
    def execute(self, context):  
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        return {'FINISHED'}

class ds_3d_view_object(bpy.types.Operator):
    bl_idname = "ds_3d_view.object"
    bl_label = "ds_3d_view.object"
    def execute(self, context): 
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}

class ds_3d_view_edit_face_delete(bpy.types.Operator):
    bl_idname = "ds_3d_view.edit_face_delete"
    bl_label = "ds_3d_view.edit_face_delete"
    def execute(self, context):
        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}

class ds_3d_view_edit_edge_delete(bpy.types.Operator):
    bl_idname = "ds_3d_view.edit_edge_delete"
    bl_label = "ds_3d_view.edit_edge_delete"
    def execute(self, context):
        bpy.ops.mesh.delete(type='EDGE')
        return {'FINISHED'}

class ds_3d_view_edit_vertex_delete(bpy.types.Operator):
    bl_idname = "ds_3d_view.edit_vertex_delete"
    bl_label = "ds_3d_view.edit_vertex_delete"
    def execute(self, context):
        bpy.ops.mesh.delete(type='VERT')
        return {'FINISHED'}

class ds_3d_view_select_all(bpy.types.Operator):
    bl_idname = "ds_3d_view.select_all"
    bl_label = "ds_3d_view.select_all"
    def execute(self, context):
        _scene = bpy.context.scene
        if bpy.context.active_object.mode=='OBJECT':
            for ob in _scene.objects:
                if ob.type == 'MESH':
                    ob.select = True
        elif bpy.context.active_object.mode=='EDIT':
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_all(action='SELECT')
        return {'FINISHED'}

class ds_3d_view_select_none(bpy.types.Operator):
    bl_idname = "ds_3d_view.select_none"
    bl_label = "ds_3d_view.select_none"
    def execute(self, context):
        _scene = bpy.context.scene
        if bpy.context.active_object.mode=='OBJECT':
            for ob in _scene.objects:
                if ob.type == 'MESH':
                    ob.select = False
        elif bpy.context.active_object.mode=='EDIT':
            bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}

class ds_3d_view_menu_toggle(bpy.types.Operator):
    bl_idname = "ds_3d_view.menu_toggle"
    bl_label = "Menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):

        if not bpy.context.user_preferences.addons[__package__].preferences.option_show_menu_toggle_state:
                bpy.context.user_preferences.addons[__package__].preferences.option_show_menu_toggle_state=True
        else:
                bpy.context.user_preferences.addons[__package__].preferences.option_show_menu_toggle_state=False
        
        return {'FINISHED'}