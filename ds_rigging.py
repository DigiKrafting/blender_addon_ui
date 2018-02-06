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

class menu_armatures(bpy.types.Menu):
    bl_label = "Armatures"
    bl_idname = "ds_rigging.menu_armatures"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'ARMATURE':
                layout.operator('ds_rigging.menu_armature_select',text=ob.name).option_value=ob.name

class menu_armature_select(bpy.types.Operator):
    bl_label = "Armature Select"
    bl_idname = "ds_rigging.menu_armature_select"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        if bpy.context.active_object and bpy.context.active_object.mode=='OBJECT':
            bpy.ops.object.select_all(action='DESELECT')

        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_active_armature',self.option_value)
        
        ob = bpy.data.objects.get(self.option_value)
        context.scene.objects.active = ob
        ob.select = True
        
        if bpy.context.active_object.mode!='POSE':
            bpy.ops.object.mode_set(mode='POSE', toggle=False)

        return {'FINISHED'}    

class menu_armature_bones(bpy.types.Menu):
    bl_label = "Bones"
    bl_idname = "ds_rigging.menu_armature_bones"
    def draw(self, context):
        layout = self.layout

        ob=bpy.data.objects[bpy.context.user_preferences.addons[__package__].preferences.option_active_armature]
    
        for bone in ob.data.bones:
            f=layout.operator('ds_rigging.menu_armature_bone_select',text=bone.name)
            f.option_armature=ob.name
            f.option_value=bone.name

class menu_armature_bone_select(bpy.types.Operator):
    bl_label = "Bone Select"
    bl_idname = "ds_rigging.menu_armature_bone_select"
    option_armature = bpy.props.StringProperty(
        name="option_armature",
        default = ''
    )
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):
        
        _armature = bpy.data.objects[self.option_armature]
        _bone = _armature.data.bones[self.option_value]

        _armature.data.bones.active = _bone
        _bone.select = True

        return {'FINISHED'}    

class menu_vertex_groups(bpy.types.Menu):
    bl_label = "Vertex Groups"
    bl_idname = "ds_rigging.menu_vertex_groups"
    def draw(self, context):
        layout = self.layout
        ob=bpy.context.active_object
        for group in ob.vertex_groups:
            layout.operator('ds_rigging.menu_vertex_group_select',text=group.name).option_value=group.name

class menu_vertex_group_select(bpy.types.Operator):
    bl_label = "Vertex Group Select"
    bl_idname = "ds_rigging.menu_vertex_group_select"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        vgroups = bpy.context.object.vertex_groups
        vgroups.active_index = vgroups[self.option_value].index
        
        return {'FINISHED'}    

class menu_meshes(bpy.types.Menu):
    bl_label = "Meshes"
    bl_idname = "ds_rigging.menu_meshes"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH' and ob.hide==False:
                layout.operator('ds_rigging.menu_mesh_select',text=ob.name).option_value=ob.name

class menu_mesh_select(bpy.types.Operator):
    bl_label = "Mesh Select"
    bl_idname = "ds_rigging.menu_mesh_select"
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

        bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)
        
        return {'FINISHED'}    

# Functions

class edit_armature_extrude_x(bpy.types.Operator):
    bl_idname = "ds_rigging.edit_armature_extrude_x"
    bl_label = "ds_rigging.edit_armature_extrude_x"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (True, False, False)})
        return {'FINISHED'}

class edit_armature_extrude_y(bpy.types.Operator):
    bl_idname = "ds_rigging.edit_armature_extrude_y"
    bl_label = "ds_rigging.edit_armature_extrude_y"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, True, False)})
        return {'FINISHED'}

class edit_armature_extrude_z(bpy.types.Operator):
    bl_idname = "ds_rigging.edit_armature_extrude_z"
    bl_label = "ds_rigging.edit_armature_extrude_z"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, False, True)})
        return {'FINISHED'}

# Weight Paint

class weight_paint_brush(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        layout = self.layout
       
        context.tool_settings.weight_paint.brush = bpy.data.brushes[self.option_value]

        return {'FINISHED'}    

class weight_paint_brush_weight_inc(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_weight_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.weight < 1:

            bpy.context.scene.tool_settings.unified_paint_settings.weight=bpy.context.scene.tool_settings.unified_paint_settings.weight+0.15

        return {'FINISHED'}    

class weight_paint_brush_weight_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_weight_dec"

    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.weight > 0.15:

            bpy.context.scene.tool_settings.unified_paint_settings.weight=bpy.context.scene.tool_settings.unified_paint_settings.weight-0.15

        return {'FINISHED'}    

class weight_paint_brush_weight_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_weight_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.weight=1.0

        return {'FINISHED'}  

class weight_paint_brush_radius_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_radius_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size < 500:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size+10

        return {'FINISHED'}    

class weight_paint_brush_radius_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_radius_dec"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size > 10:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size-10

        return {'FINISHED'}    

class weight_paint_brush_radius_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_radius_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.size=35

        return {'FINISHED'}    

class weight_paint_brush_strength_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_strength_inc"
  
    def execute(self, context):

        if context.tool_settings.weight_paint.brush.strength < 1:
            context.tool_settings.weight_paint.brush.strength=context.tool_settings.weight_paint.brush.strength+0.100

        return {'FINISHED'}    

class weight_paint_brush_strength_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_strength_dec"
  
    def execute(self, context):

        if context.tool_settings.weight_paint.brush.strength > 0:
            context.tool_settings.weight_paint.brush.strength=context.tool_settings.weight_paint.brush.strength-0.100

        return {'FINISHED'}    

class weight_paint_brush_strength_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_rigging.weight_paint_brush_strength_default"
  
    def execute(self, context):

        context.tool_settings.weight_paint.brush.strength=0.200

        return {'FINISHED'} 

# UI

class ui_layout(bpy.types.Operator):

    bl_idname = "ds_rigging.ui_layout"
    bl_label = "Toggle"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def execute(self, context):

        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_ui_mode','rigging')

        bpy.context.window.screen = bpy.data.screens['Default']

        _obj=bpy.context.scene.objects.active
        
        if _obj:
            
            _obj_parent = _obj.parent

            if _obj_parent and _obj_parent.type == 'ARMATURE':

                _obj_parent.hide=False
                
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

                setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_active_armature',_obj_parent.name)
                
                context.scene.objects.active = _obj_parent

                _obj_parent.show_x_ray=True

        x=0
        if x==1:
            for ob in context.scene.objects:
                if ob.type == 'ARMATURE':
                    ob.hide=False

            if bpy.context.scene.objects.active:

                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            _selected=False

            for ob in bpy.context.selected_objects:
                if ob.type == 'ARMATURE':
                    _selected=True

            if not _selected:

                if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_armature_select'):
                    for ob in context.scene.objects:
                        if ob.type == 'ARMATURE':
                            context.scene.objects.active = ob
                            ob.select = True
                            setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_active_armature',ob.name)
                            break

                if bpy.context.scene.objects.active:

                    bpy.context.scene.objects.active.show_x_ray=True

        return {'FINISHED'}

def menu(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    layout.menu('ds_rigging.menu_armatures',icon="TRIA_DOWN")
    layout.menu('ds_rigging.menu_armature_bones',icon="TRIA_DOWN")
    layout.menu('ds_rigging.menu_meshes',icon="TRIA_DOWN")

    if _obj:

        if _obj.show_x_ray==True:
            _icon='OUTLINER_DATA_ARMATURE'
        else:
            _icon='ARMATURE_DATA'

        layout.operator("wm.context_toggle", text="X-Ray", icon=_icon).data_path = "scene.objects.active.show_x_ray"

    if _obj_mode=='PAINT_WEIGHT':

        layout.menu('ds_rigging.menu_vertex_groups',icon="TRIA_DOWN")
        layout.menu("VIEW3D_MT_paint_weight",icon="TRIA_DOWN")

    elif _obj_mode=='EDIT_ARMATURE':

        layout.menu("INFO_MT_edit_armature_add",icon='BONE_DATA')
        layout.menu("VIEW3D_MT_edit_armature",icon='COLLAPSEMENU')

    elif _obj_mode=='POSE':

        layout.menu("VIEW3D_MT_pose",icon='COLLAPSEMENU')

    if _obj and _obj.type=='MESH':
        
        if _obj_mode=='OBJECT':

            layout.operator('object.mode_set',text="Weight Paint",icon="WPAINT_HLT").mode='WEIGHT_PAINT'

        elif _obj_mode=='PAINT_WEIGHT':

            if _obj:

                layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'

    elif _obj_mode=='POSE':

        layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'
        layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'

    elif _obj_mode=='EDIT_ARMATURE':

        layout.operator('object.mode_set',text="Pose",icon="POSE_HLT").mode='POSE'
        layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'

    elif _obj_mode=='OBJECT':

        layout.operator('object.mode_set',text="Pose",icon="POSE_HLT").mode='POSE'
        layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'

def tools(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    if _obj_mode=='EDIT_ARMATURE':

        layout.operator("armature.bone_primitive_add", text='Add')
        layout.operator("armature.duplicate", text='Duplicate')
        layout.operator("armature.delete", text='Delete')

        layout.operator("armature.split", text='Split')
        layout.operator("armature.parent_set", text='Parent Connected').type='CONNECTED'
        layout.operator("armature.parent_set", text='Parent Offset').type='OFFSET'

        layout.operator("armature.parent_clear", text='Parent Clear').type='CLEAR'
        layout.operator("armature.parent_clear", text='Parent Disconnect').type='DISCONNECT'

        layout.operator("armature.switch_direction", text='Switch Direction')

        if ds_ui.toggle_show('view3d_extrude'):
            layout.operator('ds_ui.toggle',icon='MOD_SHRINKWRAP',text="").option_toggle='view3d_extrude'
        
        if ds_ui.toggle_draw('view3d_extrude'):

            layout.operator("armature.extrude_move", text='extrude_move')
            layout.operator('ds_rigging.edit_armature_extrude_x', text="X Axis")
            layout.operator('ds_rigging.edit_armature_extrude_y', text="Y Axis")
            layout.operator('ds_rigging.edit_armature_extrude_z', text="Z Axis")

    elif _obj_mode=='POSE':

        ds_ui.tools_transform(context, layout)

        layout.operator("pose.copy", text="", icon='COPYDOWN')
        layout.operator("pose.paste", text="", icon='PASTEDOWN').flipped = False
        layout.operator("pose.paste", text="", icon='PASTEFLIPDOWN').flipped = True

        layout.operator("poselib.browse_interactive").pose_index=0
        layout.operator("poselib.pose_add")

    elif _obj_mode=='PAINT_WEIGHT':

        layout.operator('ds_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Add").option_value='Add'
        layout.operator('ds_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Blur").option_value='Blur'
        layout.operator('ds_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Darken").option_value='Darken'
        layout.operator('ds_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Lighten").option_value='Lighten'
        layout.operator('ds_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Subtract").option_value='Subtract'
        
        layout.operator('ds_rigging.weight_paint_brush_weight_dec',icon="ZOOMOUT",text='')
        layout.operator('ds_rigging.weight_paint_brush_weight_default',text='Weight: '+"{:.2f}".format(bpy.context.scene.tool_settings.unified_paint_settings.weight))
        layout.operator('ds_rigging.weight_paint_brush_weight_inc',icon="ZOOMIN",text='')
    
        layout.operator('ds_rigging.weight_paint_brush_radius_dec',icon="ZOOMOUT",text='')
        layout.operator('ds_rigging.weight_paint_brush_radius_default',text='Radius: '+"{:.0f}".format(bpy.context.scene.tool_settings.unified_paint_settings.size)+'px')
        layout.operator('ds_rigging.weight_paint_brush_radius_inc',icon="ZOOMIN",text='')

        layout.operator('ds_rigging.weight_paint_brush_strength_dec',icon="ZOOMOUT",text='')
        layout.operator('ds_rigging.weight_paint_brush_strength_default',text='Strength: '+"{:.2f}".format(context.tool_settings.weight_paint.brush.strength))
        layout.operator('ds_rigging.weight_paint_brush_strength_inc',icon="ZOOMIN",text='')

def register():

    from bpy.utils import register_class

    register_class(ui_layout)

    register_class(menu_armatures)
    register_class(menu_armature_select)
    register_class(menu_armature_bones)
    register_class(menu_armature_bone_select)
    register_class(menu_vertex_groups)    
    register_class(menu_vertex_group_select)
    register_class(menu_meshes)
    register_class(menu_mesh_select)

    register_class(edit_armature_extrude_x)
    register_class(edit_armature_extrude_y)
    register_class(edit_armature_extrude_z)

    register_class(weight_paint_brush)
    register_class(weight_paint_brush_weight_inc)
    register_class(weight_paint_brush_weight_dec)
    register_class(weight_paint_brush_weight_default)
    register_class(weight_paint_brush_radius_inc)
    register_class(weight_paint_brush_radius_dec)
    register_class(weight_paint_brush_radius_default)    
    register_class(weight_paint_brush_strength_inc)
    register_class(weight_paint_brush_strength_dec)
    register_class(weight_paint_brush_strength_default)

def unregister():

    from bpy.utils import unregister_class

    unregister_class(ui_layout)

    unregister_class(menu_armatures)
    unregister_class(menu_armature_select)
    unregister_class(menu_armature_bones)
    unregister_class(menu_armature_bone_select)
    unregister_class(menu_vertex_groups)
    unregister_class(menu_vertex_group_select)
    unregister_class(menu_meshes)
    unregister_class(menu_mesh_select)

    unregister_class(edit_armature_extrude_x)
    unregister_class(edit_armature_extrude_y)
    unregister_class(edit_armature_extrude_z)

    unregister_class(weight_paint_brush)
    unregister_class(weight_paint_brush_weight_inc)
    unregister_class(weight_paint_brush_weight_dec)
    unregister_class(weight_paint_brush_weight_default)
    unregister_class(weight_paint_brush_radius_inc)
    unregister_class(weight_paint_brush_radius_dec)
    unregister_class(weight_paint_brush_radius_default)
    unregister_class(weight_paint_brush_strength_inc)
    unregister_class(weight_paint_brush_strength_dec)
    unregister_class(weight_paint_brush_strength_default)