bl_info = {
    "name": "Radiola",
    "author": "nikitron",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Tool Shelf > SV > Radiola",
    "description": "Playing the radio (also files) using aud blender lib",
    "warning": "There are 18+ stations, be carefull",
    "wiki_url": "https://github.com/nortikin/nikitron_tools/wiki",
    "tracker_url": "https://github.com/nortikin/nikitron_tools/issues",
    "category": "Misc"}

import bpy
import aud
import json
import requests as rq
import pathlib
import os
from threading import Thread, Event#, Queue
import time
# icons
from bpy.utils import previews
import addon_utils #noqa
from PIL import Image
from io import BytesIO
import base64
# end icons


# import os
# import signal
# import time
# import subprocess as sp


icon_image = "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"

def get_image_path():
    datafiles = os.path.join(bpy.utils.user_resource('DATAFILES', path='radiola', create=True))
    path = os.path.join(datafiles,"radiola.png")
    if os.path.exists(path):
        return path
    im = Image.open(BytesIO(base64.urlsafe_b64decode(icon_image)))
    im.save(path)
    return path

plugin_icons = previews.new()

plugin_icons.load(
    name='radiola.png',
    path=get_image_path(),
    path_type='IMAGE'
)

def volume_up(self, context):
    try:
        context.window_manager.radiola_dev.volume = context.window_manager.radiola_volume
    except:
        pass

class DownloadThread(Thread):
    """
    Пример многопоточной загрузки файлов из интернета
    """

    def __init__(self, context, url, name, event):
        """Инициализация потока"""
        Thread.__init__(self)
        self.context = context
        self.url = url
        self.name = name
        self.event = event

    def run(self):
        """Запуск потока"""
        r = rq.get(self.url, stream=True)
        datafiles = os.path.join(bpy.utils.user_resource('DATAFILES', path='radiola', create=True))
        tm = time.localtime() # tm_year=2023, tm_mon=1, tm_mday=8, tm_hour=21, tm_min=47, tm_sec=38
        date = '.'.join([str(tm.tm_year),str(tm.tm_mon),str(tm.tm_mday),'.',str(tm.tm_hour),str(tm.tm_min),str(tm.tm_sec)])
        with open(os.path.join(datafiles,date+'_'+self.name+'.mp3'), 'wb') as f:
            try:
                for block in r.iter_content(1024):
                    f.write(block)
                    if self.context.window_manager.radiola_recing == False:
                        print('RADIOLA finished downloading')
                        break
            except KeyboardInterrupt:
                pass

        msg = "RADIOLA downloading: %s %s!" % (self.name, self.url)
        print(msg)


class OP_radiola_record(bpy.types.Operator):
    '''Radiola record'''
    bl_idname = "sound.radiola_record"
    bl_label = "record radio"

    def execute(self, context):
        if context.scene.rp_playlist[context.window_manager.radiola_ind].url:
            if not context.window_manager.radiola_recing:
                event = Event() # нахрен оказалось не надо
                context.window_manager.radiola_recing = True
                #queue = Queue()
                Download = DownloadThread(context=context, \
                                    url=context.scene.rp_playlist[context.window_manager.radiola_ind].url,\
                                    name=context.scene.rp_playlist[context.window_manager.radiola_ind].name.replace('/',''), \
                                    event=event)
                Download.start()
                print(f'RADIOLA: downloading {Download}')
            else:
                context.window_manager.radiola_recing = False
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'RADIOLA: There is no url')
            return {'FINISHED'}


class OP_radiola(bpy.types.Operator):
    '''Radiola play'''
    bl_idname = "sound.radiola"
    bl_label = "play radio"

    play : bpy.props.BoolProperty(name='play',default=True)
    stop : bpy.props.BoolProperty(name='stop',default=False)
    shift : bpy.props.BoolProperty(name='shift',default=False)
    item_play : bpy.props.IntProperty(name='composition',default=0)

    def execute(self, context):
        if context.scene.rp_playlist:
            context.window_manager.radiola_url = ''
            context.window_manager.radiola_name = ''
        if self.play:
            if self.stop:
                context.window_manager.radiola_dev.stopAll()
                context.window_manager.radiola_ind = -1
                return {'FINISHED'}
            context.window_manager.radiola_clear = False
            context.window_manager.radiola_dev.stopAll()
            if not len(context.scene.rp_playlist):
                self.dolist()
                return {'FINISHED'}
            if context.window_manager.radiola_url:
                url = context.window_manager.radiola_url
            else:
                url = context.scene.rp_playlist[self.item_play].url
            try:
                context.window_manager.radiola_dev.play(aud.Sound(url))
                context.window_manager.radiola_ind = self.item_play
                print('RADIOLA:',self.item_play)
                print('RADIOLA:',url)
                print('RADIOLA:',context.scene.rp_playlist[self.item_play].name)
                if self.shift:
                    context.window_manager.radiola_shift = 0
            except:
                self.report({'ERROR'}, f'RADIOLA cannot read source: {url}')
        elif self.stop:
            context.window_manager.radiola_dev.stopAll()
            context.window_manager.radiola_clear = True
        return {'FINISHED'}

    def dolist(self):
        '''
        проверка файла в настрйоках
        если файл есть, прост очитаем его
        если нет файла, то грузим из Сети и сохраняем
        '''

        datafiles = os.path.join(bpy.utils.user_resource('DATAFILES', path='radiola', create=True))
        contains = os.listdir(datafiles)
        if 'stations' in contains:
            print('RADIOLA: file already there')
            stations = os.path.join(datafiles, 'stations')
            with open(stations,'r') as fw:
                gotten = fw.read().splitlines()
                jsonic = [json.loads(lines) for lines in gotten]
            print('RADIOLA: file aten')
        else:
            stations = os.path.join(datafiles, 'stations')
            #jsons = 'https://espradio.ru/stream_list.json'
            jsons = 'https://raw.githubusercontent.com/nortikin/nikitron_tools/master/blender_3/stations'
            gottenfile = rq.get(jsons)
            gotten = gottenfile.text.splitlines()
            print('RADIOLA: Downloaded file')
            jsonic = [json.loads(lines) for lines in gotten]
            with open(stations,'wb') as fw:
                fw.write(gottenfile.content)
            print('RADIOLA: locally placed')

        for k,i in enumerate(jsonic):
            bpy.context.scene.rp_playlist.add()
            bpy.context.scene.rp_playlist[-1].ind = k
            bpy.context.scene.rp_playlist[-1].url = i["url"]
            bpy.context.scene.rp_playlist[-1].name = i["name"]



class OBJECT_PT_radiola_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_idname = 'OBJECT_PT_radiola_panel'
    bl_label = f"Radiola_{bl_info['version']}"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = 'SV'


    def draw(self, context):
        ''' \
        Radiola \
        '''
        layout = self.layout
        sce = context.scene
        wm = context.window_manager
        rurl = wm.radiola_url
        rname = wm.radiola_name

        def getname(col,rurl):
            f = rq.get(rurl)
            for i, line in enumerate(f.text.splitlines()):
                if line.startswith('icy-name') or i > 20: break
                if i > 20: print('failed to find station name')
                else:
                    out = 'composition', line.replace('icy-name:', '')
                    col.label(text='Radio list taken from espradio.ru',icon='WORLD_DATA')

        col = layout.column(align=True)
        #col.prop(context.window_manager, 'rurl')
        col.prop_search(wm, "radiola_name", sce, "rp_playlist")
        col = layout.column(align=True)
        col.scale_y = 1#2.2
        colba = col.column(align=True)
        colba.scale_y = 2.2
        
        if context.window_manager.radiola_clear:
            b = colba.operator('sound.radiola',text='B U T T O N') # ,icon_value=plugin_icons['radiola.png'].icon_id, emboss=True) 
            b.play = True
            b.stop = False
        elif rname:
            #print('RADIOLA url:',rname,sce.rp_playlist[rname].url)
            b = colba.operator('sound.radiola',text='B U T T O N')
            rurl = sce.rp_playlist[rname].url
            b.item_play = sce.rp_playlist[rname].ind
            if sce.rp_playlist[rname].ind == (wm.radiola_ind+1):
                b.play = False
                b.stop = True
            else:
                b.play = True
                b.stop = False
        else:
            colba.alert = True
            b = colba.operator('sound.radiola',text='B U T T O N')
            b.play = False
            b.stop = True

        playlist_print = [a.name for a in sce.rp_playlist]
        i=0
        col = layout.column(align=True)
        col.scale_y = 0.8
        col.ui_units_x = 100
        i = wm.radiola_ind+1
        if playlist_print:
            p = playlist_print[wm.radiola_ind]
            plength = len(playlist_print)
            coldescr = col.column_flow(columns=2, align=True)
            coldescr.prop(wm, "radiola_volume", slider=True)
            coldescr.label(text='Radio list taken from espradio.ru',icon='WORLD_DATA')
            coldescr.label(text='{0} {1}'.format(str(i), str(p)))
            coldescr.label(text='{0}'.format(str(sce.rp_playlist[i-1].url)))

        i = 0
        columnscount = wm.radiola_cols
        if columnscount == -1:
            col5 = col.column(align=True)
            col5.scale_y = 2.0
            col5.prop(wm, 'radiola_cols',text='R E C O R D    S T U D I O')
            co = col.column(align=True)
            if wm.radiola_recing:
                co.alert=True
                a = co.operator("sound.radiola_record", text='Recording that radio', icon='RADIOBUT_ON', emboss=True)
            else:
                co.alert=False
                a = col.operator("sound.radiola_record", text='Record that radio', icon='REC', emboss=True)
            datafiles = os.path.join(bpy.utils.user_resource('DATAFILES', path='radiola', create=True))
            col.operator('wm.url_open', text='Listen for recordings', icon='WINDOW').url = datafiles
            col.template_icon(icon_value=plugin_icons['radiola.png'].icon_id, scale=10.0)
        elif columnscount == 0:
            col6 = col.column(align=True)
            col6.scale_y = 2.0
            col6.prop(wm, 'radiola_cols',text='H E L P')
            box = col.box()
            row1 = box.row(align = True)
            col2 = row1.column(align=True)
            col2.label(text='        MENUes (by numbers):')
            col2.label(text='-2          Recording studio')
            col2.label(text='-1          Current help screen')
            col2.label(text=' 0          Playlist w/scrolling')
            col2.label(text='')# 1...3    Long playlist w/names')
            col2.label(text='')# 4...10  Long playlist w/o/names')
            col2.label(text='')
            col2.label(text='        Try Sverchok node addon:')
            col2.operator('wm.url_open', text='GET Sverchok', icon='URL').url =\
                        'https://github.com/nortikin/sverchok'
            col2.label(text='        Try other misc addons:')
            col2.operator('wm.url_open', text='GET miscellaneous addons', icon='VIEW_PAN').url =\
                        'https://github.com/nortikin/nikitron_tools'
            col3 = row1.column(align=True)
            col3.label(text='        B U T T O N')
            col3.label(text=' 1. Initially stops all songs.')
            col3.label(text=' 2. Than downloads playlist from github')
            col3.label(text=' 3. Next time at start it loads local playlist')
            col3.label(text=' 4. Play current url')
            col3.label(text=' 5. Stop playback')
            col3.label(text='')
            col3.label(text=' Support:')
            col3.operator('wm.url_open', text='GET Support', icon='QUESTION').url =\
                        'https://t.me/sverchok_3d'
            col3.label(text=' Also we have Music player, RSSreader')
            col3.label(text=' Toolset for volume, materials scv etc.')
            box.label(text='* - To add favorites use Q menu (RMB on quiet radio - add to Q)')
            box.label(text='       To call back stations - simply Q on view area!')
            box.label(text='')
        elif columnscount==1: # and wm.radiola_ind:
            col7 = col.column(align=True)
            col7.scale_y = 2.0
            col7.prop(wm, 'radiola_cols',text='P L A Y L I S T')
            col1 = col.column_flow(columns=3, align=True)
            wm.radiola_shift = max(wm.radiola_shift, -int(wm.radiola_ind/14))
            wm.radiola_shift = min(wm.radiola_shift, int((plength-wm.radiola_ind)/14))
            ran = range(max(wm.radiola_ind-19+ \
                    wm.radiola_shift*14,0), \
                    min(wm.radiola_ind+23+ \
                    wm.radiola_shift*14,plength),1)
            for i in ran:
                p = playlist_print[i]
                if i == (wm.radiola_ind):
                    col1.alert = True
                    a = col1.operator('sound.radiola', text='> '+str(i+1)+' | '+str(p), emboss=False)
                    a.item_play=i
                    a.play=True
                    a.stop=True
                else:
                    col1.alert = False
                    a = col1.operator("sound.radiola", text='    '+str(i+1)+' | '+str(p), emboss=False)
                    a.item_play=i
                    a.play=True
                    a.stop=False
                    a.shift=True
            col4 = col.column(align=True)
            col4.scale_y = 2.0
            col4.prop(wm, 'radiola_shift', text='')
        """
        else:
            col.prop(wm, 'radiola_cols',text='P L A Y L I S T    U G L Y')
            col1 = col.column_flow(columns=columnscount, align=True)
            for p in playlist_print:
                i+=1
                if i == (wm.radiola_ind+1):
                    col1.alert = True
                    if columnscount<11:
                        a = col1.operator('sound.radiola', text='> '+str(i)+' | '+str(p), emboss=False)
                    else:
                        a = col1.operator('sound.radiola', text='> '+str(i), emboss=False)
                    a.item_play=i-1
                    a.play=True
                    a.stop=True
                else:
                    col1.alert = False
                    if columnscount<4:
                        a = col1.operator("sound.radiola", text='    '+str(i)+' | '+str(p), emboss=False)
                    else:
                        a = col1.operator("sound.radiola", text='    '+str(i), emboss=False)
                    a.item_play=i-1
                    a.play=True
                    a.stop=False
        """



class RP_Playlist(bpy.types.PropertyGroup):
    ind : bpy.props.IntProperty()
    url : bpy.props.StringProperty()
    name : bpy.props.StringProperty()


def register():
    try:
        if 'rp_playlist' in bpy.context.scene:
            bpy.context.scene.rp_playlist.clear()
    except:
        pass
    bpy.utils.register_class(RP_Playlist)
    bpy.types.Scene.rp_playlist =           bpy.props.CollectionProperty(type=RP_Playlist)
    bpy.types.WindowManager.radiola_clear = bpy.props.BoolProperty(default=False,description='Flag that means clear playback')
    bpy.types.WindowManager.radiola =       bpy.props.IntProperty(description='player')
    bpy.types.WindowManager.radiola_ind =   bpy.props.IntProperty(description='Current radio index')
    bpy.types.WindowManager.radiola_cols =  bpy.props.IntProperty(min=-1,max=1,default=0,description='N of columns')
    bpy.types.WindowManager.radiola_shift =  bpy.props.IntProperty(min=-600,max=600,default=0,description='Shift of list')
    bpy.types.WindowManager.radiola_url =   bpy.props.StringProperty(description='Current redio url')
    bpy.types.WindowManager.radiola_name =   bpy.props.StringProperty(description='Current redio name')
    bpy.types.WindowManager.radiola_recing =   bpy.props.BoolProperty(description='Recording now')
    bpy.types.WindowManager.radiola_dev =   aud.Device()
    bpy.types.WindowManager.radiola_volume =  bpy.props.FloatProperty(min=0.0,max=1.0,default=1.0,description='volume',update=volume_up)
    
    bpy.utils.register_class(OP_radiola)
    bpy.utils.register_class(OP_radiola_record)
    bpy.utils.register_class(OBJECT_PT_radiola_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_radiola_panel)
    bpy.utils.unregister_class(OP_radiola_record)
    bpy.utils.unregister_class(OP_radiola)
    del bpy.types.WindowManager.radiola_ind
    del bpy.types.WindowManager.radiola
    del bpy.types.WindowManager.radiola_clear
    del bpy.types.WindowManager.radiola_cols
    del bpy.types.WindowManager.radiola_shift
    del bpy.types.WindowManager.radiola_dev
    del bpy.types.WindowManager.radiola_url
    del bpy.types.WindowManager.radiola_name
    del bpy.types.WindowManager.radiola_recing
    del bpy.types.Scene.rp_playlist


if __name__ == '__main__':
    register()
