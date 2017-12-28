# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
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

# <pep8 compliant>
import bpy
from bpy.types import Header, Menu

from . import ds_ui 

class INFO_HT_header(Header):
    bl_space_type = 'INFO'

    def draw(self, context):

        layout = self.layout

        window = context.window
        scene = context.scene
        rd = scene.render

        if ds_ui.option_show('info_blender_left'):
        
            layout.operator("wm.splash", text="", icon='BLENDER', emboss=False)

        if ds_ui.toggle_show('info_standard'):
            layout.operator('ds_ui.toggle',icon='TRIA_RIGHT',text="").option_toggle='info_standard'
        
        if ds_ui.toggle_draw('info_standard'):

            row = layout.row(align=True)
            row.template_header()
            
            INFO_MT_editor_menus.draw_collapsible(context, layout)

            if window.screen.show_fullscreen:
                layout.operator("screen.back_to_previous", icon='SCREEN_BACK', text="Back to Previous")
                layout.separator()
            else:
                layout.template_ID(context.window, "screen", new="screen.new", unlink="screen.delete")
                layout.template_ID(context.screen, "scene", new="scene.new", unlink="scene.delete")

            layout.separator()

            if rd.has_multiple_engines:
                layout.prop(rd, "engine", text="")

            layout.separator()

            layout.template_running_jobs()

            layout.template_reports_banner()

            row = layout.row(align=True)

            if bpy.app.autoexec_fail is True and bpy.app.autoexec_fail_quiet is False:
                row.label("Auto-run disabled", icon='ERROR')
                if bpy.data.is_saved:
                    props = row.operator("wm.revert_mainfile", icon='SCREEN_BACK', text="Reload Trusted")
                    props.use_scripts = True

                row.operator("script.autoexec_warn_clear", text="Ignore")

                # include last so text doesn't push buttons out of the header
                row.label(bpy.app.autoexec_fail_message)
                return

            row.operator("wm.splash", text="", icon='BLENDER', emboss=False)
            row.label(text=scene.statistics(), translate=False)
        
        _ui_mode = ds_ui.ui_mode()
        _obj_mode = context.mode
        _obj = context.active_object

        if ds_ui.option_show('info_new'):
            if ds_ui.option_show('info_file_icons'):
                _text=""
            else:
                _text="New"
            layout.operator('wm.read_homefile',text=_text,icon='NEW')

        if ds_ui.option_show('info_open'):
            if ds_ui.option_show('info_file_icons'):
                _text=""
            else:
                _text="Open"
            layout.operator('wm.open_mainfile',text=_text,icon='FILE_FOLDER')

        if ds_ui.option_show('info_save'):
            if ds_ui.option_show('info_file_icons'):
                _text=""
            else:
                _text="Save"
            layout.operator('ds_ui.save',text=_text,icon='FILE_TICK')

        if ds_ui.option_show('info_save_as'):
            if ds_ui.option_show('info_file_icons'):
                _text=""
            else:
                _text="Save As"
            layout.operator('wm.save_as_mainfile',text=_text,icon='SAVE_AS')
        
        if ds_ui.option_show('info_file_icons'):
            _text=""
        else:
            _text="Revert"
        layout.operator('wm.revert_mainfile',text=_text,icon='FILE_REFRESH')


        if ds_ui.option_show('info_file_icons'):
            _text=""
        else:
            _text="Undo"
        layout.operator('ds_ui.undo',text=_text,icon="LOOP_BACK")
        if ds_ui.option_show('info_file_icons'):
            _text=""
        else:
            _text="Redo"
        layout.operator('ds_ui.redo',text=_text,icon="LOOP_FORWARDS")
        
        # UI Layout Buttons

        if _ui_mode=='model':
            _icon='COLOR_GREEN'
        else:
            _icon='META_EMPTY'
        layout.operator('ds_ui.ui_layout_set',text="Model",icon=_icon).option_value = 'model'

        if _ui_mode=='rig':
            _icon='COLOR_GREEN'
        else:
            _icon='META_EMPTY'
        layout.operator('ds_ui.ui_layout_set',text="Rigging",icon=_icon).option_value = 'rig'

        if _ui_mode=='uv':
            _icon='COLOR_GREEN'
        else:
            _icon='META_EMPTY'
        layout.operator('ds_ui.ui_layout_set',text="UV",icon=_icon).option_value = 'uv'

        # UI Layout Menus

        if _ui_mode=='model':
            if ds_ui.option_show('info_meshes'):
                layout.menu('ds_ui.info_meshes_edit_menu',icon="TRIA_DOWN")
        elif _ui_mode=='rig':
            if ds_ui.option_show('info_armatures'):
                layout.menu('ds_ui.info_armatures_menu',icon="TRIA_DOWN")
            if ds_ui.option_show('info_meshes'):
                layout.menu('ds_ui.info_meshes_menu',icon="TRIA_DOWN")
            if _obj_mode=='PAINT_WEIGHT':
                layout.menu('ds_ui.info_vertex_groups_menu',icon="TRIA_DOWN")

        elif _ui_mode=='uv':
            if ds_ui.option_show('info_uvs'):
                layout.menu('ds_ui.info_uv_menu',icon="TRIA_DOWN")
        
        # UI Menus

        if _ui_mode=='model' and (_obj_mode=='OBJECT' or _obj_mode=='EDIT_MESH'):

            layout.menu("INFO_MT_mesh_add",icon='OUTLINER_OB_MESH')

        if _obj_mode=='EDIT_MESH' and (_ui_mode=='model' or _ui_mode=='uv'):

            layout.menu("VIEW3D_MT_edit_mesh",icon='COLLAPSEMENU')

        if _ui_mode=='model':

            if _obj_mode=='OBJECT':

                layout.menu("INFO_MT_curve_add", icon='OUTLINER_OB_CURVE')

            elif _obj_mode=='EDIT_CURVE':

                layout.menu("VIEW3D_MT_edit_curve",icon='COLLAPSEMENU')

            elif _obj_mode=='EDIT_MESH':

                _select_mode=bpy.context.scene.tool_settings.mesh_select_mode

                if _select_mode[0]:
                    layout.menu("VIEW3D_MT_edit_mesh_vertices",icon='COLLAPSEMENU')
                if _select_mode[1]:
                    layout.menu("VIEW3D_MT_edit_mesh_edges",icon='COLLAPSEMENU')
                if _select_mode[2]:
                    layout.menu("VIEW3D_MT_edit_mesh_faces",icon='COLLAPSEMENU')

        elif _ui_mode=='rig':

            if _obj_mode=='OBJECT':

                layout.menu("INFO_MT_armature_add",icon='BONE_DATA')

            elif _obj_mode=='EDIT_ARMATURE':

                layout.menu("INFO_MT_edit_armature_add",icon='BONE_DATA')

                layout.menu("VIEW3D_MT_edit_armature",icon='COLLAPSEMENU')

            if _obj:

                if _obj.show_x_ray==True:
                    _icon='OUTLINER_DATA_ARMATURE'
                else:
                    _icon='ARMATURE_DATA'
                
                layout.operator("wm.context_toggle", text="X-Ray", icon=_icon).data_path = "scene.objects.active.show_x_ray"

        # UI Edit Mode

        if _ui_mode=='model':

                #layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'
                #layout.operator('object.mode_set',text="Sculpt",icon="SCULPTMODE_HLT").mode='SCULPT'

            if _obj_mode=='OBJECT':
                if _obj and _obj.type=='MESH':
                    layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'
                    layout.operator('object.mode_set',text="Sculpt",icon="SCULPTMODE_HLT").mode='SCULPT'
            elif _obj_mode=='EDIT_MESH':
                layout.operator('ds_ui.ui_layout_set_object',text="Object",icon="OBJECT_DATAMODE")
                layout.operator('ds_ui.ui_layout_set_sculpt',text="Sculpt",icon="SCULPTMODE_HLT")
            elif _obj_mode=='SCULPT':
                layout.operator('object.mode_set',text="Edit",icon="EDITMODE_HLT").mode='EDIT'
                layout.operator('ds_ui.ui_layout_set_object',text="Object",icon="OBJECT_DATAMODE")

        elif _ui_mode=='rig':

            if _obj_mode=='EDIT_ARMATURE':
                layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'
                layout.operator('object.mode_set',text="Pose Mode",icon="POSE_HLT").mode='POSE'

            elif _obj_mode=='POSE':
                layout.operator('object.mode_set',text="Edit Mode",icon="EDITMODE_HLT").mode='EDIT'
                layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'

            elif _obj_mode=='OBJECT':
                if _obj and _obj.type=='MESH':
                    
                    #layout.operator('object.mode_set',text="Edit Mode",icon="EDITMODE_HLT").mode='EDIT'
                    layout.operator('object.mode_set',text="Weight Paint",icon="WPAINT_HLT").mode='WEIGHT_PAINT'

            elif _obj_mode=='PAINT_WEIGHT':

                if _obj:
                    layout.operator('object.mode_set',text="Object",icon="OBJECT_DATAMODE").mode='OBJECT'
            


            #if _obj:
            #    layout.operator('ds_ui.ui_layout_set_weightpaint',text="WEIGHT PAINT",icon="WPAINT_HLT")

        # UI Import/Export

        if ds_ui.option_show('info_obj_btns'):

            layout.operator('import_scene.obj',text="OBJ",icon="IMPORT")
            layout.operator('export_scene.obj',text="OBJ",icon="EXPORT")

        if ds_ui.option_show('info_fbx_btns'):

            layout.operator('import_scene.fbx',text="FBX",icon="IMPORT")
            layout.operator('export_scene.fbx',text="FBX",icon="EXPORT")

        # DS Pipeline Buttons

        if 'blender_addon_pipeline' in bpy.context.user_preferences.addons:

            if bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_zbc:

                self.layout.operator('ds_zbc.export',text="ZBC",icon="EXPORT")
                self.layout.operator('ds_zbc.import',text="ZBC",icon="IMPORT")

            if bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_sp:

                self.layout.operator('ds_sp.export_all',text="SP:All",icon="LINK_BLEND")
                self.layout.operator('ds_sp.export_obj',text="SP:OBJ",icon="LINK_BLEND")

            if bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_ic and bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_iclone_toggle:

                layout.operator('ds_pipeline.iclone_toggle',icon='TRIA_RIGHT')
            
            if (not bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_iclone_toggle and bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_ic) or (bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_ic and bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_iclone_toggle and bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_iclone_toggle_state):

                layout.operator('ds_ic.import_base',text="Base",icon="IMPORT")
                layout.operator('ds_ic.import_female',text="Female",icon="IMPORT")
                layout.operator('ds_ic.import_male',text="Male",icon="IMPORT")

                layout.operator('ds_ic.export_cc',text="CC",icon="LINK_BLEND")
                layout.operator('ds_ic.export_3dx',text="3DX",icon="EXPORT")
                layout.operator('ds_ic.export_ic',text="IC",icon="LINK_BLEND")

            if bpy.context.user_preferences.addons['blender_addon_pipeline'].preferences.option_show_daz3d:

                self.layout.operator('ds_daz3d.export',text="Daz3D",icon="LINK_BLEND")

        # Extra Buttons

        if ds_ui.option_show('info_fullscreen'):
            layout.operator('wm.window_fullscreen_toggle',text="",icon='FULLSCREEN_ENTER')

        if ds_ui.option_show('info_prefs'):
            layout.operator('screen.userpref_show',text="",icon='PREFERENCES')

        if ds_ui.option_show('info_console'):
            layout.operator('wm.console_toggle',text="",icon='CONSOLE')

        if ds_ui.option_show('info_quit'):
            layout.operator('ds_ui.quit',text="",icon='QUIT')

        layout.label(text=scene.statistics(), translate=False)

class INFO_MT_editor_menus(Menu):
    bl_idname = "INFO_MT_editor_menus"
    bl_label = ""

    def draw(self, context):
        self.draw_menus(self.layout, context)

    @staticmethod
    def draw_menus(layout, context):
        scene = context.scene
        rd = scene.render

        layout.menu("INFO_MT_file")

        if rd.use_game_engine:
            layout.menu("INFO_MT_game")
        else:
            layout.menu("INFO_MT_render")

        layout.menu("INFO_MT_window")
        layout.menu("INFO_MT_help")


class INFO_MT_file(Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.read_homefile", text="New", icon='NEW')
        layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
        layout.menu("INFO_MT_file_open_recent", icon='OPEN_RECENT')
        layout.operator("wm.revert_mainfile", icon='FILE_REFRESH')
        layout.operator("wm.recover_last_session", icon='RECOVER_LAST')
        layout.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')

        layout.separator()

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save Copy...", icon='SAVE_COPY').copy = True

        layout.separator()

        layout.operator("screen.userpref_show", text="User Preferences...", icon='PREFERENCES')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_homefile", icon='SAVE_PREFS')
        layout.operator("wm.read_factory_settings", icon='LOAD_FACTORY')

        if any(bpy.utils.app_template_paths()):
            app_template = context.user_preferences.app_template
            if app_template:
                layout.operator(
                    "wm.read_factory_settings",
                    text="Load Factory Template Settings",
                    icon='LOAD_FACTORY',
                ).app_template = app_template
            del app_template

        layout.menu("USERPREF_MT_app_templates", icon='FILE_BLEND')

        layout.separator()

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.link", text="Link", icon='LINK_BLEND')
        layout.operator("wm.append", text="Append", icon='APPEND_BLEND')
        layout.menu("INFO_MT_file_previews")

        layout.separator()

        layout.menu("INFO_MT_file_import", icon='IMPORT')
        layout.menu("INFO_MT_file_export", icon='EXPORT')

        layout.separator()

        layout.menu("INFO_MT_file_external_data", icon='EXTERNAL_DATA')

        layout.separator()

        layout.operator_context = 'EXEC_AREA'
        if bpy.data.is_dirty and context.user_preferences.view.use_quit_dialog:
            layout.operator_context = 'INVOKE_SCREEN'  # quit dialog
        layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


class INFO_MT_file_import(Menu):
    bl_idname = "INFO_MT_file_import"
    bl_label = "Import"

    def draw(self, context):
        if bpy.app.build_options.collada:
            self.layout.operator("wm.collada_import", text="Collada (Default) (.dae)")
        if bpy.app.build_options.alembic:
            self.layout.operator("wm.alembic_import", text="Alembic (.abc)")


class INFO_MT_file_export(Menu):
    bl_idname = "INFO_MT_file_export"
    bl_label = "Export"

    def draw(self, context):
        if bpy.app.build_options.collada:
            self.layout.operator("wm.collada_export", text="Collada (Default) (.dae)")
        if bpy.app.build_options.alembic:
            self.layout.operator("wm.alembic_export", text="Alembic (.abc)")


class INFO_MT_file_external_data(Menu):
    bl_label = "External Data"

    def draw(self, context):
        layout = self.layout

        icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
        layout.operator("file.autopack_toggle", icon=icon)

        layout.separator()

        pack_all = layout.row()
        pack_all.operator("file.pack_all")
        pack_all.active = not bpy.data.use_autopack

        unpack_all = layout.row()
        unpack_all.operator("file.unpack_all")
        unpack_all.active = not bpy.data.use_autopack

        layout.separator()

        layout.operator("file.make_paths_relative")
        layout.operator("file.make_paths_absolute")
        layout.operator("file.report_missing_files")
        layout.operator("file.find_missing_files")


class INFO_MT_file_previews(Menu):
    bl_label = "Data Previews"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.previews_ensure")
        layout.operator("wm.previews_batch_generate")

        layout.separator()

        layout.operator("wm.previews_clear")
        layout.operator("wm.previews_batch_clear")


class INFO_MT_game(Menu):
    bl_label = "Game"

    def draw(self, context):
        layout = self.layout

        gs = context.scene.game_settings

        layout.operator("view3d.game_start")

        layout.separator()

        layout.prop(gs, "show_debug_properties")
        layout.prop(gs, "show_framerate_profile")
        layout.prop(gs, "show_physics_visualization")
        layout.prop(gs, "use_deprecation_warnings")
        layout.prop(gs, "use_animation_record")
        layout.separator()
        layout.prop(gs, "use_auto_start")


class INFO_MT_render(Menu):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        layout.operator("render.render", text="Render Image", icon='RENDER_STILL').use_viewport = True
        props = layout.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION')
        props.animation = True
        props.use_viewport = True

        layout.separator()

        layout.operator("render.opengl", text="OpenGL Render Image")
        layout.operator("render.opengl", text="OpenGL Render Animation").animation = True
        layout.menu("INFO_MT_opengl_render")

        layout.separator()

        layout.operator("render.view_show")
        layout.operator("render.play_rendered_anim", icon='PLAY')


class INFO_MT_opengl_render(Menu):
    bl_label = "OpenGL Render Options"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        layout.prop(rd, "use_antialiasing")
        layout.prop(rd, "use_full_sample")

        layout.prop_menu_enum(rd, "antialiasing_samples")
        layout.prop_menu_enum(rd, "alpha_mode")


class INFO_MT_window(Menu):
    bl_label = "Window"

    def draw(self, context):
        import sys

        layout = self.layout

        layout.operator("wm.window_duplicate")
        layout.operator("wm.window_fullscreen_toggle", icon='FULLSCREEN_ENTER')

        layout.separator()

        layout.operator("screen.screenshot")
        layout.operator("screen.screencast")

        if sys.platform[:3] == "win":
            layout.separator()
            layout.operator("wm.console_toggle", icon='CONSOLE')

        if context.scene.render.use_multiview:
            layout.separator()
            layout.operator("wm.set_stereo_3d", icon='CAMERA_STEREO')


class INFO_MT_help(Menu):
    bl_label = "Help"

    def draw(self, context):
        layout = self.layout

        layout.operator(
                "wm.url_open", text="Manual", icon='HELP',
                ).url = "https://docs.blender.org/manual/en/dev/"
        layout.operator(
                "wm.url_open", text="Release Log", icon='URL',
                ).url = "http://wiki.blender.org/index.php/Dev:Ref/Release_Notes/%d.%d" % bpy.app.version[:2]
        layout.separator()

        layout.operator(
                "wm.url_open", text="Blender Website", icon='URL',
                ).url = "https://www.blender.org"
        layout.operator(
                "wm.url_open", text="Blender Store", icon='URL',
                ).url = "https://store.blender.org"
        layout.operator(
                "wm.url_open", text="Developer Community", icon='URL',
                ).url = "https://www.blender.org/get-involved/"
        layout.operator(
                "wm.url_open", text="User Community", icon='URL',
                ).url = "https://www.blender.org/support/user-community"
        layout.separator()
        layout.operator(
                "wm.url_open", text="Report a Bug", icon='URL',
                ).url = "https://developer.blender.org/maniphest/task/edit/form/1"
        layout.separator()

        layout.operator(
                "wm.url_open", text="Python API Reference", icon='URL',
                ).url = bpy.types.WM_OT_doc_view._prefix

        layout.operator("wm.operator_cheat_sheet", icon='TEXT')
        layout.operator("wm.sysinfo", icon='TEXT')
        layout.separator()

        layout.operator("wm.splash", icon='BLENDER')


classes = (
    INFO_HT_header,
    INFO_MT_editor_menus,
    INFO_MT_file,
    INFO_MT_file_import,
    INFO_MT_file_export,
    INFO_MT_file_external_data,
    INFO_MT_file_previews,
    INFO_MT_game,
    INFO_MT_render,
    INFO_MT_opengl_render,
    INFO_MT_window,
    INFO_MT_help,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)