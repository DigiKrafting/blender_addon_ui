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

bl_info = {
        "name": "UI",
        "description": "UI Tweaks",
        "author": "Digiography.Studio",
        "version": (0, 7, 5),
        "blender": (2, 79, 0),
        "location": "Properties > Scene, Info Toolbar, 3D View Toolbar",
        "wiki_url":    "https://github.com/Digiography/blender_addon_pipeline/wiki",
        "tracker_url": "https://github.com/Digiography/blender_addon_pipeline/issues",
        "category": "System",
}

import bpy

from os import path, makedirs

class ds_ui_quit(bpy.types.Operator):
    bl_idname = "ds_ui.quit"
    bl_label = "Quit"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):
        
        bpy.ops.wm.save_userpref()

        if bpy.data.is_dirty:
            bpy.ops.wm.quit_blender('INVOKE_DEFAULT')
        else:
            bpy.ops.wm.quit_blender()

        return {'FINISHED'}

class ds_ui_cycles(bpy.types.Operator):

    bl_idname = "ds_ui.cycles"
    bl_label = "Set Render Engine to CYCLES"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
 
    def execute(self, context):

        bpy.context.scene.render.engine = 'CYCLES'

        return {'FINISHED'}

class ds_ui_addon_prefs(bpy.types.AddonPreferences):

    bl_idname = __package__

    # Global Options

    option_ui_mode = bpy.props.StringProperty(name="UI Mode",default='model',)
    option_ui_xray_state = bpy.props.BoolProperty(name="Xray Mode",default=False,)
    
    option_save_before_export = bpy.props.BoolProperty(name="Save Before Export",default=True,)

    # Info Toolbar

    option_info_obj_btns = bpy.props.BoolProperty(name="OBJ Import/Export",default=True,)
    option_info_fbx_btns = bpy.props.BoolProperty(name="FBX Import/Export",default=True,)

    option_info_blender_left = bpy.props.BoolProperty(name="Blender Icon Left",default=True,)

    option_info_standard = bpy.props.BoolProperty(name="Show",default=True,)
    option_info_standard_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_info_standard_state = bpy.props.BoolProperty(name="state",default=False,)
    
    option_info_file_icons = bpy.props.BoolProperty(name="New",default=True,)
    option_info_new = bpy.props.BoolProperty(name="New",default=True,)
    option_info_open = bpy.props.BoolProperty(name="Open",default=True,)
    option_info_save = bpy.props.BoolProperty(name="Save",default=True,)
    option_info_save_as = bpy.props.BoolProperty(name="Save As",default=True,)

    option_info_meshes = bpy.props.BoolProperty(name="Meshes",default=True,)
    option_info_mesh_select = bpy.props.BoolProperty(name="Auto Select First",default=True,)
    option_info_mesh_select_edit = bpy.props.BoolProperty(name=" Auto Edit",default=True,)
    option_info_mesh_select_all = bpy.props.BoolProperty(name="Auto Select All",default=False,)

    option_info_uvs = bpy.props.BoolProperty(name="Meshes",default=True,)
    option_info_uv_select = bpy.props.BoolProperty(name="Auto Select First",default=True,)
    option_info_uv_select_edit = bpy.props.BoolProperty(name=" Auto Edit",default=True,)
    option_info_uv_select_all = bpy.props.BoolProperty(name="Auto Select All",default=True,)

    option_info_armatures = bpy.props.BoolProperty(name="Armatures",default=True,)
    option_info_armature_select = bpy.props.BoolProperty(name="Armatures Select",default=True,)

    option_info_fullscreen = bpy.props.BoolProperty(name="Fullscreen",default=True,)
    option_info_console = bpy.props.BoolProperty(name="Console",default=True,)
    option_info_prefs = bpy.props.BoolProperty(name="Preferences",default=True,)
    option_info_quit = bpy.props.BoolProperty(name="Quit",default=True,)

    # View 3D Toolbar

    option_view3d_standard = bpy.props.BoolProperty(name="Show",default=True,)
    option_view3d_standard_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_standard_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_primitives = bpy.props.BoolProperty(name="Primitives",default=False,)
    option_view3d_primitives_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_primitives_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_edges = bpy.props.BoolProperty(name="Edges",default=False,)
    option_view3d_edges_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_edges_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_extrude = bpy.props.BoolProperty(name="Extrude",default=False,)
    option_view3d_extrude_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_extrude_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_faces = bpy.props.BoolProperty(name="Faces",default=False,)
    option_view3d_faces_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_faces_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_mesh = bpy.props.BoolProperty(name="Mesh",default=False,)
    option_view3d_mesh_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_mesh_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_cleanup = bpy.props.BoolProperty(name="Cleanup",default=False,)
    option_view3d_cleanup_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_cleanup_state = bpy.props.BoolProperty(name="state",default=False,)

    option_view3d_boolean = bpy.props.BoolProperty(name="Boolean",default=True,)
    option_view3d_boolean_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_boolean_state = bpy.props.BoolProperty(name="state",default=False,)    

    option_view3d_select_tools = bpy.props.BoolProperty(name="Select Mode Tools",default=False,)
    option_view3d_select_tools_toggle = bpy.props.BoolProperty(name='Toggle',default=True,)
    option_view3d_select_tools_state = bpy.props.BoolProperty(name="state",default=False,)

    option_active_armature = bpy.props.StringProperty(name="active_armature",default="",)
    
    active_object_name = bpy.props.StringProperty(name="active_object_name",default="",)
    active_object_mode = bpy.props.StringProperty(name="active_object_mode",default="",)

    def draw(self, context):

        layout = self.layout

        layout.label('Standard',icon='UI')

        row = layout.row(align=True)

        col = row.column()
        subrow = col.row()

        box=subrow.box()
        box.label('Info Toolbar',icon='UI')
        box.prop(self, 'option_info_standard')
        box.prop(self, 'option_info_standard_toggle')
        
        box.label('View 3D Toolbar',icon='UI')
        box.prop(self, 'option_view3d_standard')
        box.prop(self, 'option_view3d_standard_toggle')

def register():

    from bpy.utils import register_class

    register_class(ds_ui_addon_prefs)

    register_class(ds_ui_quit)

    from . import ds_ui
    ds_ui.register()

    from . import ds_model
    ds_model.register()

    from . import ds_rigging
    ds_rigging.register()

    from . import ds_uv
    ds_uv.register()

    from . import space_info 
    from . import space_view3d

    register_class(space_info.INFO_HT_header)
    register_class(space_view3d.VIEW3D_HT_header)

def unregister():

    from bpy.utils import unregister_class

    unregister_class(ds_ui_addon_prefs)

    unregister_class(ds_ui_quit)

    from . import ds_ui
    ds_ui.unregister()

    from . import ds_model
    ds_model.unregister()

    from . import ds_rigging
    ds_rigging.unregister()

    from . import ds_uv
    ds_uv.unregister()

    from . import space_info 
    from . import space_view3d

    unregister_class(space_info.INFO_HT_header)
    unregister_class(space_view3d.VIEW3D_HT_header)    

