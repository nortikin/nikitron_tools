# nikitron.cc.ua ordered for this. Much thanks to Nikolay Fomichev https://vk.com/pythal
bl_info = {
    "name": "join-screen",
    "version": (0, 2, 0),
    "blender": (2, 8, 0), 
    "category": "View3D > Tool Shelf > Music Player",
    "author": "nikitron",
    "location": "View3D > Tool Shelf > Music Player",
    "description": "makes RSS appears in world propertyes",
    "warning": "",
    "wiki_url": "",          
    "tracker_url": "",  
}


import bpy
from collections import Counter as coc


class OP_Area_do(bpy.types.Operator):
    '''Area do (join, split, options) for preparations of UI'''
    bl_idname = "screen.areado"
    bl_label = "area do (jso)"
    
    action=bpy.props.StringProperty(name='area_action')


    def get_mergables(self, areas,hw):
        'sorry for long text, will shorten asap \\\
        let it be for a while == True'
        xs,ys,ws,hs = {},{},{},{}
        for a in areas:
            #xs[a] = a.x
            #ys[a] = a.y
            ws[a] = a.width
            hs[a] = a.height
        print('heights',hs)
        #cxs = coc(list(xs.values()))
        #cys = coc(list(ys.values()))
        cws = coc(list(ws.values()))
        chs = coc(list(hs.values()))
        #print('Cheights',chs)
        couple = []
        if hw == 'h':
            for h in chs:
                print('height',chs[h],h)
                if chs[h] > 1:
                    for a in areas:
                        #print('equality',a.height, h)
                        if a.height == h:
                            couple.append(a)
                            #print('couple',couple)
                        if len(couple) == 2:
                            break
        elif hw == 'w':
            for w in cws:
                print('width',cws[w],w)
                if cws[w] > 1:
                    for a in areas:
                        #print('equality',a.width, w)
                        if a.width == w:
                            couple.append(a)
                            #print('couple',couple)
                        if len(couple) == 2:
                            break
        if len(couple) > 1 and hw == 'h':
            if couple[0].x > couple[1].x:
                b,a = couple[:2]
            else:
                a,b = couple[:2]
            return couple+[b.x-30,b.y,b.x+30,b.y+30]
        elif len(couple) > 1 and hw == 'w':
            if couple[0].y > couple[1].y:
                b,a = couple[:2]
            else:
                a,b = couple[:2]
            return couple+[b.x,b.y-30,b.x+30,b.y+30]
        return None,None,None,None,None,None

        #tx = area.x + area.width + 1

    def execute(self, context):
        context = bpy.context
        window = context.window
        areas = context.screen.areas 
        main = [i for i in areas if i.type == 'VIEW_3D'][0] # shit
        region = main.regions[4] # bullshit
        screen = context.screen
        direction = 'VERTICAL'
        factor = 0.3
        if self.action == 'join':
            # check height and width ping-pong till areas count rize 1
            hw = 'h'
            while True:
                #areas = context.screen.areas
                if len(areas) == 1:
                    break
                a,b,mix,miy,max,may = self.get_mergables(areas,hw)
                # C, CTX_wm_screen(C), sd->sarea, sd->narea
                if a and b: # sideli na trube
                    bpy.ops.screen.area_join(dict(region=a.regions[0],area=a,window=window,screen=screen,sarea=a,narea=b),min_x=mix, min_y=miy, max_x=max, max_y=may)
                    blend_data = context.blend_data
                    #bpy.ops.screen.screen_full_area(dict(screen=screen,window=window,region=region,area=context.area,blend_data=blend_data))
                    #bpy.ops.screen.back_to_previous(dict(screen=screen,window=window,region=region,area=context.area,blend_data=blend_data))
                    #print('joined and die')
                areas.update()
                # context.screen.update_tag(refresh=set({'DATA'})) # id ONLY
                if hw == 'h':
                    hw = 'w'
                else:
                    hw = 'h'
        elif self.action == 'split':
            bpy.ops.screen.area_split(dict(region=region,area=main,screen=screen,window=window),direction=direction,factor=factor)
        elif self.action == 'options':
            bpy.ops.screen.area_options(dict(region=region,area=main,screen=screen,window=window))
        # bpy.ops.screen.area_move(x=0, y=0, delta=10)
        # bpy.ops.screen.area_move(dict(region=region,area=main,screen=screen,window=window),direction="HORIZONTAL",delta=0.3)

        return {'FINISHED'} 


class VIEW3D_PT_area_do(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "area"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = 'SV'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator('screen.areado', text='join').action = 'join'
        col.operator('screen.areado', text='split').action = 'split'
        col.operator('screen.areado', text='options').action = 'options'

# registering 
def register():
    bpy.utils.register_class(OP_Area_do)
    bpy.utils.register_class(VIEW3D_PT_area_do)

# unregistering 
def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_area_do)
    bpy.utils.unregister_class(OP_Area_do)

if __name__ == "__main__":
    #unregister()
    register()