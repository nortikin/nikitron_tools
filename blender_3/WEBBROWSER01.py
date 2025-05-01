import bpy
import webview
import threading
from queue import Queue

# Глобальные переменные
webview_thread = None
webview_window = None
url_queue = Queue()

class BROWSER_OT_open_webview(bpy.types.Operator):
    bl_idname = "browser.open_webview"
    bl_label = "Open Browser"
    bl_description = "Open a web browser in a separate window"

    def execute(self, context):
        global webview_thread, webview_window

        url = context.scene.browser_url.strip()
        if not url:
            self.report({'ERROR'}, "URL is empty!")
            return {'CANCELLED'}

        # Если окно уже открыто, закрываем его
        if webview_window:
            webview_window.destroy()
            if webview_thread:
                webview_thread.join()

        # Запускаем новый поток
        webview_thread = threading.Thread(
            target=self.run_webview,
            args=(url,),
            daemon=True
        )
        webview_thread.start()

        return {'FINISHED'}

    def run_webview(self, url):
        global webview_window

        # Создаем окно webview (главный поток)
        webview_window = webview.create_window(
            "Blender Browser",
            url,
            width=1024,
            height=768,
            resizable=True,
        )

        # Запускаем веб-просмотрщик (блокирует поток)
        webview.start()

class BROWSER_OT_close_webview(bpy.types.Operator):
    bl_idname = "browser.close_webview"
    bl_label = "Close Browser"
    bl_description = "Close the web browser"

    def execute(self, context):
        global webview_window

        # Закрываем окно через API webview
        if webview_window:
            try:
                webview_window.destroy()
            except Exception as e:
                print(f"Error closing webview: {e}")

        return {'FINISHED'}

class BROWSER_PT_webview_panel(bpy.types.Panel):
    bl_label = "Blender Browser"
    bl_idname = "BROWSER_PT_webview_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Browser"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "browser_url", text="URL")
        row = layout.row()
        row.operator("browser.open_webview", icon="WORLD")
        row.operator("browser.close_webview", icon="CANCEL")

def register():
    bpy.utils.register_class(BROWSER_OT_open_webview)
    bpy.utils.register_class(BROWSER_OT_close_webview)
    bpy.utils.register_class(BROWSER_PT_webview_panel)
    bpy.types.Scene.browser_url = bpy.props.StringProperty(
        name="URL",
        description="Website URL (e.g., https://youtube.com)",
        default="https://www.youtube.com",
    )

def unregister():
    bpy.utils.unregister_class(BROWSER_OT_open_webview)
    bpy.utils.unregister_class(BROWSER_OT_close_webview)
    bpy.utils.unregister_class(BROWSER_PT_webview_panel)
    del bpy.types.Scene.browser_url

if __name__ == "__main__":
    register()