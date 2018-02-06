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

# Menus

class menu_pivot(bpy.types.Menu):
    bl_label = " Pivot"
    bl_idname = "ds_ui.menu_pivot"
    def draw(self, context):

        layout = self.layout
        layout.operator('ds_ui.pivot_active_element',icon='ROTACTIVE',text="Active Element")
        layout.operator('ds_ui.pivot_median_point',icon='ROTATECENTER',text="Median Point")
        layout.operator('ds_ui.pivot_individual_origins',icon='ROTATECOLLECTION',text="Individual Origins")
        layout.operator('ds_ui.pivot_cursor',icon='CURSOR',text="3d Cursor")
        layout.operator('ds_ui.pivot_bounding_box_center',icon='ROTATE',text="Bounding Box Center")

class menu_shade(bpy.types.Menu):
    bl_label = " Shade"
    bl_idname = "ds_ui.menu_shade"
    def draw(self, context):

        layout = self.layout
        layout.operator("ds_ui.shade", text="Rendered", icon='SMOOTH').option_value='RENDERED'
        layout.operator("ds_ui.shade", text="Wireframe", icon='WIRE').option_value='WIREFRAME'
        layout.operator("ds_ui.shade", text="Solid", icon='SOLID').option_value='SOLID'
        layout.operator("ds_ui.shade", text="Material", icon='MATERIAL').option_value='MATERIAL'

class menu_viewpoints(bpy.types.Menu):
    bl_label = " View"
    bl_idname = "ds_ui.menu_viewpoints"
    def draw(self, context):

        layout = self.layout

        layout.operator("view3d.viewnumpad", text="Top", icon='TRIA_UP').type = 'TOP'
        layout.operator("view3d.viewnumpad", text="Bottom", icon='TRIA_DOWN').type = 'BOTTOM'
        layout.operator("view3d.viewnumpad", text="Front", icon='ARROW_LEFTRIGHT').type = 'FRONT'
        layout.operator("view3d.viewnumpad", text="Back", icon='ARROW_LEFTRIGHT').type = 'BACK'
        layout.operator("view3d.viewnumpad", text="Right", icon='TRIA_RIGHT').type = 'RIGHT'
        layout.operator("view3d.viewnumpad", text="Left", icon='TRIA_LEFT').type = 'LEFT'

        layout.operator("view3d.viewnumpad", text="Camera", icon='CAMERA_DATA').type = 'CAMERA'

class menu_edges(bpy.types.Menu):
    bl_label = " Edge"
    bl_idname = "ds_ui.menu_edges"
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

# Globals

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

# UI

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

# Functions

class show_node_editor(bpy.types.Operator):
    bl_idname = "ds_ui.show_node_editor"
    bl_label = "Node Editor"
    def execute(self, context):
        bpy.context.area.type = 'NODE_EDITOR'
        return {'FINISHED'}

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

def blender_addon_pipeline(layout):

    if 'blender_addon_zbrushcore' in bpy.context.user_preferences.addons:

        layout.operator('ds_zbc.export',text="ZBC",icon="EXPORT")
        layout.operator('ds_zbc.import',text="ZBC",icon="IMPORT")

    if 'blender_addon_unfold3d' in bpy.context.user_preferences.addons:

        layout.operator('ds_u3d.export',text="U3D",icon="EXPORT")
        layout.operator('ds_u3d.import',text="U3D",icon="IMPORT")

    if 'blender_addon_substance_painter' in bpy.context.user_preferences.addons:

        if bpy.context.user_preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle:

            layout.operator('ds_sp.toggle',icon='TRIA_RIGHT')

        if (not bpy.context.user_preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle) or (bpy.context.user_preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle and bpy.context.user_preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle_state):

            layout.operator('ds_sp.export_scene',text="SP:Scene",icon="EXPORT")
            layout.operator('ds_sp.pbr_nodes', text='SP:Scene',icon="IMPORT").import_setting = 'scene'
            layout.operator('ds_sp.export_sel',text="SP:Sel",icon="EXPORT")
            layout.operator('ds_sp.pbr_nodes', text='SP:Sel',icon="IMPORT").import_setting = 'selected'

    if 'blender_addon_iclone' in bpy.context.user_preferences.addons:

        if bpy.context.user_preferences.addons['blender_addon_iclone'].preferences.option_show_iclone_toggle:

            layout.operator('ds_ic.toggle',icon='TRIA_RIGHT')
        
        if (not bpy.context.user_preferences.addons['blender_addon_iclone'].preferences.option_show_iclone_toggle) or (bpy.context.user_preferences.addons['blender_addon_iclone'].preferences.option_show_iclone_toggle and bpy.context.user_preferences.addons['blender_addon_iclone'].preferences.option_show_iclone_toggle_state):

            layout.operator('ds_ic.export_cc',text="CC",icon="EXPORT")
            layout.operator('ds_ic.export_3dx',text="3DX",icon="EXPORT")

            layout.operator('ds_ic.import_base',text="Base",icon="IMPORT")
            layout.operator('ds_ic.import_female',text="Female",icon="IMPORT")
            layout.operator('ds_ic.import_male',text="Male",icon="IMPORT")

            layout.operator('ds_ic.export_ic',text="IC",icon="LINK_BLEND")

def tools(context, layout):

    _obj_mode = context.mode
    _obj = context.active_object

    if _obj:

        layout.menu("VIEW3D_MT_object",icon='COLLAPSEMENU',text="")

    layout.menu('ds_ui.menu_viewpoints',icon="CURSOR",text='')
    layout.operator('screen.region_quadview',icon='MOD_LATTICE',text="")
    layout.operator('view3d.view_selected',icon='ZOOM_SELECTED',text="")
    layout.operator('view3d.localview',icon='RESTRICT_VIEW_OFF',text="")
    layout.operator('view3d.view_persportho',icon='ORTHO',text="")
    layout.operator('view3d.zoom_border', text="",icon='BORDERMOVE')

    _icon="FORCE_FORCE"
    _shade=bpy.context.space_data.viewport_shade
    if _shade=='RENDERED':
        _icon='SMOOTH'
    elif _shade=='WIREFRAME':
        _icon='WIRE'
    elif _shade=='SOLID':
        _icon='SOLID'
    elif _shade=='MATERIAL':
        _icon='MATERIAL'
    layout.menu('ds_ui.menu_shade',icon=_icon,text='')

    _icon="FORCE_FORCE"
    _pivot=bpy.context.space_data.pivot_point
    if _pivot == 'ACTIVE_ELEMENT':
        _icon='ROTACTIVE'
    elif _pivot == 'MEDIAN_POINT':
        _icon='ROTATECENTER'
    elif _pivot == 'INDIVIDUAL_ORIGINS':
        _icon='ROTATECOLLECTION'
    elif _pivot == 'CURSOR':
        _icon='CURSOR'
    elif _pivot == 'BOUNDING_BOX_CENTER':
        _icon='ROTATE'
    layout.menu('ds_ui.menu_pivot',icon=_icon,text='')

#        layout.operator("transform.translate",icon='MAN_TRANS', text="")
    view = context.space_data

    # if (( (_obj_mode == 'PARTICLE_EDIT' or (_obj_mode == 'EDIT' and _obj.type == 'MESH'))) or (_obj_mode == 'WEIGHT_PAINT')):
    
    layout.prop(view, "use_occlude_geometry", text="")

    layout.operator('ds_ui.select_all', text="",icon='RESTRICT_COLOR_ON')
    layout.operator('ds_ui.select_none', text="",icon='RESTRICT_COLOR_OFF')

    layout.operator("view3d.select_border", text='',icon='BORDER_RECT')
    layout.operator("view3d.select_circle", text='',icon='BORDER_LASSO')

    layout.operator("object.select_less", text='',icon='DISCLOSURE_TRI_DOWN')
    layout.operator("object.select_more", text='',icon='DISCLOSURE_TRI_RIGHT')

def tools_transform(context, layout):

    layout.operator("transform.translate",icon='MAN_TRANS', text="")
    layout.operator("transform.rotate", icon='ROTATE', text="")
    layout.operator("transform.resize", icon='MAN_SCALE', text="")
    
    layout.operator("ds_ui.manipulator_decrease", icon='ZOOMOUT', text='')
    layout.operator("ds_ui.manipulator_none", icon='MANIPUL', text='')
    layout.operator("ds_ui.manipulator_move", icon='MAN_TRANS', text='')
    layout.operator("ds_ui.manipulator_rotate", icon='MAN_ROT', text='')
    layout.operator("ds_ui.manipulator_scale", icon='MAN_SCALE', text='')
    layout.operator("ds_ui.manipulator_increase", icon='ZOOMIN', text='')

def register():

    from bpy.utils import register_class

    register_class(select_all)
    register_class(select_none)

    register_class(toggle_set)

    register_class(save)
    register_class(undo)
    register_class(redo)
    register_class(shade)

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

    register_class(menu_viewpoints)
    register_class(menu_edges)
    register_class(menu_pivot)
    register_class(menu_shade)

    register_class(ui_layout_set_sculpt)
    register_class(ui_layout_set_object)
    


    register_class(show_node_editor)

def unregister():

    from bpy.utils import unregister_class

    unregister_class(select_all)
    unregister_class(select_none)

    unregister_class(toggle_set)

    unregister_class(save)
    unregister_class(undo)
    unregister_class(redo)
    unregister_class(shade)

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

    unregister_class(menu_viewpoints)
    unregister_class(menu_edges)
    unregister_class(menu_pivot)
    unregister_class(menu_shade)

    unregister_class(ui_layout_set_sculpt)
    unregister_class(ui_layout_set_object)
    


    unregister_class(show_node_editor)
    