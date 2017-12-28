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

from os import path, makedirs

import bmesh

def bmesh_vert_active(mesh_data):
    bm = bmesh.from_edit_mesh(mesh_data)
    if bm.select_history:
        elem = bm.select_history[-1]
        if isinstance(elem, bmesh.types.BMVert):
            return True
    return False

def bmesh_edge_active(mesh_data):
    bm = bmesh.from_edit_mesh(mesh_data)
    if bm.select_history:
        elem = bm.select_history[-1]
        if isinstance(elem, bmesh.types.BMEdge):
            return True
    return False

def bmesh_face_active(mesh_data):
    bm = bmesh.from_edit_mesh(mesh_data)
    if bm.select_history:
        elem = bm.select_history[-1]
        if isinstance(elem, bmesh.types.BMFace):
            return True
    return False


def option_show(option_name):

        if hasattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+option_name):

            if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+option_name):
                return True
            else:
                return False
        
        else:

            return False

def toggle_show(option_name):

    #if hasattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+option_toggle):

    if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name + '_toggle'):
        return True
    else:
        return False

def toggle_state(option_name):

    #if hasattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+option_toggle):
    if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name):

        if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name + '_state' ):
            return True
        else:
            return False

    else:

        return False

def toggle_draw(option_name):

    #if hasattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+option_toggle):
    #    if (not ds_ui.toggle_show('info_standard') and ds_ui.option_show('info_standard')) or (ds_ui.toggle_show('info_standard') and ds_ui.toggle_state('info_standard')):

    if (not getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name + '_toggle') and getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name) ) or ( getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name + '_toggle') and getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_' + option_name + '_state') ):
        return True
    else:
        return False

class save(bpy.types.Operator):

    bl_idname = "ds_ui.save"
    bl_label = "Save"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
 
    def execute(self, context):

        bpy.ops.wm.save_mainfile()

        return {'FINISHED'}

class undo(bpy.types.Operator):
    bl_idname = "ds_ui.undo"
    bl_label = "Undo"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):
        bpy.ops.ed.undo()
        return {'FINISHED'}

class redo(bpy.types.Operator):
    bl_idname = "ds_ui.redo"
    bl_label = "Redo"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):
        bpy.ops.ed.redo()
        return {'FINISHED'}

class toggle_set(bpy.types.Operator):

    bl_idname = "ds_ui.toggle"
    bl_label = "Toggle"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    option_toggle = bpy.props.StringProperty(
        name="toggle",
        default = 'transform'
    )
    def execute(self, context):

        _param=self.option_toggle

        if hasattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+_param+'_state'):
            
            if not getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+_param+'_state'):
                setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+_param+'_state',True)
            else:
                setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_'+_param+'_state',False)

        return {'FINISHED'}    

def ui_mode():

    return getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_ui_mode')


class ui_layout_set_object(bpy.types.Operator):

    bl_idname = "ds_ui.ui_layout_set_object"
    bl_label = "SCULPT"

    def execute(self, context):
            
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                context_copy = bpy.context.copy()
                context_copy['area'] = area

                tool_shelf = False
                props_shelf = False
                for region in area.regions:
                    if region.type == 'TOOLS':
                        if region.width > 1:
                            tool_shelf = True
                    elif region.type == 'UI':
                        if region.width > 1:
                            props_shelf = True

                if tool_shelf:
                    bpy.ops.view3d.toolshelf(context_copy)

                break



        return {'FINISHED'}    

class ui_layout_set_sculpt(bpy.types.Operator):

    bl_idname = "ds_ui.ui_layout_set_sculpt"
    bl_label = "SCULPT"

    def execute(self, context):
            
        bpy.ops.object.mode_set(mode='SCULPT', toggle=False)

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                context_copy = bpy.context.copy()
                context_copy['area'] = area

                tool_shelf = False
                props_shelf = False
                for region in area.regions:
                    if region.type == 'TOOLS':
                        if region.width > 1:
                            tool_shelf = True
                    elif region.type == 'UI':
                        if region.width > 1:
                            props_shelf = True

                if not tool_shelf:
                    bpy.ops.view3d.toolshelf(context_copy)

                break

        return {'FINISHED'}    

class ui_layout_set_weightpaint(bpy.types.Operator):

    bl_idname = "ds_ui.ui_layout_set_weightpaint"
    bl_label = "WEIGHT PAINT"

    def execute(self, context):
            
        #layout.operator('object.mode_set',text="Weight Paint",icon="WPAINT_HLT").mode='WEIGHT_PAINT'


        return {'FINISHED'}    

class ui_layout_set(bpy.types.Operator):

    bl_idname = "ds_ui.ui_layout_set"
    bl_label = "Toggle"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_ui_mode',self.option_value)

        #if bpy.context.active_object:

        #   if bpy.context.active_object.mode=='EDIT':
        #        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        if self.option_value=='model':
            
            if bpy.context.scene.objects.active:
                bpy.context.scene.objects.active.show_x_ray=False
            bpy.context.window.screen = bpy.data.screens['Default']

            for ob in context.scene.objects:
                if ob.type == 'ARMATURE':
                    ob.hide=True

            _selected=False
            for ob in bpy.context.selected_objects:
                if ob.type == 'MESH':
                    _selected=True

            if not _selected:
                
                if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select'):
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

                if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_edit'):
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

                if bpy.context.active_object.mode=='EDIT':

                    if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_info_mesh_select_all'):
                        bpy.ops.mesh.select_all(action='SELECT')
                    else:        
                        bpy.ops.mesh.select_all(action='DESELECT')

        elif self.option_value=='rig':

            bpy.context.window.screen = bpy.data.screens['Default']

            for ob in context.scene.objects:
                if ob.type == 'ARMATURE':
                    ob.hide=False

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
                            break

            if bpy.context.scene.objects.active:
                bpy.context.scene.objects.active.show_x_ray=True

        elif self.option_value=='uv':

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

class info_mesh_edit_select(bpy.types.Operator):
    bl_label = "Mesh Select"
    bl_idname = "ds_ui.info_mesh_edit_select"
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

class info_mesh_select(bpy.types.Operator):
    bl_label = "Mesh Select"
    bl_idname = "ds_ui.info_mesh_select"
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


class info_meshes_edit_menu(bpy.types.Menu):
    bl_label = "Meshes"
    bl_idname = "ds_ui.info_meshes_edit_menu"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH':
                layout.operator('ds_ui.info_mesh_edit_select',text=ob.name).option_value=ob.name

class info_meshes_menu(bpy.types.Menu):
    bl_label = "Meshes"
    bl_idname = "ds_ui.info_meshes_menu"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH':
                layout.operator('ds_ui.info_mesh_select',text=ob.name).option_value=ob.name


class info_armature_select(bpy.types.Operator):
    bl_label = "Armature Select"
    bl_idname = "ds_ui.info_armature_select"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        if bpy.context.active_object and bpy.context.active_object.mode=='OBJECT':
            bpy.ops.object.select_all(action='DESELECT')
        
        ob = bpy.data.objects.get(self.option_value)
        context.scene.objects.active = ob
        ob.select = True
        
        if bpy.context.active_object.mode!='POSE':
            bpy.ops.object.mode_set(mode='POSE', toggle=False)

        return {'FINISHED'}    


class info_vertex_groups_menu(bpy.types.Menu):
    bl_label = "Vertex Groups"
    bl_idname = "ds_ui.info_vertex_groups_menu"
    def draw(self, context):
        layout = self.layout
        ob=bpy.context.active_object
        for group in ob.vertex_groups:
            layout.operator('ds_ui.info_vertex_groups_select',text=group.name).option_value=group.name

class info_armatures_menu(bpy.types.Menu):
    bl_label = "Armatures"
    bl_idname = "ds_ui.info_armatures_menu"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'ARMATURE':
                layout.operator('ds_ui.info_armature_select',text=ob.name).option_value=ob.name

class info_vertex_groups_select(bpy.types.Operator):
    bl_label = "Vertex Group Select"
    bl_idname = "ds_ui.info_vertex_groups_select"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        vgroups = bpy.context.object.vertex_groups
        vgroups.active_index = vgroups[self.option_value].index
        
        return {'FINISHED'}    

class info_uv_select(bpy.types.Operator):
    bl_label = "UV Select"
    bl_idname = "ds_ui.info_uv_select"
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

class info_uv_menu(bpy.types.Menu):
    bl_label = "Meshes"
    bl_idname = "ds_ui.info_uv_menu"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'MESH':
                layout.operator('ds_ui.info_uv_select',text=ob.name).option_value=ob.name

class view3d_viewpoints_menu(bpy.types.Menu):
    bl_label = " View"
    bl_idname = "ds_ui.view3d_viewpoints_menu"
    def draw(self, context):

        layout = self.layout

        layout.operator("view3d.viewnumpad", text="Top", icon='TRIA_UP').type = 'TOP'
        layout.operator("view3d.viewnumpad", text="Bottom", icon='TRIA_DOWN').type = 'BOTTOM'
        layout.operator("view3d.viewnumpad", text="Front", icon='ARROW_LEFTRIGHT').type = 'FRONT'
        layout.operator("view3d.viewnumpad", text="Back", icon='ARROW_LEFTRIGHT').type = 'BACK'
        layout.operator("view3d.viewnumpad", text="Right", icon='TRIA_RIGHT').type = 'RIGHT'
        layout.operator("view3d.viewnumpad", text="Left", icon='TRIA_LEFT').type = 'LEFT'

        layout.operator("view3d.viewnumpad", text="Camera", icon='CAMERA_DATA').type = 'CAMERA'


class view3d_edges_menu(bpy.types.Menu):
    bl_label = " Edge"
    bl_idname = "ds_ui.view3d_edges_menu"
    def draw(self, context):

        layout = self.layout

        _mesh=bpy.context.active_object.data
        _selected_edges = [v for v in _mesh.edges if v.select]
        if _selected_edges:

            layout.operator("mesh.loop_multi_select", text='Loop',icon="EDGESEL").ring=False
            layout.operator("mesh.loop_multi_select", text='Ring',icon="SNAP_EDGE").ring=True
            layout.operator('mesh.bevel',text="Bevel",icon="MOD_BEVEL").vertex_only=False

        layout.operator('mesh.subdivide',icon="MOD_EDGESPLIT")
        layout.operator('mesh.unsubdivide',icon="MOD_EDGESPLIT")


class view3d_select_mode_edge(bpy.types.Operator):
    bl_label = "Edge Select"
    bl_idname = "ds_ui.view3d_select_mode_edge"
    def execute(self, context):
        
        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_view3d_edges_state',True)
        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_view3d_faces_state',False)

        bpy.ops.mesh.select_mode(type="EDGE")
        
        return {'FINISHED'}    

class view3d_select_mode_face(bpy.types.Operator):
    bl_label = "Face Select"
    bl_idname = "ds_ui.view3d_select_mode_face"
    def execute(self, context):
        
        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_view3d_edges_state',False)
        setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_view3d_faces_state',True)

        bpy.ops.mesh.select_mode(type="FACE")
        
        return {'FINISHED'}   

class shade(bpy.types.Operator):
    bl_idname = "ds_ui.shade"
    bl_label = "ds_ui.shade"
    option_value = bpy.props.StringProperty(
        name="value",
        default = 'SOLID'
    )    
    def execute(self, context):

        bpy.ops.wm.context_set_enum(data_path="space_data.viewport_shade", value=self.option_value)        

        return {'FINISHED'}

class select_all(bpy.types.Operator):
    bl_idname = "ds_ui.select_all"
    bl_label = "ds_ui.select_all"
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

class select_none(bpy.types.Operator):
    bl_idname = "ds_ui.select_none"
    bl_label = "ds_ui.select_none"
    def execute(self, context):
        _scene = bpy.context.scene
        if bpy.context.active_object.mode=='OBJECT':
            for ob in _scene.objects:
                if ob.type == 'MESH':
                    ob.select = False
        elif bpy.context.active_object.mode=='EDIT':
            bpy.ops.mesh.select_all(action='DESELECT')
        return {'FINISHED'}

class primitives(bpy.types.Operator):
    bl_idname = "ds_ui.primitives"
    bl_label = "ds_ui.primitives"
    option_shape = bpy.props.StringProperty(
        name="shape",
        default = 'cube'
    )    
    def execute(self, context):

        if self.option_shape=='plane':
            bpy.ops.mesh.primitive_plane_add()
        elif self.option_shape=='circle':
            bpy.ops.mesh.primitive_circle_add()
        elif self.option_shape=='cube':
            bpy.ops.mesh.primitive_cube_add()
        elif self.option_shape=='uv_sphere':
            bpy.ops.mesh.primitive_uv_sphere_add()
        elif self.option_shape=='cylinder':
            bpy.ops.mesh.primitive_cylinder_add()
        elif self.option_shape=='cone':
            bpy.ops.mesh.primitive_cone_add()
        elif self.option_shape=='torus':
            bpy.ops.mesh.primitive_torus_add()

        #if getattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_show_primitives_close'):
        #    setattr(bpy.context.user_preferences.addons[__package__].preferences, 'option_show_primitives_toggle_state',False)

        return {'FINISHED'}

class uv_unwrap(bpy.types.Operator):
    bl_idname = "ds_ui.uv_unwrap"
    bl_label = "ds_ui.uv_unwrap"
    def execute(self, context):
        select_all.execute(self, context)
        bpy.ops.uv.unwrap()
        return {'FINISHED'}

class transform_apply(bpy.types.Operator):
    bl_idname = "ds_ui.transform_apply"
    bl_label = "ds_ui.transform_apply"
    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        return {'FINISHED'}

class manipulator_none(bpy.types.Operator):
    bl_idname = "ds_ui.manipulator_none"
    bl_label = "ds_ui.manipulator_none"
    def execute(self, context):
        bpy.context.space_data.show_manipulator = False
        return {'FINISHED'}

class manipulator_move(bpy.types.Operator):
    bl_idname = "ds_ui.manipulator_move"
    bl_label = "ds_ui.manipulator_move"
    def execute(self, context):
        bpy.context.space_data.show_manipulator = True
        bpy.context.space_data.transform_manipulators = {'TRANSLATE'}
        return {'FINISHED'}    

class manipulator_rotate(bpy.types.Operator):
    bl_idname = "ds_ui.manipulator_rotate"
    bl_label = "ds_ui.manipulator_rotate"
    def execute(self, context):
        bpy.context.space_data.show_manipulator = True
        bpy.context.space_data.transform_manipulators = {'ROTATE'}
        return {'FINISHED'}

class manipulator_scale(bpy.types.Operator):
    bl_idname = "ds_ui.manipulator_scale"
    bl_label = "ds_ui.manipulator_scale"
    def execute(self, context):
        bpy.context.space_data.show_manipulator = True
        bpy.context.space_data.transform_manipulators = {'SCALE'}
        return {'FINISHED'}    

class manipulator_decrease(bpy.types.Operator):
    bl_idname = "ds_ui.manipulator_decrease"
    bl_label = "ds_ui.manipulator_decrease"
    def execute(self, context):
        bpy.context.user_preferences.view.manipulator_size = bpy.context.user_preferences.view.manipulator_size - 10
        return {'FINISHED'}

class manipulator_increase(bpy.types.Operator):
    bl_idname = "ds_ui.manipulator_increase"
    bl_label = "ds_ui.manipulator_increase"
    def execute(self, context):
        bpy.context.user_preferences.view.manipulator_size = bpy.context.user_preferences.view.manipulator_size + 10
        return {'FINISHED'}

class edit_mesh_extrude_x(bpy.types.Operator):
    bl_idname = "ds_ui.edit_mesh_extrude_x"
    bl_label = "ds_ui.edit_mesh_extrude_x"
    def execute(self, context):  
        bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (True, False, False)})
        return {'FINISHED'}

class edit_mesh_extrude_y(bpy.types.Operator):
    bl_idname = "ds_ui.edit_mesh_extrude_y"
    bl_label = "ds_ui.edit_mesh_extrude_y"
    def execute(self, context):  
        bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, True, False)})
        return {'FINISHED'}

class edit_mesh_extrude_z(bpy.types.Operator):
    bl_idname = "ds_ui.edit_mesh_extrude_z"
    bl_label = "ds_ui.edit_mesh_extrude_z"
    def execute(self, context):  
        bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, False, True)})
        return {'FINISHED'}

class edit_armature_extrude_x(bpy.types.Operator):
    bl_idname = "ds_ui.edit_armature_extrude_x"
    bl_label = "ds_ui.edit_armature_extrude_x"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (True, False, False)})
        return {'FINISHED'}

class edit_armature_extrude_y(bpy.types.Operator):
    bl_idname = "ds_ui.edit_armature_extrude_y"
    bl_label = "ds_ui.edit_armature_extrude_y"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, True, False)})
        return {'FINISHED'}

class edit_armature_extrude_z(bpy.types.Operator):
    bl_idname = "ds_ui.edit_armature_extrude_z"
    bl_label = "ds_ui.edit_armature_extrude_z"
    def execute(self, context):  
        bpy.ops.armature.extrude_move('INVOKE_REGION_WIN',TRANSFORM_OT_translate={"constraint_orientation": 'NORMAL',"constraint_axis": (False, False, True)})
        return {'FINISHED'}

class pivot_active_element(bpy.types.Operator):
    bl_idname = "ds_ui.pivot_active_element"
    bl_label = "ds_ui.pivot_active_element"
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
        return {'FINISHED'}

class pivot_median_point(bpy.types.Operator):
    bl_idname = "ds_ui.pivot_median_point"
    bl_label = "ds_ui.pivot_median_point"
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'MEDIAN_POINT'
        return {'FINISHED'}

class pivot_individual_origins(bpy.types.Operator):
    bl_idname = "ds_ui.pivot_individual_origins"
    bl_label = "ds_ui.pivot_individual_origins"
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        return {'FINISHED'}

class pivot_cursor(bpy.types.Operator):
    bl_idname = "ds_ui.pivot_cursor"
    bl_label = "ds_ui.pivot_cursor"
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'CURSOR'
        return {'FINISHED'}

class pivot_bounding_box_center(bpy.types.Operator):
    bl_idname = "ds_ui.pivot_bounding_box_center"
    bl_label = "ds_ui.pivot_bounding_box_center"
    def execute(self, context):
        bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
        return {'FINISHED'}

class view3d_pivot_menu(bpy.types.Menu):
    bl_label = " Pivot"
    bl_idname = "ds_ui.view3d_pivot_menu"
    def draw(self, context):

        layout = self.layout
        layout.operator('ds_ui.pivot_active_element',icon='ROTACTIVE',text="Active Element")
        layout.operator('ds_ui.pivot_median_point',icon='ROTATECENTER',text="Median Point")
        layout.operator('ds_ui.pivot_individual_origins',icon='ROTATECOLLECTION',text="Individual Origins")
        layout.operator('ds_ui.pivot_cursor',icon='CURSOR',text="3d Cursor")
        layout.operator('ds_ui.pivot_bounding_box_center',icon='ROTATE',text="Bounding Box Center")

class view3d_shade_menu(bpy.types.Menu):
    bl_label = " Shade"
    bl_idname = "ds_ui.view3d_shade_menu"
    def draw(self, context):

        layout = self.layout
        layout.operator("ds_ui.shade", text="Rendered", icon='SMOOTH').option_value='RENDERED'
        layout.operator("ds_ui.shade", text="Wireframe", icon='WIRE').option_value='WIREFRAME'
        layout.operator("ds_ui.shade", text="Solid", icon='SOLID').option_value='SOLID'
        layout.operator("ds_ui.shade", text="Material", icon='MATERIAL').option_value='MATERIAL'

class view3d_weight_paint_set_brush(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush"
    option_value = bpy.props.StringProperty(
        name="option_value",
        default = ''
    )
    def execute(self, context):

        layout = self.layout
       
        context.tool_settings.weight_paint.brush = bpy.data.brushes[self.option_value]

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_weight_inc(bpy.types.Operator):
    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_weight_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.weight < 1:

            bpy.context.scene.tool_settings.unified_paint_settings.weight=bpy.context.scene.tool_settings.unified_paint_settings.weight+0.15

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_weight_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_weight_dec"

    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.weight > 0.15:

            bpy.context.scene.tool_settings.unified_paint_settings.weight=bpy.context.scene.tool_settings.unified_paint_settings.weight-0.15

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_weight_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_weight_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.weight=1.0

        return {'FINISHED'}  

class view3d_weight_paint_set_brush_radius_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_radius_inc"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size < 500:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size+10

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_radius_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_radius_dec"
  
    def execute(self, context):

        if bpy.context.scene.tool_settings.unified_paint_settings.size > 10:
            bpy.context.scene.tool_settings.unified_paint_settings.size=bpy.context.scene.tool_settings.unified_paint_settings.size-10

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_radius_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_radius_default"
  
    def execute(self, context):

        bpy.context.scene.tool_settings.unified_paint_settings.size=35

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_strength_inc(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_strength_inc"
  
    def execute(self, context):

        if context.tool_settings.weight_paint.brush.strength < 1:
            context.tool_settings.weight_paint.brush.strength=context.tool_settings.weight_paint.brush.strength+0.100

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_strength_dec(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_strength_dec"
  
    def execute(self, context):

        if context.tool_settings.weight_paint.brush.strength > 0:
            context.tool_settings.weight_paint.brush.strength=context.tool_settings.weight_paint.brush.strength-0.100

        return {'FINISHED'}    

class view3d_weight_paint_set_brush_strength_default(bpy.types.Operator):

    bl_label = "Set Brush"
    bl_idname = "ds_ui.view3d_weight_paint_set_brush_strength_default"
  
    def execute(self, context):

        context.tool_settings.weight_paint.brush.strength=0.200

        return {'FINISHED'} 

from os import path, makedirs

def ds_fbx_export(self, context):

    _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
    
    _export_path = bpy.path.abspath('//')
    
    if bpy.context.user_preferences.addons[__package__].preferences.option_export_folder:
        _export_folder=bpy.context.user_preferences.addons[__package__].preferences.option_export_folder
        if _export_folder!='':
            _export_path = path.join(_export_path,_export_folder)

    if not path.exists(_export_path):
        makedirs(_export_path)
    export_file = path.join(_export_path,export_name + '.fbx')

    if bpy.context.user_preferences.addons[__package__].preferences.option_save_before_export:
        bpy.ops.wm.save_mainfile()

    bpy.ops.export_scene.fbx(filepath=export_file, check_existing=False, axis_forward='-Z', axis_up='Y', filter_glob="*.fbx", version='BIN7400', ui_tab='MAIN', use_selection=False, global_scale=1.0, apply_unit_scale=True, bake_space_transform=False, object_types={'ARMATURE', 'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='OFF', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
    
    return export_file

def register():

    from bpy.utils import register_class

    register_class(primitives)
    register_class(select_all)
    register_class(select_none)

    register_class(toggle_set)
    register_class(ui_layout_set)
    register_class(info_mesh_select)
    register_class(info_meshes_menu)
    register_class(info_mesh_edit_select)
    register_class(info_meshes_edit_menu)
    register_class(info_armature_select)
    register_class(info_armatures_menu)
    register_class(info_vertex_groups_select)
    register_class(info_vertex_groups_menu)
    register_class(info_uv_select)
    register_class(info_uv_menu)
    register_class(save)
    register_class(undo)
    register_class(redo)
    register_class(shade)

    register_class(uv_unwrap)

    register_class(edit_mesh_extrude_x)
    register_class(edit_mesh_extrude_y)
    register_class(edit_mesh_extrude_z)

    register_class(edit_armature_extrude_x)
    register_class(edit_armature_extrude_y)
    register_class(edit_armature_extrude_z)

    register_class(manipulator_none)
    register_class(manipulator_move)
    register_class(manipulator_rotate)
    register_class(manipulator_scale)
    register_class(manipulator_decrease)
    register_class(manipulator_increase)
    
    register_class(pivot_active_element)
    register_class(pivot_median_point)
    register_class(pivot_individual_origins)
    register_class(pivot_cursor)
    register_class(pivot_bounding_box_center)

    register_class(view3d_viewpoints_menu)
    register_class(view3d_edges_menu)
    register_class(view3d_pivot_menu)
    register_class(view3d_shade_menu)

    register_class(view3d_select_mode_edge)
    register_class(view3d_select_mode_face)

    register_class(transform_apply)
    register_class(ui_layout_set_sculpt)
    register_class(ui_layout_set_object)
    register_class(ui_layout_set_weightpaint)
    
    register_class(view3d_weight_paint_set_brush)
    register_class(view3d_weight_paint_set_brush_weight_inc)
    register_class(view3d_weight_paint_set_brush_weight_dec)
    register_class(view3d_weight_paint_set_brush_weight_default)
    register_class(view3d_weight_paint_set_brush_radius_inc)
    register_class(view3d_weight_paint_set_brush_radius_dec)
    register_class(view3d_weight_paint_set_brush_radius_default)    
    register_class(view3d_weight_paint_set_brush_strength_inc)
    register_class(view3d_weight_paint_set_brush_strength_dec)
    register_class(view3d_weight_paint_set_brush_strength_default)

def unregister():

    from bpy.utils import unregister_class

    unregister_class(primitives)
    unregister_class(select_all)
    unregister_class(select_none)

    unregister_class(toggle_set)
    unregister_class(ui_layout_set)
    unregister_class(info_mesh_select)
    unregister_class(info_meshes_menu)
    unregister_class(info_mesh_edit_select)
    unregister_class(info_meshes_edit_menu)
    unregister_class(info_armature_select)
    unregister_class(info_armatures_menu)
    unregister_class(info_vertex_groups_select)
    unregister_class(info_vertex_groups_menu)
    unregister_class(info_uv_select)
    unregister_class(info_uv_menu)
    unregister_class(save)
    unregister_class(undo)
    unregister_class(redo)
    unregister_class(shade)
    
    unregister_class(uv_unwrap)    

    unregister_class(edit_mesh_extrude_x)
    unregister_class(edit_mesh_extrude_y)
    unregister_class(edit_mesh_extrude_z)

    unregister_class(edit_armature_extrude_x)
    unregister_class(edit_armature_extrude_y)
    unregister_class(edit_armature_extrude_z)

    unregister_class(manipulator_none)
    unregister_class(manipulator_move)
    unregister_class(manipulator_rotate)
    unregister_class(manipulator_scale)
    unregister_class(manipulator_decrease)
    unregister_class(manipulator_increase)

    unregister_class(pivot_active_element)
    unregister_class(pivot_median_point)
    unregister_class(pivot_individual_origins)
    unregister_class(pivot_cursor)
    unregister_class(pivot_bounding_box_center)

    unregister_class(view3d_viewpoints_menu)
    unregister_class(view3d_edges_menu)
    unregister_class(view3d_pivot_menu)
    unregister_class(view3d_shade_menu)

    unregister_class(view3d_select_mode_edge)
    unregister_class(view3d_select_mode_face)

    unregister_class(transform_apply)
    unregister_class(ui_layout_set_sculpt)
    unregister_class(ui_layout_set_object)
    unregister_class(ui_layout_set_weightpaint)
    
    unregister_class(view3d_weight_paint_set_brush)
    unregister_class(view3d_weight_paint_set_brush_weight_inc)
    unregister_class(view3d_weight_paint_set_brush_weight_dec)
    unregister_class(view3d_weight_paint_set_brush_weight_default)
    unregister_class(view3d_weight_paint_set_brush_radius_inc)
    unregister_class(view3d_weight_paint_set_brush_radius_dec)
    unregister_class(view3d_weight_paint_set_brush_radius_default)
    unregister_class(view3d_weight_paint_set_brush_strength_inc)
    unregister_class(view3d_weight_paint_set_brush_strength_dec)
    unregister_class(view3d_weight_paint_set_brush_strength_default)