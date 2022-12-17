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
# import os
# import signal
# import time
# import subprocess as sp



class OP_radiola(bpy.types.Operator):
    '''Radiola'''
    bl_idname = "sound.radiola"
    bl_label = "play radio"

    play : bpy.props.BoolProperty(name='play',default=True)
    stop : bpy.props.BoolProperty(name='stop',default=False)
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
                print('Radiols:',self.item_play)
                print('Radiols:',url)
                print('Radiols:',context.scene.rp_playlist[self.item_play].name)
            except:
                self.report({'ERROR'}, f'Radiola cannot read source: {url}')
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
            jsons = 'https://raw.githubusercontent.com/nortikin/nikitron_tools/master/blender_2.82/stations'
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
        rurl = context.window_manager.radiola_url
        rname = context.window_manager.radiola_name

        col = layout.column(align=True)
        #col.prop(context.window_manager, 'radiola_url')
        col.prop_search(wm, "radiola_name", sce, "rp_playlist")
        col = layout.column(align=True)
        col.scale_y = 1.2
        colba = col.column(align=True)
        if context.window_manager.radiola_clear:
            b = colba.operator('sound.radiola',text='B U T T O N')
            b.play = True
            b.stop = False
        elif rname:
            #print('RADIOLA url:',rname,context.scene.rp_playlist[rname].url)
            b = colba.operator('sound.radiola',text='B U T T O N')
            context.window_manager.radiola_url = context.scene.rp_playlist[rname].url
            b.item_play = context.scene.rp_playlist[rname].ind
            if context.scene.rp_playlist[rname].ind == (context.window_manager.radiola_ind+1):
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

        playlist_print = [a.name for a in context.scene.rp_playlist]
        i=0
        col = layout.column(align=True)
        col.scale_y = 0.8
        col.ui_units_x = 100
        i = context.window_manager.radiola_ind+1
        p = playlist_print[context.window_manager.radiola_ind]
        #if rurl:
        #    col.label(text='Your URL is:{0}'.format(rurl),icon='WORLD_DATA')
        #    col.label(text=context.window_manager.radiola_url)
        #if rname:
        #    print('RADIOLA url:',rname,context.scene.rp_playlist[rname].url)
        #    context.window_manager.radiola_url = context.scene.rp_playlist[rname].url
        #else:
        col.label(text='Radio list taken from espradio.ru',icon='WORLD_DATA')
        col.label(text='{0} {1}'.format(str(i), str(p)))
        col.label(text='{0}'.format(str(context.scene.rp_playlist[i-1].url)))
        col.prop(context.window_manager, 'radiola_cols',text='Columns count')
        i = 0
        columnscount = context.window_manager.radiola_cols
        col1 = col.column_flow(columns=columnscount, align=True)
        for p in playlist_print:
            i+=1
            if i == (context.window_manager.radiola_ind+1):
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
    bpy.types.WindowManager.radiola_clear = bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.radiola =       bpy.props.IntProperty()
    bpy.types.WindowManager.radiola_ind =   bpy.props.IntProperty()
    bpy.types.WindowManager.radiola_cols =  bpy.props.IntProperty(min=1,max=10,default=1,description='N of columns')
    bpy.types.WindowManager.radiola_url =   bpy.props.StringProperty()
    bpy.types.WindowManager.radiola_name =   bpy.props.StringProperty()
    bpy.types.WindowManager.radiola_dev =   aud.Device()
    
    bpy.utils.register_class(OP_radiola)
    bpy.utils.register_class(OBJECT_PT_radiola_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_radiola_panel)
    bpy.utils.unregister_class(OP_radiola)
    del bpy.types.WindowManager.radiola_ind
    del bpy.types.WindowManager.radiola
    del bpy.types.WindowManager.radiola_clear
    del bpy.types.WindowManager.radiola_cols
    del bpy.types.WindowManager.radiola_dev
    del bpy.types.WindowManager.radiola_url
    del bpy.types.WindowManager.radiola_name
    del bpy.types.Scene.rp_playlist


if __name__ == '__main__':
    register()
