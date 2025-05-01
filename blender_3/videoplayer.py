bl_info = {
    "name": "SV_videoplayer",
    "version": (0, 5, 0),
    "blender": (4, 2, 0),
    "category": "Misc",
    "author": "nikitron",
    "location": "View3D > Tool Shelf > SV",
    "description": "Video player",
    "warning": "Early alpha",
    "wiki_url": "https://t.me/sverchok_3d",
    "tracker_url": "https://t.me/sverchok_3d",
}


import bpy
import numpy as np
import threading
import ffmpeg
import time

class VideoPlayer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.running = False
        self.texture = None
        self.width, self.height = 0, 0

    def play(self):
        probe = ffmpeg.probe(self.filepath)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        self.width = int(video_info['width'])
        self.height = int(video_info['height'])

        # Создаем текстуру в Blender
        if f"video_tex_{self.filepath}" not in bpy.data.images:
            bpy.data.images.new(
                name=f"video_tex_{self.filepath}",
                width=self.width,
                height=self.height
            )
        self.texture = bpy.data.images[f"video_tex_{self.filepath}"]
        
        # Запускаем поток воспроизведения
        self.running = True
        threading.Thread(target=self._update_frame, daemon=True).start()

    def _update_frame(self):
        process = (
            ffmpeg
            .input(self.filepath)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True)
        )

        while self.running:
            in_bytes = process.stdout.read(self.width * self.height * 3)
            if not in_bytes:
                break
            
            # Конвертируем в numpy-массив и обновляем текстуру
            frame = np.frombuffer(in_bytes, np.uint8).reshape(self.height, self.width, 3)
            self.texture.pixels = frame.ravel().tolist()
            time.sleep(1/30)  # ~30 FPS

        process.terminate()

class OT_VIDEO_OT_play(bpy.types.Operator):
    bl_idname = "video.play"
    bl_label = "Play Video"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        player = VideoPlayer(self.filepath)
        player.play()
        return {'FINISHED'}

class PT_VIDEO_PT_panel(bpy.types.Panel):
    bl_label = "Video Player"
    bl_idname = "PT_VIDEO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SV"


    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "sv_videoplayerpath", text='filepath')
        layout.operator("video.play").filepath = "//video.mp4"  # Относительный путь

def register():
    bpy.utils.register_class(OT_VIDEO_OT_play)
    bpy.utils.register_class(PT_VIDEO_PT_panel)
    bpy.types.Scene.sv_videoplayerpath = bpy.props.StringProperty(
        subtype="FILE_PATH",
        name="path",
        description="Path to file",
        default="//video.mp4",
    )

def unregister():
    bpy.utils.unregister_class(OT_VIDEO_OT_play)
    bpy.utils.unregister_class(PT_VIDEO_PT_panel)
    del bpy.types.Scene.sv_videoplayerpath

if __name__ == '__main__':
    register()