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
from bpy.types import Header, Menu, Panel
from bpy.app.translations import contexts as i18n_contexts

from bl_ui.space_topbar import (
    TOPBAR_MT_file,
    TOPBAR_MT_edit,
    TOPBAR_MT_render,
    TOPBAR_MT_window,
    TOPBAR_MT_help,
)


class workspace_set(bpy.types.Operator):

    bl_idname = "dks_ui.workspace_set"
    bl_label = "Workspace Set"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "Workspace Select"
    option_workspace : bpy.props.StringProperty(
        name="workspace",
        default = 'Modeling'
    )
    def execute(self, context):

        bpy.context.window.workspace = bpy.data.workspaces[self.option_workspace]
        
        #bpy.context.preferences.addons[__package__].preferences.option_ui_mode=self.option_workspace

        bpy.context.preferences.addons[__package__].preferences.option_active_workspace=self.option_workspace

        return {'FINISHED'} 
        
class MENU_MT_armatures(bpy.types.Menu):
    bl_label = "Armatures"
    def draw(self, context):
        layout = self.layout
        for ob in context.scene.objects:
            if ob.type == 'ARMATURE':
                layout.operator('dks_rigging.menu_armature_select',text=ob.name).option_value=ob.name


class render_and_display(bpy.types.Operator):

    bl_idname = "dks_ui.render_and_display"
    bl_label = "Render and Display"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_description = "Render and Display"
    def execute(self, context):

       # bpy.context.scene.render.display_mode = 'NONE'
        bpy.ops.render.render(use_viewport=True)
       # bpy.context.window.workspace = bpy.data.workspaces["Rendering"]

        return {'FINISHED'}    

class TOPBAR_MT_workspaces(Menu):
    bl_idname = "dks_ui.workspaces"
    bl_label = "WorkSpaces"
    def draw(self, context):
        layout = self.layout

        for _workspace in bpy.data.workspaces:

            layout.operator("dks_ui.workspace_set", text=_workspace.name).option_workspace = _workspace.name

class TOPBAR_HT_upper_bar(Header):
    bl_space_type = 'TOPBAR'

    def draw(self, context):
        region = context.region

        if region.alignment == 'RIGHT':
            self.draw_right(context)
        else:
            self.draw_left(context)

    def draw_left(self, context):
        layout = self.layout

        window = context.window
        screen = context.screen

        layout.operator("wm.splash", text="", icon='BLENDER', emboss=False)

        if bpy.context.preferences.addons[__package__].preferences.option_ui_menu_toggle_state:

            layout.operator('dks_ui.menu_toggle',text="",icon="TRIA_LEFT")

            layout.menu("TOPBAR_MT_file")
            layout.menu("TOPBAR_MT_edit")

            layout.menu("TOPBAR_MT_render")

            layout.menu("TOPBAR_MT_window")
            layout.menu("TOPBAR_MT_help")

        else:

            layout.operator('dks_ui.menu_toggle',text="",icon="TRIA_RIGHT")

        layout.label(text="",icon='THREE_DOTS')

        layout.operator('wm.read_homefile',text="",icon='FILE_NEW')
        layout.operator('wm.open_mainfile',text="",icon='FILEBROWSER')
        
        if bpy.data.is_dirty:
            save_emboss=True
        else:
            save_emboss=False

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="", icon='FILE_TICK', emboss=save_emboss)  

        layout.operator_context = 'INVOKE_AREA'
        layout.operator('wm.save_as_mainfile',text="",icon='GRIP')
        layout.operator('wm.revert_mainfile',text="",icon='FILE_REFRESH')

        layout.label(text="",icon='THREE_DOTS')

        layout.operator('ed.undo',text="",icon="LOOP_BACK")
        layout.operator('ed.redo',text="",icon="LOOP_FORWARDS")
        
        layout.label(text="",icon='THREE_DOTS')
        layout.operator("wm.search_menu", text="", icon='VIEWZOOM')
        layout.label(text="",icon='THREE_DOTS')

        layout.operator("render.render", text="", icon='RENDER_STILL').use_viewport = True

        anim_render = layout.operator("render.render", text="", icon='RENDER_ANIMATION')
        anim_render.use_viewport = True
        anim_render.animation = True

        workspace_ui_mode = bpy.context.preferences.addons[__package__].preferences.option_active_workspace
        workspace_icon_model = "LAYER_USED"
        workspace_icon_uv = "LAYER_USED"
        workspace_icon_anim = "LAYER_USED"

        if workspace_ui_mode == 'Modeling':
            workspace_icon_model = "LAYER_ACTIVE"
        elif workspace_ui_mode == 'UV Editing':
            workspace_icon_uv = "LAYER_ACTIVE"
        elif workspace_ui_mode == 'Animation':
            workspace_icon_anim = "LAYER_ACTIVE"
        
        layout.label(text="",icon='THREE_DOTS')

        layout.menu("dks_ui.workspaces", text=workspace_ui_mode)

        layout.operator("dks_ui.workspace_set", text="Model", icon=workspace_icon_model).option_workspace = 'Modeling'
        layout.operator("dks_ui.workspace_set", text="UV", icon=workspace_icon_uv).option_workspace = 'UV Editing'
        layout.operator("dks_ui.workspace_set", text="Anim", icon=workspace_icon_anim).option_workspace = 'Animation'
        
        if screen.show_fullscreen:
            layout.operator(
                "screen.back_to_previous",
                icon='SCREEN_BACK',
                text="Back to Previous",
            )
        
        layout.label(text="",icon='THREE_DOTS')
            
        layout.operator('import_scene.fbx',text="FBX",icon="IMPORT")
        layout.operator('export_scene.fbx',text="FBX",icon="EXPORT")

        if 'blender_addon_rizom_uv' in bpy.context.preferences.addons:

            layout.operator('dks_ruv.export',text="RUV",icon="EXPORT")
            layout.operator('dks_ruv.import',text="RUV",icon="IMPORT")

        if 'blender_addon_substance_painter' in bpy.context.preferences.addons:

            row = layout.row(align=True)

            if bpy.context.preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle:

                    if bpy.context.preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle_state:
                        row.operator('dks_sp.toggle',text="SP",icon="TRIA_LEFT")
                    else:
                        row.operator('dks_sp.toggle',text="SP",icon="TRIA_RIGHT")

            if bpy.context.preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle_state or not bpy.context.preferences.addons['blender_addon_substance_painter'].preferences.option_show_sp_toggle:

                    row.operator('dks_sp.export_scene',text="SP:Scene",icon="EXPORT")
                    row.operator('dks_sp.pbr_nodes', text='SP:Scene',icon="IMPORT").import_setting = 'scene'

                    row.operator('dks_sp.export_sel',text="SP:Sel",icon="EXPORT")
                    row.operator('dks_sp.pbr_nodes', text='SP:Sel', icon="IMPORT").import_setting = 'selected'

        if 'blender_addon_reallusion' in bpy.context.preferences.addons:

            row = layout.row(align=True)
            
            if bpy.context.preferences.addons['blender_addon_reallusion'].preferences.option_show_rl_toggle:

                if bpy.context.preferences.addons['blender_addon_reallusion'].preferences.option_show_rl_toggle_state:
                    row.operator('dks_rl.toggle',text="RL",icon="TRIA_LEFT")
                else:
                    row.operator('dks_rl.toggle',text="RL",icon="TRIA_RIGHT")

            if bpy.context.preferences.addons['blender_addon_reallusion'].preferences.option_show_rl_toggle_state or not bpy.context.preferences.addons['blender_addon_reallusion'].preferences.option_show_rl_toggle:

                row.operator("dks_rl.export_cc",text="CC",icon="EXPORT")
                row.operator("dks_rl.import_cc",text="CC",icon="IMPORT")
                row.operator("dks_rl.export_3dx",text="3DX",icon="EXPORT")
                row.operator("dks_rl.import_neutral",text="Neutral",icon="IMPORT")
                row.operator("dks_rl.import_female",text="Female",icon="IMPORT")
                row.operator("dks_rl.import_male",text="Male",icon="IMPORT")

        if 'blender_addon_ue' in bpy.context.preferences.addons:

            layout.operator('dks_ue.export',text="UE",icon="EXPORT")

        layout.label(text="",icon='THREE_DOTS')

    def draw_right(self, context):
        layout = self.layout

        window = context.window
        screen = context.screen
        scene = window.scene

        # If statusbar is hidden, still show messages at the top
        if not screen.show_statusbar:
            layout.template_reports_banner()
            layout.template_running_jobs()

        # stats
        scene = context.scene
        view_layer = context.view_layer

      #  layout.label(text=scene.statistics(view_layer), translate=False)
        layout.operator('wm.window_fullscreen_toggle',text="",icon='FULLSCREEN_ENTER')
        layout.operator('wm.console_toggle',text="",icon='CONSOLE')
        layout.operator('screen.userpref_show',text="",icon='PREFERENCES')
        layout.operator('dks_ui.quit',text="",icon='QUIT')

classes = (
    workspace_set,
    render_and_display,
    TOPBAR_HT_upper_bar,
    TOPBAR_MT_workspaces,
)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    

def unregister():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    