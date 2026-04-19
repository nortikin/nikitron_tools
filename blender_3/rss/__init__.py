import bpy
import urllib.request as req
import urllib.error as err
from xml.etree import ElementTree as ET
import ssl
import re
from threading import Thread
import time
import pprint

bl_info = {
    "name": "RSS Reader Pro",
    "version": (0, 9, 0),
    "blender": (4, 2, 0),
    "category": "World",
    "author": "Nikolay Fomichev (enhanced with Nikitron & deepseek)",
    "location": "World",
    "description": "RSS reader with preset feeds and custom URL",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
}

# Предустановленные RSS-ленты
PRESET_FEEDS = [
    ("http://feeds.feedburner.com/BlenderNation", "Blender Nation", "Официальный блог Blender"),
    ("https://rsshub.app/telegram/channel/sverchok3d", "Sverchok", "Официальный сайт Sverchok addon"),
    ("custom", "Custom URL", "Введите свой RSS-адрес")
]

# Глобальный кеш для хранения данных
rss_cache = {
    'data': None,
    'loading': False,
    'error': None,
    'timestamp': 0
}

def update_rss_url(self, context):
    """Обновляет URL при выборе пресета"""
    if context.window_manager.RSSpreset:  # Если выбран не Custom URL
        context.window_manager.RSSadress = context.window_manager.RSSpreset

# Регистрируем свойства
bpy.types.WindowManager.RSSadress = bpy.props.StringProperty(
    name="RSS URL",
    description="Enter RSS feed URL",
    default=PRESET_FEEDS[1][0],
    update=update_rss_url
)

bpy.types.WindowManager.RSSpreset = bpy.props.EnumProperty(
    name="Preset Feeds",
    description="Select from preset RSS feeds",
    items=PRESET_FEEDS,
    default=PRESET_FEEDS[1][0]
)


bpy.types.WindowManager.RSSpreset_updater = bpy.props.BoolProperty(
    name="RSS Preset Updater",
    description="Internal property to handle preset updates",
    update=update_rss_url
)

def fetch_rss(url):
    global rss_cache
    
    if not url or not url.startswith(('http://', 'https://')):
        rss_cache['error'] = "Invalid URL format" if url else "URL is empty"
        return
        
    rss_cache['loading'] = True
    rss_cache['error'] = None
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        headers = {
            'User-Agent': 'BlenderRSSReader/1.0',
            'Accept': 'application/xml, text/xml, */*'
        }
        
        request = req.Request(url, headers=headers)
        
        with req.urlopen(request, context=ctx, timeout=15) as response:
            content = response.read().decode('utf-8')
            
            if content.startswith('\ufeff'):
                content = content[1:]
                
            try:
                rss_cache['data'] = ET.fromstring(content)
                rss_cache['error'] = None
            except ET.ParseError as e:
                rss_cache['error'] = f"XML parse error: {str(e)}"
                
    except err.HTTPError as e:
        rss_cache['error'] = f"HTTP Error {e.code}: {e.reason}"
    except err.URLError as e:
        rss_cache['error'] = f"URL Error: {e.reason}"
    except Exception as e:
        rss_cache['error'] = f"Error: {str(e)}"
    finally:
        rss_cache['loading'] = False
        rss_cache['timestamp'] = time.time()

def load_rss_in_thread(url):
    if rss_cache['loading']:
        return
        
    thread = Thread(target=fetch_rss, args=(url,))
    thread.daemon = True
    thread.start()

class RSS_PT_Panel(bpy.types.Panel):
    bl_label = "RSS Reader"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        width1=100
        for i in context.screen.areas:
            if i.type == 'PROPERTIES':
                width1 = (i.width-70)//5.5
        layout = self.layout
        wm = context.window_manager
        
        # Выбор пресета
        row = layout.row()
        row.prop(wm, "RSSpreset", text="Preset")
        
        # Поле для ручного ввода URL (только если выбран Custom URL)
        if wm.RSSpreset == "custom":
            row = layout.row()
            row.prop(wm, "RSSadress", text="Custom URL")
        
        # Кнопка обновления
        row = layout.row()
        row.operator('world.rss_reload', text="Reload", icon='FILE_REFRESH')
        
        # Проверяем, нужно ли загружать данные
        current_url = wm.RSSadress
        if not rss_cache['loading'] and (rss_cache['data'] is None or time.time() - rss_cache['timestamp'] > 300):
            load_rss_in_thread(current_url)
        
        # Статус загрузки
        if rss_cache['loading']:
            layout.label(text="Loading feed...", icon='SORTTIME')
            return
            
        # Ошибки
        if rss_cache['error']:
            layout.label(text=rss_cache['error'], icon='ERROR')
            return
            
        # Данные
        if rss_cache['data'] is None:
            layout.label(text="No data available", icon='INFO')
            return
            
        # Отображение RSS
        channel = rss_cache['data'].find('channel')
        if channel is None:
            channel = rss_cache['data']
            
        for item in channel.findall('item'):
            box = layout.box()
            title = item.find('title')
            link = item.find('link')
            desc = item.find('description')
            
            # Заголовок
            if title is not None and title.text:
                row = box.row()
                if link is not None and link.text:
                    row.operator('wm.url_open', text=title.text).url = link.text
                else:
                    row.label(text=title.text)
            
            # Описание
            if desc is not None and desc.text:
                #print(desc.text)
                clean_text = pprint.pformat(re.sub('<[^<]+?>', '', desc.text), width=width1)
                #clean_text = re.sub('<[^<]+?>', '', desc.text)
                clean_text = clean_text.strip()
                if clean_text:
                    # Разбиваем текст на строки
                    lines = clean_text.splitlines() # splitlines() # split('\n')
                    for line in lines:
                        if line.strip()[1:-1]:
                            col = box.column()
                            col.scale_y=0.4
                            col.label(text=line.strip()[1:-1].replace('\n',''))

class RSS_Reload_Operator(bpy.types.Operator):
    bl_idname = "world.rss_reload"
    bl_label = "Reload RSS"
    bl_description = "Reload the current RSS feed"

    def execute(self, context):
        if context.window_manager.RSSpreset:  # Если выбран не Custom URL
            context.window_manager.RSSadress = context.window_manager.RSSpreset
        
        load_rss_in_thread(context.window_manager.RSSadress)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RSS_PT_Panel)
    bpy.utils.register_class(RSS_Reload_Operator)

def unregister():
    bpy.utils.unregister_class(RSS_PT_Panel)
    bpy.utils.unregister_class(RSS_Reload_Operator)

if __name__ == "__main__":
    register()