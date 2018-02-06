# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from . import ds_ui 

# Menus

class menu_meshes(bpy.types.Menu):
    bl_label = "Meshes"
    bl_idname = "ds_uv.menu_meshes"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH' and ob.hide==False:
                layout.operator('ds_uv.menu_mesh_select',text=ob.name).option_value=ob.name

class menu_mesh_select(bpy.types.Operator):
    bl_label = "UV Select"
    bl_idname = "ds_uv.menu_mesh_select"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        if bpy.context.active_object:

            if bpy.context.active_object.mode=='EDIT':
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        
        ob = bpy.data.objects.get(self.option_value)
        context.scene.objects.active = ob
        ob.select = True

        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_uv_select_edit'):
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_uv_select_all'):
            bpy.ops.mesh.select_all(action='SELECT')
        else:        
            bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}

# Functions

class uv_unwrap(bpy.types.Operator):
    bl_idname = "ds_ui.uv_unwrap"
    bl_label = "ds_ui.uv_unwrap"
    def execute(self, context):
        ds_ui.select_all.execute(self, context)
        bpy.ops.uv.unwrap()
        return {'FINISHED'}


# UI

class ui_layout(bpy.types.Operator):

    bl_idname = "ds_uv.ui_layout"
    bl_label = "Toggle"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def execute(self, context):

        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_ui_mode','uv')

        if bpy.context.scene.objects.active:
            bpy.context.scene.objects.active.show_x_ray=False
        bpy.context.window.screen = bpy.data.screens['UV Editing']

        if not len(bpy.context.selected_objects):

            if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_uv_select'):
                bpy.ops.object.select_all(action='DESELECT')
                for ob in context.scene.objects:
                    if ob.type == 'MESH':
                        context.scene.objects.active = ob
                        ob.select = True
                        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_uv_select_edit'):
                            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_uv_select_all'):
                            bpy.ops.mesh.select_all(action='SELECT')
                        else:        
                            bpy.ops.mesh.select_all(action='DESELECT')
                        break
        elif bpy.context.active_object and bpy.context.active_object.type == 'MESH':

            if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_edit'):
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            if bpy.context.active_object.mode=='EDIT':

                if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_all'):
                    bpy.ops.mesh.select_all(action='SELECT')
                else:        
                    bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}

def menu(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    layout.menu('ds_uv.menu_meshes',icon="TRIA_DOWN")

    if _obj_mode=='EDIT_MESH':

        layout.menu("VIEW3D_MT_edit_mesh",icon='COLLAPSEMENU')

    layout.menu("VIEW3D_MT_uv_map",icon='COLLAPSEMENU')

    if _obj_mode=='OBJECT':
        layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'
    elif _obj_mode=='EDIT_MESH':
        layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'

def tools(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    if _obj_mode=='EDIT_MESH':

        layout.operator("mesh.select_mode", text="", icon='EDGESEL').type = 'EDGE'

        _mesh=_obj.data
        _selected = True

        _selected_vertices = False
        _selected_edges = False
        _selected_faces = False
        
        _select_mode=bpy.context.scene.tool_settings.mesh_select_mode

        if _select_mode[0]:
            _selected_vertices=True
        if _select_mode[1]:
            _selected_edges=True
        if _select_mode[2]:
            _selected_faces=True

        if _selected_edges:

            layout.operator("mesh.edge_split", text='Split')
            layout.operator("mesh.loop_multi_select", text='Loop').ring=False
            layout.operator("mesh.loop_multi_select", text='Ring').ring=True

    if _obj_mode=='EDIT_MESH':

        layout.operator('mesh.mark_seam',text="M",icon="EDGESEL").clear = False
        layout.operator('mesh.mark_seam',text="U",icon="EDGESEL").clear = True
        layout.operator('uv.unwrap',text="Unwrap",icon="MOD_UVPROJECT")
        layout.operator('ds_ui.uv_unwrap',text="Unwrap ALL",icon="MOD_UVPROJECT")

def register():

    from bpy.utils import register_class

    register_class(ui_layout)

    register_class(menu_meshes)
    register_class(menu_mesh_select)

    register_class(uv_unwrap)

def unregister():

    from bpy.utils import unregister_class

    unregister_class(ui_layout)

    unregister_class(menu_meshes)
    unregister_class(menu_mesh_select)

    unregister_class(uv_unwrap)
