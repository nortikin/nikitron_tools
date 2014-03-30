bl_info = {
    "name": "Music Player",
    "author": "edddy <edddy74@live.fr> + nikitron.cc.ua a little",
    "version": (0, 1, 131),
    "blender": (2, 59, 0),
    "api": 34074,
    "location": "View3D > Tool Shelf > Music Player",
    "description": "A Little Music Player for Blender",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Misc"}

from bpy_extras.io_utils import ImportHelper
from bpy.props import *
import bpy, aud, time, threading
import re
import urllib.request as req

#itemdefault = req.urlopen('http://mp3vega.com/down-v1/4770v4/7a374117a2fd/u52089946/audios/testovaya_muzyka_melodiya_super_-_angel_skoro_budet_moya_1_pesnyaot_k_angel%20MP3VEGA.COM.mp3').read()
#bpy.context.window_manager.playlist.append(itemdefault)
bpy.types.WindowManager.show_names = bpy.props.BoolProperty(default=False, name='show_names', description='show playlist')
bpy.types.WindowManager.playlist_names = []

def volume_up(self, context):
    try:
        context.window_manager.playsound.volume=context.window_manager.volume
    except:
        pass

def soundIsOn(context):
    try:
        while context.window_manager.playsound.status:
            time.sleep(0.001)
        if context.window_manager.index+1 < context.window_manager.playlist.__len__():
            context.window_manager.index += 1
            bpy.ops.sound.play()
        else:
            context.window_manager.index = 0
    except:
        pass

def playlistprint():
    pl = bpy.context.window_manager.playlist
    print ('Playlist: \n')
    for i, p in enumerate(pl):
        print (str(i+1)+ '.', p)
    return


class PlaySIC(bpy.types.Operator):
    '''Play a sound File'''
    bl_idname = "sound.play"
    bl_label = "Play sound"
    
    item_play = bpy.props.StringProperty(name="item", default='[False, 0]')
    
    @classmethod
    def poll(cls, context):
        try:
            if context.window_manager.playsound.status or not context.window_manager.playlist.__len__():
                return 0
            else:
                return 1
        except:
            if context.window_manager.playlist.__len__():
                return 1
            else:
                return 0

    def execute(self, context):
        check = eval(self.item_play)
        if check[0]:
            bpy.context.window_manager.index = check[1]
            check[0] = False
        bpy.types.WindowManager.f = aud.Factory(context.window_manager.playlist[context.window_manager.index])
        bpy.types.WindowManager.playsound = context.window_manager.d.play(context.window_manager.f)
        context.window_manager.pause=False
        context.window_manager.playsound.volume=context.window_manager.volume
        threading.Thread(target=soundIsOn, args=(context,)).start()
        #self.report({'INFO'}, "||| %s of %s ||| %s" % (str(context.window_manager.index+1), str(len(context.window_manager.playlist)), str(context.window_manager.playlist[context.window_manager.index])))
        
        if bpy.context.window_manager.playlist_names:
            pl = bpy.context.window_manager.playlist_names
        else:
            pl = bpy.context.window_manager.playlist
        print ("||| %s of %s ||| %s" % (str(context.window_manager.index+1), str(len(context.window_manager.playlist)), str(pl[context.window_manager.index])))
        return {'FINISHED'}


class ImportSIC(bpy.types.Operator):
    '''Load a sound File'''
    bl_idname = "sound.import"
    bl_label = "Import sound"

    filename_ext = ".mp3"
    filter_glob = StringProperty(default="*.mp3;*.ogg;*.wav;*.avi;*.mp4;*.wma", options={'HIDDEN'})
    filepath = StringProperty(subtype="FILE_PATH")
    filename = StringProperty()
    files = CollectionProperty(name="File Path",type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    
    def execute(self, context):
        print(self.filename)
        if self.files :
            for sfile in self.files:
                context.window_manager.playlist.append(self.directory + sfile.name)
                context.window_manager.playlist_names.append(sfile.name)
            playlistprint()
        else:
            context.window_manager.playlist.append(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ImportM3U(bpy.types.Operator, ImportHelper):
    '''Load a M3U File'''
    bl_idname = "sound.import_m3u"
    bl_label = "Import m3u"
    
    filename_ext = ".m3u"
    filter_glob = StringProperty(default="*.m3u;*.M3U", options={'HIDDEN'})
    
    def execute(self, context):
        f = open(self.filepath)
        for l in f :
            if not l[0]=='#':
                context.window_manager.playlist.append(l[0:-1])
        f.close()
        del f
        playlistprint()
        return {'FINISHED'}

class StopSIC(bpy.types.Operator):
    '''stop sound load'''
    bl_idname = "sound.stop"
    bl_label = "stop sound"

    @classmethod
    def poll(cls, context):
        try:
            return (context.window_manager.playsound.status)
        except:
            return 0

    def execute(self, context):
        
        context.window_manager.playsound.stop()
        context.window_manager.index = context.window_manager.playlist.__len__()
        
        return {'FINISHED'}

class DelList(bpy.types.Operator):
    '''Delet play list'''
    bl_idname = "sound.delplaylist"
    bl_label = "Del play list"

    @classmethod
    def poll(cls, context):
        return (context.window_manager.playlist.__len__())

    def execute(self, context):
        
        bpy.types.WindowManager.playlist=[]
        bpy.types.WindowManager.playlist_names=[]
        bpy.types.WindowManager.playlist_print=[]
        
        return {'FINISHED'}

class NextSIC(bpy.types.Operator):
    '''Next sound'''
    bl_idname = "sound.next"
    bl_label = "next sound"

    @classmethod
    def poll(cls, context):
        try:
            return (context.window_manager.playsound.status and context.window_manager.index+1 < context.window_manager.playlist.__len__())
        except:
            return 0

    def execute(self, context):
        
        context.window_manager.playsound.stop()
        
        return {'FINISHED'}

class PrevSIC(bpy.types.Operator):
    '''Previus sound load'''
    bl_idname = "sound.prev"
    bl_label = "previus sound"

    @classmethod
    def poll(cls, context):
        if context.window_manager.playlist.__len__():
            return (context.window_manager.index)
        else:
            return 0

    def execute(self, context):
        
        context.window_manager.index-=2
        context.window_manager.playsound.stop()
        
        return {'FINISHED'}

class PauseSIC(bpy.types.Operator):
    '''pause sound load'''
    bl_idname = "sound.pause"
    bl_label = "pause sound"

    @classmethod
    def poll(cls, context):
        try:
            return (context.window_manager.playsound.status)
        except:
            return 0

    def execute(self, context):
        
        context.window_manager.playsound.pause()
        context.window_manager.pause=True
        return {'FINISHED'}       
 
class ResumeSIC(bpy.types.Operator):
    '''resume sound load'''
    bl_idname = "sound.resume"
    bl_label = "resume sound"

    def execute(self, context):
        
        context.window_manager.playsound.resume()
        context.window_manager.pause=False
        return {'FINISHED'} 
    
class SetPosSIC(bpy.types.Operator):
    '''set position of song in seconds'''
    bl_idname = "sound.setpos"
    bl_label = "set position"

    def execute(self, context):
        context.window_manager.playsound.position = context.window_manager.MusHandle
        return {'FINISHED'} 
 
class PrintPlaylist(bpy.types.Operator):
    '''Print playlist'''
    bl_idname = "sound.printplaylist"
    bl_label = "print playlist"

    def execute(self, context):
        pl = context.window_manager.playlist
        print ('Playlist: \n')
        for i, p in enumerate(pl):
            print (str(i+1)+ '.', p)
        return {'FINISHED'} 


class VIEW3D_PT_Musicplayer(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Music Player"
    bl_category = 'NT'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=False)
        col2 = row.column(align=True)
        col2.operator("sound.import", text="Import sound", icon='FILE_SOUND')
        col2.operator("sound.prev", text="Previus", icon='REW')
        if context.window_manager.pause:
            col2.operator("sound.resume", text="Resume", icon='PLAY')
        else:
            col2.operator("sound.pause", text="Pause", icon='PAUSE')
        col2 = row.column(align=True)
        #col2.operator("sound.import_m3u", text="Import m3u", icon='ZOOMIN')
        col2.operator("sound.delplaylist", text="Clear play list", icon='X')
        col2.operator("sound.next", text="Next", icon='FF')
        col2.operator("sound.stop", text="Stop", icon='FULLSCREEN')
        col = layout.column(align=True)
        col.scale_y=2
        col.operator("sound.play", text="Play           ", icon='PLAY')
        row = col.row(align=True)
        row.scale_y=0.75
        row.prop(context.window_manager, "volume", slider=True)
        
        #col.operator("sound.printplaylist", text="Print playlist", icon='TEXT')
        row = col.row(align=True)
        row.scale_y=0.75
        row.prop(context.window_manager, 'MusHandle', slider=True, text='Position(sec)')
        row.operator('sound.setpos', text='Set Position')
        
        
        #col.prop(context.window_manager.f.limit)
        #plaingnow = context.window_manager.playlist[context.window_manager.index]
        #playitemgroup = re.match(r'(\w+)', plaingnow) # - need to be pattern for filename for linux/windows exception /\ in full path. So all after /\/ needed to be in group(1) matching
        #playitem = playitemgroup.group(1)
        row = layout.row(align=False)
        plaingindex = 'Song index: '+str(context.window_manager.index+1)+'/'+str(len(context.window_manager.playlist))
        row.label(text=plaingindex)
        row.prop(bpy.context.window_manager, 'show_names', text='show playlist')
        row = layout.row(align=False)
        row.label(text=bpy.context.window_manager.playlist_names[ context.window_manager.index])
        row.label(text = str(round(context.window_manager.playsound.position))+' seconds')
        
        if bpy.context.window_manager.playlist_names:
            playlist_print=context.window_manager.playlist_names
        else:
            playlist_print=context.window_manager.playlist
        if bpy.context.window_manager.show_names:
            box = layout.box()
            col = box.column(align=True)
            i=0
            for p in playlist_print:
                i+=1
                #col.operator('sound.play', bpy.context.window_manager.index=i-1, text=str(i)+' '+str(p))
                if i == (context.window_manager.index+1):
                    col.operator("sound.play", text='> '+str(i)+' | '+str(p)).item_play=str([True, i-1])
                else:
                    col.operator("sound.play", text=str(i)+' | '+str(p)).item_play=str([True, i-1])
        #a = context.window_manager
        #a.progress_begin(0,1)
        #a.progress_update(0.5)
        #a.progress_end()


# define classes for registration
classes = [PlaySIC,
            SetPosSIC,
            ImportSIC,
            ImportM3U,
            StopSIC,
            DelList,
            NextSIC,
            PrevSIC,
            PauseSIC,
            ResumeSIC,
            VIEW3D_PT_Musicplayer,
            PrintPlaylist]


# registering 
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.playlist=[]
    bpy.types.WindowManager.index=bpy.props.IntProperty()
    bpy.types.WindowManager.pause = bpy.props.BoolProperty(False)
    bpy.types.WindowManager.volume = bpy.props.FloatProperty(name="Volume",default=1.0, min=0.0, max=1.0, update=volume_up)
    bpy.types.WindowManager.d = aud.device()
    bpy.types.WindowManager.MusHandle = bpy.props.FloatProperty(name="MusHandle",default=0.0, min=0.0, max=300)


# unregistering 
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    try:
        del bpy.types.WindowManager.index
        del bpy.types.WindowManager.playlist
        del bpy.types.WindowManager.pause
        del bpy.types.WindowManager.volume
        del bpy.types.WindowManager.d
    except:
        pass
    try:
        del bpy.types.WindowManager.f
        del bpy.types.WindowManager.playsound
        del bpy.types.WindowManager.show_names
        del bpy.types.WindowManager.MusHandle
    except:
        pass

if __name__ == "__main__": 
    register()
    
