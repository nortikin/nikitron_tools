bl_info = {
    "name": "Radiola",
    "author": "nikitron",
    "version": (0, 9, 0),
    "blender": (3, 4, 0),
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

# import os
# import signal
# import time
# import subprocess as sp


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
                                    name=context.scene.rp_playlist[context.window_manager.radiola_ind].name, \
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
    bl_label = "Radiola"
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
        col.scale_y = 1.2
        colba = col.column(align=True)
        if context.window_manager.radiola_clear:
            b = colba.operator('sound.radiola',text='B U T T O N')
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
            col.label(text='Radio list taken from espradio.ru',icon='WORLD_DATA')
            col.label(text='{0} {1}'.format(str(i), str(p)))
            col.label(text='{0}'.format(str(sce.rp_playlist[i-1].url)))

        i = 0
        columnscount = wm.radiola_cols
        if columnscount == -2:
            col.prop(wm, 'radiola_cols',text='R E C O R D    S T U D I O')
            co = col.column(align=True)
            if wm.radiola_recing:
                co.alert=True
                a = co.operator("sound.radiola_record", text='Recording that radio', icon='RADIOBUT_ON', emboss=True)
            else:
                co.alert=False
                a = col.operator("sound.radiola_record", text='Record that radio', icon='REC', emboss=True)
            datafiles = os.path.join(bpy.utils.user_resource('DATAFILES', path='radiola', create=True))
            col.operator('wm.url_open', text='Listen for recordings', icon='WINDOW').url = datafiles
        elif columnscount == -1:
            col.prop(wm, 'radiola_cols',text='H E L P')
            box = col.box()
            row1 = box.row(align = True)
            col2 = row1.column(align=True)
            col2.label(text='        MENUes (by numbers):')
            col2.label(text='-2          Recording studio')
            col2.label(text='-1          Current help screen')
            col2.label(text=' 0          Playlist w/scrolling')
            col2.label(text=' 1...3    Long playlist w/names')
            col2.label(text=' 4...10  Long playlist w/o/names')
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
        elif columnscount==0: # and wm.radiola_ind:
            col.prop(wm, 'radiola_cols',text='P L A Y L I S T')
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
            col.prop(wm, 'radiola_shift', text='')
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
    bpy.types.WindowManager.radiola_cols =  bpy.props.IntProperty(min=-2,max=10,default=-1,description='N of columns')
    bpy.types.WindowManager.radiola_shift =  bpy.props.IntProperty(min=-600,max=600,default=0,description='Shift of list')
    bpy.types.WindowManager.radiola_url =   bpy.props.StringProperty(description='Current redio url')
    bpy.types.WindowManager.radiola_name =   bpy.props.StringProperty(description='Current redio name')
    bpy.types.WindowManager.radiola_recing =   bpy.props.BoolProperty(description='Recording now')
    bpy.types.WindowManager.radiola_dev =   aud.Device()
    
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
