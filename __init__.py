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
        "version": (0, 5, 0),
        "blender": (2, 79, 0),
        "location": "3D View Toolbar",
        "wiki_url":    "https://github.com/Digiography/blender_addon_3dview_toolbar/wiki",
        "tracker_url": "https://github.com/Digiography/blender_addon_3dview_toolbar/issues",
        "category": "3D View",
}

import bpy

def register():

    from bpy.utils import register_class

    from . import space_view3d 

    register_class(space_view3d.VIEW3D_HT_header)

    from . import ds_3d_view
    ds_3d_view.register()

def unregister():

    from bpy.utils import unregister_class

    from . import ds_3d_view
    ds_3d_view.unregister()

    from . import space_view3d 

    unregister_class(space_view3d.VIEW3D_HT_header)

if __name__ == "__main__":

	register()