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
        "name": "Toolbar Replacement",
        "description": "Custom 3D View Toolbar",
        "author": "Digiography.Studio",
        "version": (0, 6, 5),
        "blender": (2, 79, 0),
        "location": "3D View Toolbar",
        "wiki_url":    "https://github.com/Digiography/blender_addon_3dview_toolbar/wiki",
        "tracker_url": "https://github.com/Digiography/blender_addon_3dview_toolbar/issues",
        "category": "3D View",
}

import bpy

from bpy.props import (StringProperty,BoolProperty,IntProperty,FloatProperty,FloatVectorProperty,EnumProperty,PointerProperty,)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup,)

class ds_3d_view_addon_prefs(AddonPreferences):

    bl_idname = __package__

    option_show_uv = BoolProperty(
        name="UV",
        default = True
    )
    option_show_edit_select = BoolProperty(
        name="Select",
        default = True
    )
    option_show_edit_delete = BoolProperty(
        name="Delete",
        default = True
    )
    option_show_views = BoolProperty(
        name="Viewport Shade",
        default = True
    )
    option_show_viewpoints = BoolProperty(
        name="Viewpoints",
        default = True
    )
    option_show_modes = BoolProperty(
        name="Edit/Object",
        default = True
    )
    option_show_selection = BoolProperty(
        name="Selection",
        default = True
    )
    option_hide_menu = BoolProperty(
        name="Menu",
        default = True
    )
    option_show_menu_toggle = BoolProperty(
        name="Menu Toggle",
        default = True
    )
    option_show_menu_toggle_state = BoolProperty(
        name="Menu Toogle State",
        default = False
    )    
    option_hide_3d = BoolProperty(
        name="Default 3D Panel",
        default = True
    )
    option_hide_3d_switcher = BoolProperty(
        name="Toolbar Switcher",
        default = True
    )
    option_hide_snap = BoolProperty(
        name="Snap",
        default = True
    )
    option_hide_opengl_render = BoolProperty(
        name="OpenGL Render",
        default = True
    )
    option_show_viewpoints_toggle = BoolProperty(
        name="Viewpoints Toggle",
        default = True
    )
    option_show_viewpoints_toggle_state = BoolProperty(
        name="Viewpoints Toogle State",
        default = False
    )    
    def draw(self, context):

        layout = self.layout

        row = layout.row(align=True)
        
        col = row.column()
        subrow = col.row()

        box=subrow.box()
        box.label('Hide',icon='UI')
        box.prop(self, 'option_hide_menu')
        box.prop(self, 'option_hide_3d')
        box.prop(self, 'option_hide_3d_switcher')
        box.prop(self, 'option_hide_snap')
        box.prop(self, 'option_hide_opengl_render')

        box=subrow.box()
        box.label('Show',icon='UI')
        box.prop(self, 'option_show_menu_toggle')
        box.prop(self, 'option_show_viewpoints_toggle')
        box.prop(self, 'option_show_views')
        box.prop(self, 'option_show_viewpoints')
        box.prop(self, 'option_show_modes')
        box.prop(self, 'option_show_selection')
        box.prop(self, 'option_show_edit_select')
        box.prop(self, 'option_show_edit_delete')
        box.prop(self, 'option_show_uv')


def register():

    from bpy.utils import register_class

    register_class(ds_3d_view_addon_prefs)

    from . import ds_3d_view

    register_class(ds_3d_view.ds_3d_view_menu_toggle)
    register_class(ds_3d_view.ds_3d_view_viewpoints_toggle)
    register_class(ds_3d_view.ds_3d_view_edit)
    register_class(ds_3d_view.ds_3d_view_object)

    register_class(ds_3d_view.ds_3d_view_select_all)
    register_class(ds_3d_view.ds_3d_view_select_none)

    register_class(ds_3d_view.ds_3d_view_edit_vertex_delete)
    register_class(ds_3d_view.ds_3d_view_edit_edge_delete)
    register_class(ds_3d_view.ds_3d_view_edit_face_delete)

    from . import space_view3d 

    register_class(space_view3d.VIEW3D_HT_header)



def unregister():

    from bpy.utils import unregister_class
    
    unregister_class(ds_3d_view_addon_prefs)

    from . import ds_3d_view

    unregister_class(ds_3d_view.ds_3d_view_menu_toggle)
    unregister_class(ds_3d_view.ds_3d_view_viewpoints_toggle)
    unregister_class(ds_3d_view.ds_3d_view_edit)
    unregister_class(ds_3d_view.ds_3d_view_object)

    unregister_class(ds_3d_view.ds_3d_view_select_all)
    unregister_class(ds_3d_view.ds_3d_view_select_none)

    unregister_class(ds_3d_view.ds_3d_view_edit_vertex_delete)
    unregister_class(ds_3d_view.ds_3d_view_edit_edge_delete)
    unregister_class(ds_3d_view.ds_3d_view_edit_face_delete)

    from . import space_view3d 

    unregister_class(space_view3d.VIEW3D_HT_header)

if __name__ == "__main__":

	register()