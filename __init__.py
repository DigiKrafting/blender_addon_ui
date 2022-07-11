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
        "name": "DKS UI",
        "description": "UI Customisations",
        "author": "DigiKrafting.Studio",
        "version": (0, 8, 2),
        "blender": (3, 0, 0),
        "location": "Properties > Scene, Info Toolbar, 3D View Toolbar",
        "wiki_url":    "https://github.com/DigiKrafting/blender_addon_ui/wiki",
        "tracker_url": "https://github.com/DigiKrafting/blender_addon_ui/issues",
        "category": "System",
}

import bpy
from bpy.utils import register_class, unregister_class
from os import path, makedirs
from . import dks_ui
from . import dks_globals

import bpy.utils.previews


class dks_ui_quit(bpy.types.Operator):
    bl_idname = "dks_ui.quit"
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

class dks_ui_cycles(bpy.types.Operator):

    bl_idname = "dks_ui.cycles"
    bl_label = "Set Render Engine to CYCLES"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
 
    def execute(self, context):

        bpy.context.scene.render.engine = 'CYCLES'

        return {'FINISHED'}

class dks_ui_addon_prefs(bpy.types.AddonPreferences):

    bl_idname = __package__

    # Global Options

    option_active_workspace : bpy.props.StringProperty(name="active_workspace",default="Modeling",)

    option_ui_mode : bpy.props.EnumProperty(
            items=[('Modeling', "Modeling", "Modeling"),('UV Editing', "UV Editing", "UV Editing"),('Animation', "Animation", "Animation"),],
            name="UI Mode",
            default='Modeling',
    )

    option_ui_menu_toggle_state : bpy.props.BoolProperty(
            name="Menu Toggle State",
            default=False,
    )

    option_active_armature : bpy.props.StringProperty(name="active_armature",default="",)

    def draw(self, context):

        layout = self.layout

        box=layout.box()
        box.prop(self, 'option_ui_mode')

class dks_ui_menu_toggle(bpy.types.Operator):

    bl_idname = "dks_ui.menu_toggle"
    bl_label = "SP"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    
    def execute(self, context):

        if not bpy.context.preferences.addons[__package__].preferences.option_ui_menu_toggle_state:
            bpy.context.preferences.addons[__package__].preferences.option_ui_menu_toggle_state=True
        else:
            bpy.context.preferences.addons[__package__].preferences.option_ui_menu_toggle_state=False
        return {'FINISHED'}

classes = (
    dks_ui_addon_prefs,
    dks_ui_quit,
    dks_ui_menu_toggle,
)

def register():

    for cls in classes:
        register_class(cls)
    
    global icons

    icons = bpy.utils.previews.new()
    icons_dir = path.join(path.dirname(__file__), "icons")
    icons.load("DKS_VIEW_FRONT", path.join(icons_dir, "view_front.png"), 'IMAGE')
    icons.load("DKS_VIEW_BACK", path.join(icons_dir, "view_back.png"), 'IMAGE')
    icons.load("DKS_VIEW_LEFT", path.join(icons_dir, "view_left.png"), 'IMAGE')
    icons.load("DKS_VIEW_RIGHT", path.join(icons_dir, "view_right.png"), 'IMAGE')
    icons.load("DKS_VIEW_TOP", path.join(icons_dir, "view_top.png"), 'IMAGE')
    icons.load("DKS_VIEW_BOTTOM", path.join(icons_dir, "view_bottom.png"), 'IMAGE')

    dks_ui.register()

    from . import dks_rigging
    dks_rigging.register()

    from . import dks_modeling
    dks_modeling.register()

    from . import space_view3d
    space_view3d.preview_collections["main"] = icons
  
    register_class(space_view3d.VIEW3D_HT_header)

def unregister():

    dks_ui.unregister()

    for cls in reversed(classes):
        unregister_class(cls)
 
    from . import dks_rigging
    dks_rigging.unregister()
    
    from . import dks_modeling
    dks_modeling.unregister()

    from . import space_view3d

    unregister_class(space_view3d.VIEW3D_HT_header)            

    space_view3d.preview_collections.clear()
