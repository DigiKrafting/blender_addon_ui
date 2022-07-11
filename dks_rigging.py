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

from . import dks_ui 

# Menus

class MENU_MT_armatures(bpy.types.Menu):
    bl_label = "Armatures"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'ARMATURE':
                layout.operator('dks_rigging.menu_armature_select',text=ob.name).option_value=ob.name

class menu_armature_select(bpy.types.Operator):
    bl_label = "Armature Select"
    bl_idname = "dks_rigging.menu_armature_select"
    option_value : bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        if bpy.context.active_object and bpy.context.active_object.mode=='OBJECT':
            bpy.ops.object.select_all(action='DESELECT')

        setattr(bpy.context.preferences.addons[__package__].preferences, 'option_active_armature',self.option_value)
        
        ob = bpy.data.objects.get(self.option_value)
        #context.scene.objects.active = ob
        bpy.context.view_layer.objects.active = ob

        ob.select_set(True)
        
        if ob.mode!='POSE':
            bpy.ops.object.mode_set(mode='POSE', toggle=False)

        return {'FINISHED'}    

class MENU_MT_armature_poses(bpy.types.Menu):
    bl_label = "Poses"
    def draw(self, context):
        layout = self.layout

        _armature = bpy.context.active_object

        if bpy.context.preferences.addons[__package__].preferences.option_active_armature in bpy.data.objects:
            _armature=bpy.data.objects[bpy.context.preferences.addons[__package__].preferences.option_active_armature]
        else:
            setattr(bpy.context.preferences.addons[__package__].preferences, 'option_active_armature',_armature.name)
        
        _poses = bpy.data.objects[_armature.name].pose_library.pose_markers
        _i=-1

        for _pose in _poses:

            _i=_i+1

            f=layout.operator('dks_rigging.menu_armature_pose_select',text=_pose.name)
            f.option_armature=_armature.name
            f.option_value=_i

class menu_armature_pose_select(bpy.types.Operator):
    bl_label = "Bone Select"
    bl_idname = "dks_rigging.menu_armature_pose_select"
    option_armature : bpy.props.StringProperty(
        name="option_armature",
        default = ''
    )
    option_value : bpy.props.IntProperty(
        name="option_value",
        default = 0
    )
    def execute(self, context):

        bpy.ops.poselib.apply_pose(pose_index=self.option_value)
        
        return {'FINISHED'}    

class MENU_MT_armature_bones(bpy.types.Menu):
    bl_label = "Deform Bones"
    def draw(self, context):
        layout = self.layout

        _armature = bpy.context.active_object

        if bpy.context.preferences.addons[__package__].preferences.option_active_armature in bpy.data.objects:
            _armature=bpy.data.objects[bpy.context.preferences.addons[__package__].preferences.option_active_armature]
        else:
            setattr(bpy.context.preferences.addons[__package__].preferences, 'option_active_armature',_armature.name)
        
        if bpy.context.active_object.mode=='POSE':

            _bones = _armature.pose.bones

            for _bone in _bones:

                if _bone.use_deform == True:

                    f=layout.operator('dks_rigging.menu_armature_bone_select',text=_bone.name)
                    f.option_armature=ob.name
                    f.option_value=_bone.name

        else:

            _bones = _armature.data.edit_bones

            for _bone in _bones:
                
                #if not "DEF-" in _bone.name and not "MCH-" in _bone.name and not "VIS_" in _bone.name and not "ORG-" in _bone.name and not "." in _bone.name and not "ik_" in _bone.name and not "_twist_" in _bone.name:
                if _bone.use_deform == True:

                    f=layout.operator('dks_rigging.menu_armature_bone_select',text=_bone.name)
                    f.option_armature=ob.name
                    f.option_value=_bone.name

class MENU_MT_armature_bones_ik(bpy.types.Menu):
    bl_label = "Bones"
    def draw(self, context):
        layout = self.layout

        _armature = bpy.context.active_object

        if bpy.context.preferences.addons[__package__].preferences.option_active_armature in bpy.data.objects:
            _armature=bpy.data.objects[bpy.context.preferences.addons[__package__].preferences.option_active_armature]
        else:
            setattr(bpy.context.preferences.addons[__package__].preferences, 'option_active_armature',_armature.name)

        _bones = _armature.pose.bones

        for _bone in _bones:
            
            if "ik_" in _bone.name:

                f=layout.operator('dks_rigging.menu_armature_bone_select',text=_bone.name)
                f.option_armature=_armature.name
                f.option_value=_bone.name

class menu_armature_bone_select(bpy.types.Operator):
    bl_label = "Bone Select"
    bl_idname = "dks_rigging.menu_armature_bone_select"
    option_armature : bpy.props.StringProperty(
        name="option_armature",
        default = ''
    )
    option_value : bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):
        
        mode_string = context.mode
        
        #self.report({'ERROR'}, 'mode_string: ' + mode_string)

        _armature = bpy.data.objects.get(self.option_armature)

        if _armature is None:
            self.report({'ERROR'}, 'Unable to reference armature.')
            return {'FINISHED'}

        bpy.context.view_layer.objects.active = _armature
        _armature.select_set(True)
        
        if mode_string == 'EDIT_ARMATURE':

            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.armature.select_all(action='DESELECT')
            
            _bone = _armature.data.edit_bones.get(self.option_value)
            _armature.data.edit_bones.active = _bone
            _bone.select = True
            bpy.context.view_layer.objects.active = _bone

        elif mode_string == 'POSE':

            bpy.ops.object.mode_set(mode = 'POSE')
            bpy.ops.pose.select_all(action='DESELECT')

            _bone = _armature.data.bones.get(self.option_value)
            _armature.data.bones.active = _bone
            _bone.select = True
            bpy.context.view_layer.objects.active = _bone

        return {'FINISHED'}    

class MENU_MT_vertex_groups(bpy.types.Menu):
    bl_label = "Vertex Groups"
    def draw(self, context):
        layout = self.layout
        ob=bpy.context.active_object
        for group in ob.vertex_groups:
            layout.operator('dks_rigging.menu_vertex_group_select',text=group.name).option_value=group.name

class menu_vertex_group_select(bpy.types.Operator):
    bl_label = "Vertex Group Select"
    bl_idname = "dks_rigging.menu_vertex_group_select"
    option_value : bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        vgroups = bpy.context.object.vertex_groups
        vgroups.active_index = vgroups[self.option_value].index
        
        return {'FINISHED'}    

class MENU_MT_meshes(bpy.types.Menu):
    bl_label = "Meshes"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH' and ob.hide==False:
                layout.operator('dks_rigging.menu_mesh_select',text=ob.name).option_value=ob.name

class menu_mesh_select(bpy.types.Operator):
    bl_label = "Mesh Select"
    bl_idname = "dks_rigging.menu_mesh_select"
    option_value : bpy.props.StringProperty(
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
    bl_idname = "dks_rigging.edit_armature_extrude_x"
    bl_label = "dks_rigging.edit_armature_extrude_x"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (True, False, False)})
        return {'FINISHED'}

class edit_armature_extrude_y(bpy.types.Operator):
    bl_idname = "dks_rigging.edit_armature_extrude_y"
    bl_label = "dks_rigging.edit_armature_extrude_y"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, True, False)})
        return {'FINISHED'}

class edit_armature_extrude_z(bpy.types.Operator):
    bl_idname = "dks_rigging.edit_armature_extrude_z"
    bl_label = "dks_rigging.edit_armature_extrude_z"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, False, True)})
        return {'FINISHED'}

class insert_keyframe_location_rotation(bpy.types.Operator):
    bl_label = "Insert Keyframe - Location Rotation"
    bl_idname = "dks_rigging.insert_keyframe_location_rotation"
    def execute(self, context):
        bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
        return {'FINISHED'} 

class insert_keyframe_location(bpy.types.Operator):
    bl_label = "Insert Keyframe - Location"
    bl_idname = "dks_rigging.insert_keyframe_location"
    def execute(self, context):
        bpy.ops.anim.keyframe_insert_menu(type='Location')
        return {'FINISHED'}

class insert_keyframe_rotation(bpy.types.Operator):
    bl_label = "Insert Keyframe - Rotation"
    bl_idname = "dks_rigging.insert_keyframe_rotation"
    def execute(self, context):
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        return {'FINISHED'} 

# Weight Paint

class weight_paint_brush(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush"
    option_value : bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        layout = self.layout
       
        context.tool_settings.weight_paint.brush = bpy.data.brushes[self.option_value]

        return {'FINISHED'}    

class weight_paint_brush_weight_inc(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_weight_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.weight < 1:

            bpy.context.scene.tool_settings.unified_paint_settings.weight=bpy.context.scene.tool_settings.unified_paint_settings.weight+0.15

        return {'FINISHED'}    

class weight_paint_brush_weight_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_weight_dec"

    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.weight > 0.15:

            bpy.context.scene.tool_settings.unified_paint_settings.weight=bpy.context.scene.tool_settings.unified_paint_settings.weight-0.15

        return {'FINISHED'}    

class weight_paint_brush_weight_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_weight_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.weight=1.0

        return {'FINISHED'}  

class weight_paint_brush_radius_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_radius_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size < 500:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size+10

        return {'FINISHED'}    

class weight_paint_brush_radius_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_radius_dec"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size > 10:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size-10

        return {'FINISHED'}    

class weight_paint_brush_radius_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_radius_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.size=35

        return {'FINISHED'}    

class weight_paint_brush_strength_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_strength_inc"
  
    def execute(self, context):

        if context.tool_settings.weight_paint.brush.strength < 1:
            context.tool_settings.weight_paint.brush.strength=context.tool_settings.weight_paint.brush.strength+0.100

        return {'FINISHED'}    

class weight_paint_brush_strength_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_strength_dec"
  
    def execute(self, context):

        if context.tool_settings.weight_paint.brush.strength > 0:
            context.tool_settings.weight_paint.brush.strength=context.tool_settings.weight_paint.brush.strength-0.100

        return {'FINISHED'}    

class weight_paint_brush_strength_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "dks_rigging.weight_paint_brush_strength_default"
  
    def execute(self, context):

        context.tool_settings.weight_paint.brush.strength=0.200

        return {'FINISHED'} 

# UI

class ui_layout(bpy.types.Operator):

    bl_idname = "dks_rigging.ui_layout"
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

    layout.menu('MENU_MT_armatures',icon="TRIA_DOWN")
    layout.menu('MENU_MT_armature_bones',icon="TRIA_DOWN")
    layout.menu('MENU_MT_meshes',icon="TRIA_DOWN")

    if _obj:

        if _obj.show_x_ray==True:
            _icon='OUTLINER_DATA_ARMATURE'
        else:
            _icon='ARMATURE_DATA'

        layout.operator("wm.context_toggle", text="X-Ray", icon=_icon).data_path = "scene.objects.active.show_x_ray"

    if _obj_mode=='PAINT_WEIGHT':

        layout.menu('MENU_MT_vertex_groups',icon="TRIA_DOWN")
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
            layout.operator('dks_rigging.edit_armature_extrude_x', text="X Axis")
            layout.operator('dks_rigging.edit_armature_extrude_y', text="Y Axis")
            layout.operator('dks_rigging.edit_armature_extrude_z', text="Z Axis")

    elif _obj_mode=='POSE':

        ds_ui.tools_transform(context, layout)

        layout.operator("pose.copy", text="", icon='COPYDOWN')
        layout.operator("pose.paste", text="", icon='PASTEDOWN').flipped = False
        layout.operator("pose.paste", text="", icon='PASTEFLIPDOWN').flipped = True

        layout.operator("poselib.browse_interactive").pose_index=0
        layout.operator("poselib.pose_add")

    elif _obj_mode=='PAINT_WEIGHT':

        layout.operator('dks_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Add").option_value='Add'
        layout.operator('dks_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Blur").option_value='Blur'
        layout.operator('dks_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Darken").option_value='Darken'
        layout.operator('dks_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Lighten").option_value='Lighten'
        layout.operator('dks_rigging.weight_paint_brush',icon='BRUSH_DATA',text="Subtract").option_value='Subtract'
        
        layout.operator('dks_rigging.weight_paint_brush_weight_dec',icon="ZOOMOUT",text='')
        layout.operator('dks_rigging.weight_paint_brush_weight_default',text='Weight: '+"{:.2f}".format(bpy.context.scene.tool_settings.unified_paint_settings.weight))
        layout.operator('dks_rigging.weight_paint_brush_weight_inc',icon="ZOOMIN",text='')
    
        layout.operator('dks_rigging.weight_paint_brush_radius_dec',icon="ZOOMOUT",text='')
        layout.operator('dks_rigging.weight_paint_brush_radius_default',text='Radius: '+"{:.0f}".format(bpy.context.scene.tool_settings.unified_paint_settings.size)+'px')
        layout.operator('dks_rigging.weight_paint_brush_radius_inc',icon="ZOOMIN",text='')

        layout.operator('dks_rigging.weight_paint_brush_strength_dec',icon="ZOOMOUT",text='')
        layout.operator('dks_rigging.weight_paint_brush_strength_default',text='Strength: '+"{:.2f}".format(context.tool_settings.weight_paint.brush.strength))
        layout.operator('dks_rigging.weight_paint_brush_strength_inc',icon="ZOOMIN",text='')

class weight_paint_auto_weight(bpy.types.Operator):

    bl_idname = "dks_rigging.weight_paint_auto_weight"
    bl_label = "Auto Weight"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "Select all Bones and Auto Weight"
    def execute(self, context):

        ob=bpy.context.active_object
        
        _armature_bones=bpy.data.objects[ob.parent.name].data.bones

        for bone in _armature_bones:

            _select=True

            if bone.name[0:3]=="ik_" or bone.name=="root":
                _select=False

            _armature_bones[bone.name].select = _select

#        for group in ob.vertex_groups:
#            _armature_bones[group.name].select = True

        bpy.ops.paint.weight_from_bones(type='AUTOMATIC')

        return {'FINISHED'}    

classes = (
    ui_layout,
    MENU_MT_armatures,
    menu_armature_select,
    MENU_MT_armature_poses,
    menu_armature_pose_select,
    MENU_MT_armature_bones,
    MENU_MT_armature_bones_ik,
    menu_armature_bone_select,
    MENU_MT_vertex_groups,
    menu_vertex_group_select,
    MENU_MT_meshes,
    menu_mesh_select,
    edit_armature_extrude_x,
    edit_armature_extrude_y,
    edit_armature_extrude_z,
    insert_keyframe_location_rotation,
    insert_keyframe_location,
    insert_keyframe_rotation,
    weight_paint_brush,
    weight_paint_brush_weight_inc,
    weight_paint_brush_weight_dec,
    weight_paint_brush_weight_default,
    weight_paint_brush_radius_inc,
    weight_paint_brush_radius_dec,
    weight_paint_brush_radius_default,
    weight_paint_brush_strength_inc,
    weight_paint_brush_strength_dec,
    weight_paint_brush_strength_default,
    weight_paint_auto_weight,
)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)