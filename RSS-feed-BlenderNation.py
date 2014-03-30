# nikitron.cc.ua ordered for this. Much thanks to Nikolay Fomichev https://vk.com/pythal
bl_info = {
    "name": "RSS",
    "version": (0, 1, 2),
    "blender": (2, 6, 9), 
    "category": "World",
    "author": "Nikolay Fomichev",
    "location": "World",
    "description": "makes RSS appears in world propertyes",
    "warning": "",
    "wiki_url": "",          
    "tracker_url": "",  
}

import bpy
import urllib.error as err
import urllib.request as req
from xml.etree import ElementTree as ET
import re

bpy.types.WindowManager.RSSadress = bpy.props.StringProperty(name='', default='http://feeds.feedburner.com/BlenderNation')

def getRss(adress):
    try:
        page = req.urlopen(adress).read().decode('utf8')
    except err.URLError:
        page = None
       
    tree = ET.XML(page) if page else None
    
    return tree    

class RssPanel(bpy.types.Panel):
    ''' Read feed '''
    bl_label = "RSS"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    
    
    #adress = bpy.context.window_manager.RSSadress[1]['default']
    tree = getRss(bpy.context.window_manager.RSSadress)
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_y=2
        row.prop(context.window_manager, "RSSadress")
        row.operator('world.reloadrss', text='Reload')
        width=100
        for i in context.screen.areas:
            if i.type == 'PROPERTIES':
                width = i.width
        if self.tree:  
            for el in self.tree.getchildren():
                for i in el.findall('item'):
                    box = layout.box()
                    title = i.find('title')
                    link = i.find('link')
                    description = i.find('description')
                    col = box.column()
                    col.scale_y=1.5
                    col.operator('wm.url_open', text=title.text).url = link.text
                    dtext_ = re.split('<br/>',description.text)[0]
                    dtext=''
                    for a in re.split('&#.....', dtext_):
                        dtext += a
                    labeltext = []
                    string = ''
                    k=0
                    for j in dtext:
                        if k == width//7:
                            k=0
                            labeltext.append(string)
                            string = ''
                        k+=1
                        string+=j
                    col = box.column()
                    col.scale_y=0.6
                    for t in labeltext:
                        col.label(t)
        else:
            layout.label('No connection to Internet!')

          
class reloadRSS(bpy.types.Operator):
    bl_label = "Reload operator"
    bl_idname = "world.reloadrss"
    bl_description = "Reload"
 
    def invoke(self, context, event):
        bpy.types.RssPanel.tree = getRss(context.window_manager.RSSadress)      
        return{"FINISHED"}
              
# registering and menu integration
def register():
    bpy.utils.register_class(RssPanel)
    bpy.utils.register_class(reloadRSS)
 
# unregistering and removing menus
def unregister():
    bpy.utils.unregister_class(RssPanel)
    bpy.utils.unregister_class(reloadRSS)
 
if __name__ == "__main__":
    register()
