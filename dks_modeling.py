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

class object_center(bpy.types.Operator):

    bl_label = "Center Object"
    bl_idname = "dks_modeling.object_center"

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')

        return {'FINISHED'}    

class object_transform_apply(bpy.types.Operator):

    bl_label = "Transform Apply"
    bl_idname = "dks_modeling.object_transform_apply"

    def execute(self, context):

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        return {'FINISHED'}    

class object_origin_geometry(bpy.types.Operator):

    bl_label = "Origin to Geometry"
    bl_idname = "dks_modeling.object_origin_geometry"

    def execute(self, context):

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        return {'FINISHED'}    

class object_remove_doubles(bpy.types.Operator):

    bl_label = "Remove Doubles"
    bl_idname = "dks_modeling.object_remove_doubles"

    def execute(self, context):

        #bpy.ops.mesh.select_all(action='SELECT')
        #bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.remove_doubles(threshold=0.1, use_unselected=True)

        return {'FINISHED'}    
    
class object_normals_reset(bpy.types.Operator):

    bl_label = "Normals Reset"
    bl_idname = "dks_modeling.object_normals_reset"

    def execute(self, context):

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_tools(mode='RESET')

        return {'FINISHED'}    
        
classes = (
    object_center,
    object_transform_apply,
    object_origin_geometry,
    object_remove_doubles,
    object_normals_reset
)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)