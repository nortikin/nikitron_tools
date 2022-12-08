bl_info = {
    "name": "Radiola",
    "author": "nikitron.cc.ua",
    "version": (0, 1, 2),
    "blender": (3, 4, 0),
    "location": "View3D > Tool Shelf > SV > Radiola",
    "description": "Play the radio",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Misc"}

# import os
#import signal
import bpy
# import time
# import subprocess as sp
import aud
import json
import requests as rq



class OP_radiola(bpy.types.Operator):
    '''Radiola'''
    bl_idname = "sound.radiola"
    bl_label = "play radio"

    play : bpy.props.BoolProperty(name='play',default=True)
    stop : bpy.props.BoolProperty(name='stop',default=False)
    item_play : bpy.props.IntProperty(name='composition',default=0)

    def execute(self, context):

        if self.play:
            if self.stop:
                context.window_manager.radiola_dev.stopAll()
                context.window_manager.radiola_ind = -1
                return {'FINISHED'}
            if not len(context.scene.rp_playlist):
                self.dolist(urls,names)
            context.window_manager.radiola_clear = False
            context.window_manager.radiola_dev.stopAll()
            if context.window_manager.radiola_url:
                url = context.window_manager.radiola_url
            else:
                url = context.scene.rp_playlist[self.item_play].url
            try:
                context.window_manager.radiola_dev.play(aud.Sound(url))
                context.window_manager.radiola_ind = self.item_play
            except:
                self.report({'ERROR'}, f'Radiola cannot read source: {url}')
        elif self.stop:
            context.window_manager.radiola_dev.stopAll()
            #context.scene.rp_playlist.clear()
            context.window_manager.radiola_clear = True
        return {'FINISHED'}

    def dolist(self,urls,names):
        # dic={}
        jsons = 'https://espradio.ru/stream_list.json'
        gotten = rq.get(jsons).text.splitlines()
        jsonic = [json.loads(lines) for lines in gotten]
        for i in jsonic: #[:3772]: limit 3771 items in PropertyGroup
            bpy.context.scene.rp_playlist.add()
            bpy.context.scene.rp_playlist[-1].url = i['url']
            bpy.context.scene.rp_playlist[-1].name = i['name']
        #filetext = rq.get(jsons).text
        #with open('radios','w') as f:
        #    for line in filetext:
        #        f.write(line)


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
        col = layout.column(align=True)
        col.prop(context.window_manager, 'radiola_url')
        col = layout.column(align=True)
        col.scale_y = 1.2
        b = col.operator('sound.radiola',text='B U T T O N')
        if context.window_manager.radiola_clear:
            b.play = True
            b.stop = False
        else:
            b.play = False
            b.stop = True
            
        playlist_print = [a.name for a in context.scene.rp_playlist]
        i=0
        col = layout.column(align=True)
        col.scale_y = 0.8
        rurl = context.window_manager.radiola_url
        if rurl:
            col.label(text='Your URL is:',icon='WORLD_DATA')
            col.label(text=context.window_manager.radiola_url)
        else:
            col.label(text='List too large',icon='WORLD_DATA')
            col.label(text='limit is 3771 items')
            for p in playlist_print:
                i+=1
                if i == (context.window_manager.radiola_ind+1):
                    a = col.operator('sound.radiola', text='> '+str(i)+' | '+str(p))
                    a.item_play=i-1
                    a.play=True
                    a.stop=True
                else:
                    a = col.operator("sound.radiola", text='    '+str(i)+' | '+str(p))
                    a.item_play=i-1
                    a.play=True
                    a.stop=False

class RP_Playlist(bpy.types.PropertyGroup):
    url : bpy.props.StringProperty()
    name : bpy.props.StringProperty()

urls = [    'http://icecast.vgtrk.cdnvideo.ru/vestifm_mp3_192kbps',
            'http://strm112.1.fm/atr_mobile_mp3',
            'http://online.radiorecord.ru:8101/rr_320',
            'http://air.radiorecord.ru:8102/sd90_320',
            'http://strm112.1.fm/chilloutlounge_mobile_mp3',

            'http://185.53.169.128:8000/192',
            'http://sumerki.su:8000/Sumerki',
            'http://myradio.ua:8000/loungefm128.mp3',
            'http://81.30.54.74:8000/radio4',
            'http://radio.globaltranceinvasion.com:8000/radiohi',

            'http://icecast.vgtrk.cdnvideo.ru/mayakfm_mp3_192kbps',
            'http://nashe1.hostingradio.ru/nashe-128.mp3',
            'http://choco.hostingradio.ru:10010/fm', #http://pianosolo.streamguys.net:80/live
            'http://sc1c-sjc.1.fm:7070/?type=.flv',
            'http://source.dnbradio.com:10128/128k.mp3',

            'http://sc3b-sjc.1.fm:7802/?type=.flv',
            'http://audio2.video.ria.ru:80/voicerus',
            'http://media.govoritmoskva.ru:8880/ru64.mp3',
    ]
names = [   'Вести',       
            'Амстердам транс',
            'Рекорд электроника', 
            '90-е гг',
            '1фм лаунж',  

            'Атмосфера ланж', 
            'Сумерьки',    
            'ЛанжФМ', 
            'Дача',
            'Транс',       

            'Маяк', 
            'Наше радио', 
            'Шакалад', 
            'Классика',    
            'ДНБ',

            'Кантри',      
            'Спутник',
            'Говорит Москва',
    ]

#def dolist(urls,names):
#    for u,n in zip(urls,names):
#        bpy.context.scene.rp_playlist.add()
#        bpy.context.scene.rp_playlist[-1].url = u
#        bpy.context.scene.rp_playlist[-1].name = n

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
    bpy.types.WindowManager.radiola_url =   bpy.props.StringProperty()
    bpy.types.WindowManager.radiola_dev =   aud.Device()
    bpy.utils.register_class(OP_radiola)
    bpy.utils.register_class(OBJECT_PT_radiola_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_radiola_panel)
    bpy.utils.unregister_class(OP_radiola)
    del bpy.types.WindowManager.radiola_ind
    del bpy.types.WindowManager.radiola
    del bpy.types.WindowManager.radiola_clear
    del bpy.types.Scene.rp_playlist


if __name__ == '__main__':
    register()
