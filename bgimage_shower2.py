# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Camera backgrounder",
    "version": (0, 2, 0),
    "blender": (2, 7, 9),  
    "category": "Camera",
    "author": "Nikita Gorodetskiy",
    "location": "object",
    "description": "camera background changer",
    "warning": "not works for earlier versions",
    "wiki_url": "",          
    "tracker_url": "https://vk.com/sverchok_b3d",  
}



import bpy
from bpy.props import StringProperty, CollectionProperty, \
                        BoolProperty, PointerProperty, \
                        IntProperty


class SvBgImage(bpy.types.PropertyGroup):
    object = PointerProperty(type=bpy.types.Object, name='object')
    image = PointerProperty(type=bpy.types.Image, name='image')
    opened = BoolProperty(name='opened',default=True)



class OP_SV_bgimage_remove(bpy.types.Operator):
    bl_idname = 'image.sv_bgimage_remove'
    bl_label = "remover of bgimages"
    bl_description = "remove bgimages"
    bl_options = {'REGISTER'}


    def execute(self, context):
        a = context.space_data.background_images
        obs = bpy.data.cameras
        for i in a:
            if i.image:
                i.image.user_clear()
            a.remove(i)
        for o in obs:
            bpy.data.objects[o.name].bgimage = ''
        self.report({'INFO'}, 'cleared all backgrounds')
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)



class OP_SV_bgimage_remove_unused(bpy.types.Operator):
    bl_idname = 'image.sv_bgimage_remove_unused'
    bl_label = "remover of unused bgimages"
    bl_description = "remove unused bgimages"
    bl_options = {'REGISTER'}


    def execute(self, context):
        a = context.space_data.background_images
        obs = bpy.data.cameras
        obj = bpy.data.objects
        used = []
        for i in a:
            for o in obs:
                if i.image.name == obj[o.name].bgimage:
                    used.append(i.image.name)
        for i in a:
            if i.image.name not in used:
                bpy.data.images[i.image.name].user_clear()
                a.remove(i)

        self.report({'INFO'}, 'cleared unused backgrounds')
        return {'FINISHED'}



class OP_SV_bgimage_new_slot(bpy.types.Operator):
    bl_idname = 'object.sv_bgimage_new_slot'
    bl_label = "new slot"
    bl_description = "new slot"
    bl_options = {'REGISTER'}


    def execute(self, context):
        obj = context.object
        bpy.ops.view3d.object_as_camera()
        
        bgimages = context.space_data.background_images
        context.scene.bgobjects.add()
        context.scene.bgobjects[-1].object = obj
        #context.scene.bgobjects[-1].image
        bgi = bgimages.new()
        bgi.image = context.scene.bgobjects[-1].image
        '''if bgim:
            for bgi in bgimages:
                if bgi.image.name == bgim:
                    #print(bgi.image.name, bgim)
                    bgi.show_background_image = True
                else:
                    bgi.show_background_image = False
        else:
            for bgi in bgimages:
                print('noimage',bgi.show_background_image)
                bgi.show_background_image = False'''

        return {'FINISHED'}



class OP_SV_bgimage_setcamera(bpy.types.Operator):
    '''Set camera active bg'''
    bl_idname = "image.sv_bgimage_set_camera"
    bl_label = "Open image"
    bl_description = "activate gbimage"
    bl_options = {'REGISTER'}

    item = IntProperty(name='item')


    def execute(self, context):
        bgimages = context.space_data.background_images
        bgobjects = context.scene.bgobjects
        item= self.item
        bgobject = bgobjects[item]
        im = False
        for bgi in bgimages:
            print(bgi.image.name)
            if bgi.image.name == bgobject.image.name:
                print('image %s switched, not created + %s' % (bgobject.image.name, bgi.image.name))
                bgi.show_background_image = True
                im = True
                context.scene.camera = bgobject.object
            else:
                bgi.show_background_image = False
        if not im:
            print('image %s not switched, created' % (bgobject.image.name))
            newbgimage = bgimages.new()
            print(bgobject.image)
            context.scene.camera = bgobject.object
            newbgimage.image = bgobject.image
        return {'FINISHED'}



class OP_SV_bgimage_rem_bgimage(bpy.types.Operator):
    '''Removes background object with linked image for camera'''
    bl_idname = "image.sv_bgimage_rem_bgimage"
    bl_label = "Rem bgimage"
    bl_description = "Remove background image"
    bl_options = {'REGISTER'}

    item = IntProperty(name='item')


    def execute(self, context):
        bgimages = context.space_data.background_images
        bgobjects = context.scene.bgobjects
        item = self.item
        bgobject = bgobjects[item]
        im = False
        for bgi in bgimages:
            if bgi.image.name == bgobject.image.name:
                print('image %s for object %s was removed' % (bgobject.image.name, bgobject.object.name))
                bgimages.remove(bgi)
                bgobjects.remove(item)
                im = True
        if not im:
            print('impossible thing - we canot remove item under index', str(item))
            bpy.ops.image.sv_bgimage_set_camera(item=item)
        return {'FINISHED'}



class VIEW3D_PT_camera_bgimages2(bpy.types.Panel):
    bl_label = "Backgrounds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'



    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        
        main = context.scene
        row = col.row(align=True)
        if main.bgimage_panel:
            row.prop(main, 'bgimage_panel', text="Be carefull", icon='DOWNARROW_HLT')
        else:
            row.prop(main, 'bgimage_panel', text="Basics", icon='RIGHTARROW')
        if main.bgimage_panel:
            row = col.row(align=True)
            row.operator("image.sv_bgimage_remove", text='all', icon='X')
            row.operator("image.sv_bgimage_remove_unused", text='unused', icon='X')
            row.prop(context.space_data,'show_background_images',text='Activate',expand=True,toggle=True)
            col.prop(main,'bgimage_preview', text='Preview',expand=True,toggle=True, icon='RESTRICT_VIEW_OFF')
            col.prop(main,'bgimage_debug', text='Debug',expand=True,toggle=True)
        if context.scene.bgimage_debug:
            col.label(text='EXISTING BGIMAGESETS:')
            for Y,bgo in enumerate(context.scene.bgobjects):
                row = col.row(align=True)
                row.label(text=str(Y))
                row.label(text=bgo.image.name)
                row.label(text=bgo.object.name)
                row.label(text=str(bgo.opened))
            col.label(text='EXISTING BACKGROUNDS:')
            for Y,bgs_existing in enumerate(context.space_data.background_images):
                row = col.row(align=True)
                row.label(text=str(Y))
                row.label(text=bgs_existing.image.name)
        col.label(text='  ')
        col.operator('object.sv_bgimage_new_slot', text='New', icon='ZOOMIN')
        for ind,bgo in enumerate(context.scene.bgobjects):
            row = col.row(align=True)
            if bgo.opened:
                row.prop(bgo, 'opened', text='', icon='TRIA_DOWN')
                if bgo.image and bgo.object:
                    try:
                        row.label(text=bgo.object.name)
                        a = row.operator('image.sv_bgimage_set_camera', text='',icon='RESTRICT_VIEW_OFF')
                        a.item = ind
                        row.operator('image.sv_bgimage_rem_bgimage', text='',icon='X').item = ind
                    except:
                        row.label(text='')
                cam = bgo.object
                img = bgo.image
                col.prop(bgo, "object")
                #col.template_ID(bgo, "object", open="camera.open")
                if context.scene.bgimage_preview:
                    col.template_ID_preview(bgo, 'image',open="image.open", rows=2, cols=3)
                else:
                    col.template_ID(bgo, 'image',open="image.open")
            else:
                row.prop(bgo, 'opened', text='', icon='TRIA_RIGHT')
                if bgo.image and bgo.object:
                    try:
                        row.label(text=bgo.object.name)
                        a = row.operator('image.sv_bgimage_set_camera', text='',icon='RESTRICT_VIEW_OFF')
                        a.item = ind
                        row.operator('image.sv_bgimage_rem_bgimage', text='',icon='X').item = ind
                    except:
                        row.label(text='')



def register():
    bpy.types.Scene.bgimage_panel = BoolProperty(
                                name="show main panel",
                                description="",
                                default = False)
    bpy.types.Scene.bgimage_preview = BoolProperty(
                                name="preview_images",
                                description="",
                                default = False)
    bpy.types.Scene.bgimage_debug = BoolProperty(
                                name="debug",
                                description="",
                                default = False)
    bpy.utils.register_class(SvBgImage)
    bpy.types.Scene.bgobjects = CollectionProperty(type=SvBgImage)
    bpy.utils.register_class(VIEW3D_PT_camera_bgimages2)
    bpy.utils.register_class(OP_SV_bgimage_setcamera)
    bpy.utils.register_class(OP_SV_bgimage_new_slot)
    bpy.utils.register_class(OP_SV_bgimage_remove)
    bpy.utils.register_class(OP_SV_bgimage_remove_unused)
    bpy.utils.register_class(OP_SV_bgimage_rem_bgimage)


def unregister():
    bpy.utils.unregister_class(OP_SV_bgimage_rem_bgimage)
    bpy.utils.unregister_class(OP_SV_bgimage_remove_unused)
    bpy.utils.unregister_class(OP_SV_bgimage_remove)
    bpy.utils.unregister_class(OP_SV_bgimage_new_slot)
    bpy.utils.unregister_class(OP_SV_bgimage_setcamera)
    bpy.utils.unregister_class(VIEW3D_PT_camera_bgimages2)
    bpy.utils.unregister_class(SvBgImage)
    try:
        del bpy.types.Scene.bgobjects
        del bpy.types.Scene.bgimage_panel
        del bpy.types.Scene.bgimage_preview
        del bpy.types.Scene.bgimage_debug
    except:
        pass

if __name__ == '__main__':
    register()
    '''for k,i in enumerate(bpy.data.images):
        bpy.context.scene.bgobjects.add()
        bpy.context.scene.bgobjects[-1].object = bpy.context.object
        bpy.context.scene.bgobjects[-1].image = i
    for k,t in enumerate(bpy.context.scene.bgobjects):
        print(t.object, t.image)
    '''
    #bpy.context.scene.bgobjects.clear()

