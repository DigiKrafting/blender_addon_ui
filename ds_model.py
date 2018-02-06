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
    bl_idname = "ds_model.menu_meshes"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH' and ob.hide==False:
                layout.operator('ds_model.menu_mesh_select',text=ob.name).option_value=ob.name

class menu_mesh_select(bpy.types.Operator):
    bl_label = "Mesh Select"
    bl_idname = "ds_model.menu_mesh_select"
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
        
        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_edit'):
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_all'):
            bpy.ops.mesh.select_all(action='SELECT')
        else:        
            bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}    

# Functions

class edit_mesh_extrude_x(bpy.types.Operator):
    bl_idname = "ds_model.edit_mesh_extrude_x"
    bl_label = "ds_model.edit_mesh_extrude_x"
    def execute(self, context):  
        bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (True, False, False)})
        return {'FINISHED'}

class edit_mesh_extrude_y(bpy.types.Operator):
    bl_idname = "ds_model.edit_mesh_extrude_y"
    bl_label = "ds_model.edit_mesh_extrude_y"
    def execute(self, context):  
        bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, True, False)})
        return {'FINISHED'}

class edit_mesh_extrude_z(bpy.types.Operator):
    bl_idname = "ds_model.edit_mesh_extrude_z"
    bl_label = "ds_model.edit_mesh_extrude_z"
    def execute(self, context):  
        bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, False, True)})
        return {'FINISHED'}

class edit_faces_tris(bpy.types.Operator):
    bl_idname = "ds_model.edit_faces_tris"
    bl_label = "ds_model.edit_faces_tris"
    def execute(self, context):  
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        bpy.ops.mesh.select_face_by_sides(number=3, type='EQUAL')
        return {'FINISHED'}

class edit_faces_quads(bpy.types.Operator):
    bl_idname = "ds_model.edit_faces_quads"
    bl_label = "ds_model.edit_faces_quads"
    def execute(self, context):  
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        bpy.ops.mesh.select_face_by_sides(number=4, type='EQUAL')
        return {'FINISHED'}

# Sculpt

class sculpt_brush(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        layout = self.layout

        _brush = self.option_value

        if _brush=='Inflate':
            _brush='Inflate/Deflate'
            bpy.data.brushes["Inflate/Deflate"].direction = 'INFLATE'
        elif _brush=='Deflate':
            _brush='Inflate/Deflate'
            bpy.data.brushes["Inflate/Deflate"].direction = 'DEFLATE'
        elif _brush=='Flatten':
            _brush='Flatten/Contrast'
            bpy.data.brushes["Flatten/Contrast"].direction = 'FLATTEN'

        context.tool_settings.sculpt.brush = bpy.data.brushes[_brush]

        return {'FINISHED'}    

class sculpt_brush_radius_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush_radius_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size < 500:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size+10

        return {'FINISHED'}    

class sculpt_brush_radius_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush_radius_dec"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size > 10:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size-10

        return {'FINISHED'}    

class sculpt_brush_radius_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush_radius_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.size=35

        return {'FINISHED'}    

class sculpt_brush_strength_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush_strength_inc"
  
    def execute(self, context):

        if context.tool_settings.sculpt.brush.strength < 1:
            context.tool_settings.sculpt.brush.strength=context.tool_settings.sculpt.brush.strength+0.100

        return {'FINISHED'}    

class sculpt_brush_strength_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush_strength_dec"
  
    def execute(self, context):

        if context.tool_settings.sculpt.brush.strength > 0:
            context.tool_settings.sculpt.brush.strength=context.tool_settings.sculpt.brush.strength-0.100

        return {'FINISHED'}    

class sculpt_brush_strength_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_model.sculpt_brush_strength_default"
  
    def execute(self, context):

        context.tool_settings.sculpt.brush.strength=0.200

        return {'FINISHED'} 

# UI

class ui_layout(bpy.types.Operator):

    bl_idname = "ds_model.ui_layout"
    bl_label = "Toggle"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def execute(self, context):

        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_ui_mode','model')

        if bpy.context.scene.objects.active:
            bpy.context.scene.objects.active.show_x_ray=False
        bpy.context.window.screen = bpy.data.screens['Default']

        for ob in context.scene.objects:
            if ob.type == 'ARMATURE':
                ob.hide=True

        if bpy.context.user_preferences.addons[__package__].preferences.active_object_name!='':
            
            ob = bpy.context.scene.objects[bpy.context.user_preferences.addons[__package__].preferences.active_object_name]
            bpy.context.scene.objects.active = ob
            ob.select=True
            print(bpy.context.user_preferences.addons[__package__].preferences.active_object_mode)
            bpy.ops.object.mode_set(mode=bpy.context.user_preferences.addons[__package__].preferences.active_object_mode, toggle=False)

        x=0
        if x==1:


            _selected=False
            for ob in bpy.context.selected_objects:
                if ob.type == 'MESH':
                    _selected=True

            if not _selected:
                
                if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select'):

                    if bpy.context.scene.objects.active:
                        bpy.ops.object.select_all(action='DESELECT')

                    for ob in context.scene.objects:
                        if ob.type == 'MESH':
                            context.scene.objects.active = ob
                            ob.select = True
                            if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_edit'):
                                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                            if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_all'):
                                bpy.ops.mesh.select_all(action='SELECT')
                            else:        
                                bpy.ops.mesh.select_all(action='DESELECT')
                            break

        elif bpy.context.active_object and bpy.context.active_object.type == 'MESH':

            #if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_edit'):
                #bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            if bpy.context.active_object.mode=='EDIT':

                if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_all'):
                    bpy.ops.mesh.select_all(action='SELECT')
                else:        
                    bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}

def menu(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    if context.scene.objects.active:

        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'active_object_name', context.scene.objects.active.name)
        _active_object_mode=_obj_mode
        if _active_object_mode=='EDIT_MESH':
            _active_object_mode='EDIT'
        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'active_object_mode', _active_object_mode)

    layout.menu('ds_model.menu_meshes',icon="TRIA_DOWN")

    if _obj_mode=='OBJECT' or _obj_mode=='EDIT_MESH':

        layout.menu("INFO_MT_mesh_add",icon='OUTLINER_OB_MESH')

    if _obj_mode=='EDIT_MESH':

        layout.menu("VIEW3D_MT_edit_mesh",icon='COLLAPSEMENU')

    if _obj_mode=='OBJECT':

        layout.menu("INFO_MT_curve_add", icon='OUTLINER_OB_CURVE')

    elif _obj_mode=='EDIT_CURVE':

        layout.menu("VIEW3D_MT_edit_curve",icon='COLLAPSEMENU')

    elif _obj_mode=='EDIT_MESH':

        _select_mode=bpy.context.scene.tool_settings.mesh_select_mode

        if _select_mode[0]:
            layout.menu("VIEW3D_MT_edit_mesh_vertices",icon='COLLAPSEMENU')
        if _select_mode[1]:
            layout.menu("VIEW3D_MT_edit_mesh_edges",icon='COLLAPSEMENU')
        if _select_mode[2]:
            layout.menu("VIEW3D_MT_edit_mesh_faces",icon='COLLAPSEMENU')

    if _obj and _obj.type=='MESH':

        if _obj_mode=='OBJECT':
            layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'
            #layout.operator('object.mode_set',text="Sculpt",icon="SCULPTMODE_HLT").mode='SCULPT'
            layout.operator('ds_ui.ui_layout_set_sculpt',text="Sculpt",icon="SCULPTMODE_HLT")
        elif _obj_mode=='EDIT_MESH':
            #layout.operator('ds_ui.ui_layout_set_object',text="Object",icon="OBJECT_DATAMODE")
            layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'
            layout.operator('ds_ui.ui_layout_set_sculpt',text="Sculpt",icon="SCULPTMODE_HLT")
        elif _obj_mode=='SCULPT':
            layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'
            #layout.operator('ds_ui.ui_layout_set_object',text="Object",icon="OBJECT_DATAMODE")
            layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'

def tools(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    ds_ui.tools_transform(context, layout)

    if _obj_mode=='EDIT_MESH':

        layout.operator("mesh.select_mode", text="", icon='VERTEXSEL').type = 'VERT'
        layout.operator("mesh.select_mode", text="", icon='EDGESEL').type = 'EDGE'
        layout.operator("mesh.select_mode", text="", icon='FACESEL').type = 'FACE'

        layout.operator('mesh.delete',text="",icon="VERTEXSEL").type = 'VERT'
        layout.operator('mesh.delete',text="",icon="EDGESEL").type = 'EDGE'
        layout.operator('mesh.delete',text="",icon="FACESEL").type = 'FACE'

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

        if (_selected_vertices or _selected_edges):
            
            layout.operator("mesh.edge_face_add")

        if _selected_edges:

            layout.operator("mesh.edge_split", text='Split')
            layout.operator("mesh.loop_multi_select", text='Loop').ring=False
            layout.operator("mesh.loop_multi_select", text='Ring').ring=True
            layout.operator('mesh.bevel',text="Bevel").vertex_only=False

        if (_selected_edges or _selected_faces):

            layout.operator('mesh.subdivide',text='SubD')
            layout.operator('mesh.unsubdivide',text='UnSubD')

        if _selected_faces:
            layout.operator('mesh.flip_normals',text="Flip Normals")
            layout.operator('mesh.solidify',text="Solidify")
            layout.operator('mesh.solidify',text="Solidify .005").thickness=0.005
            layout.operator('mesh.solidify',text="Solidify .010").thickness=0.010

        layout.operator('ds_model.edit_faces_tris',text="Tris")
        layout.operator('ds_model.edit_faces_quads',text="Quads")

    if _obj_mode=='OBJECT':

        if _obj:

            f=layout.operator("object.transform_apply")
            f.location=True
            f.rotation=True
            f.scale=True

            layout.operator("object.duplicate_move")
            layout.operator("object.join")
            layout.operator("object.delete")
            layout.operator("object.shade_smooth")
            layout.operator("object.shade_flat")

    if _obj_mode=='EDIT_MESH':

        if ds_ui.toggle_show('view3d_extrude'):
            layout.operator('ds_ui.toggle',icon='MOD_SHRINKWRAP',text="").option_toggle='view3d_extrude'
        
        if ds_ui.toggle_draw('view3d_extrude'):

            layout.operator("view3d.edit_mesh_extrude_move_normal", text='Normal')
            layout.operator('ds_model.edit_mesh_extrude_x', text="X Axis")
            layout.operator('ds_model.edit_mesh_extrude_y', text="Y Axis")
            layout.operator('ds_model.edit_mesh_extrude_z', text="Z Axis")

        if ds_ui.toggle_show('view3d_boolean'):
            layout.operator('ds_ui.toggle',icon='MOD_BOOLEAN',text="").option_toggle='view3d_boolean'
        
        if ds_ui.toggle_draw('view3d_boolean'):

            layout.operator('mesh.intersect_boolean',text="Diff").operation='DIFFERENCE'
            layout.operator('mesh.intersect_boolean',text="Intersect").operation='INTERSECT'
            layout.operator('mesh.intersect_boolean',text="Union").operation='UNION'

    if _obj_mode=='SCULPT':
    
        layout.operator('ds_model.sculpt_brush',icon='BRUSH_DATA',text="Flatten").option_value='Flatten'
        layout.operator('ds_model.sculpt_brush',icon='BRUSH_DATA',text="Grab").option_value='Grab'
        layout.operator('ds_model.sculpt_brush',icon='BRUSH_DATA',text="Inflate").option_value='Inflate'
        layout.operator('ds_model.sculpt_brush',icon='BRUSH_DATA',text="Deflate").option_value='Deflate'
        layout.operator('ds_model.sculpt_brush',icon='BRUSH_DATA',text="Smooth").option_value='Smooth'

        layout.operator('ds_model.sculpt_brush_radius_dec',icon="ZOOMOUT",text='')
        layout.operator('ds_model.sculpt_brush_radius_default',text='Radius: '+"{:.0f}".format(bpy.context.scene.tool_settings.unified_paint_settings.size)+'px')
        layout.operator('ds_model.sculpt_brush_radius_inc',icon="ZOOMIN",text='')

        layout.operator('ds_model.sculpt_brush_strength_dec',icon="ZOOMOUT",text='')
        layout.operator('ds_model.sculpt_brush_strength_default',text='Strength: '+"{:.2f}".format(context.tool_settings.sculpt.brush.strength))
        layout.operator('ds_model.sculpt_brush_strength_inc',icon="ZOOMIN",text='')

def register():

    from bpy.utils import register_class

    register_class(ui_layout)

    register_class(menu_meshes)
    register_class(menu_mesh_select)

    register_class(edit_mesh_extrude_x)
    register_class(edit_mesh_extrude_y)
    register_class(edit_mesh_extrude_z)

    register_class(edit_faces_tris)
    register_class(edit_faces_quads)

    register_class(sculpt_brush)
    register_class(sculpt_brush_radius_inc)
    register_class(sculpt_brush_radius_dec)
    register_class(sculpt_brush_radius_default)
    register_class(sculpt_brush_strength_inc)
    register_class(sculpt_brush_strength_dec)
    register_class(sculpt_brush_strength_default)

def unregister():

    from bpy.utils import unregister_class

    unregister_class(ui_layout)

    unregister_class(menu_meshes)
    unregister_class(menu_mesh_select)

    unregister_class(edit_mesh_extrude_x)
    unregister_class(edit_mesh_extrude_y)
    unregister_class(edit_mesh_extrude_z)

    unregister_class(edit_faces_tris)
    unregister_class(edit_faces_quads)

    unregister_class(sculpt_brush)
    unregister_class(sculpt_brush_radius_inc)
    unregister_class(sculpt_brush_radius_dec)
    unregister_class(sculpt_brush_radius_default)
    unregister_class(sculpt_brush_strength_inc)
    unregister_class(sculpt_brush_strength_dec)
    unregister_class(sculpt_brush_strength_default)