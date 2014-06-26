bl_info = {
    "name": "Fedge",
    "author": "nikitron.cc.ua",
    "version": (0, 1, 0),
    "blender": (2, 7, 5),
    "location": "View3D > Tool Shelf > 1D > select loose",
    "description": "selects objects and edges that lost",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy

class D1_select_loose(bpy.types.Operator):
    ''' Select loose edges '''
    bl_idname = "object.d1_select_loose_edges"
    bl_label = "Fedge"
    
    def make_edges(self, edges, name):
        for e in edges:
            if e.is_loose:
                return True
        return False
    
    def make_indeces(self, list, vertices):
        for e in list:
            for i in e.vertices:
                vertices.add(i)
    
    def select_loose_objt(self):
        objects = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in objects:
            if obj.type != 'MESH':
                continue
            data = obj.data
            if not len(data.vertices):
                obj.select = True
                continue
            vertices = set()
            self.make_indeces(data.edges, vertices)
            self.make_indeces(data.polygons, vertices)
            v = set([i for i in range(len(data.vertices))])
            if v.difference(vertices):
                obj.select = True
                continue
            lost = self.make_edges(data.edges, obj.name)
            if lost: obj.select = True
                
    
    def select_loose_edit(self):
        obj = bpy.context.active_object
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        selected_edges = False
        for edg in obj.data.edges:
            if edg.is_loose:
                edg.select = True
                selected_edges = True
        bpy.ops.object.editmode_toggle()
        if not selected_edges:
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            vertices = set()
            self.make_indeces(obj.data.edges, vertices)
            self.make_indeces(obj.data.polygons, vertices)
            for i, v in enumerate(obj.data.vertices):
                if i not in vertices:
                    v.select = True
            bpy.ops.object.editmode_toggle()
            
                
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            self.select_loose_objt()
        elif bpy.context.mode == 'EDIT_MESH':
            self.select_loose_edit()
        return {'FINISHED'}

class D1_select_loose_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Fedge"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = '1D'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator('object.d1_select_loose_edges', text='select loose')

addons_keymap = []
def register():
    bpy.utils.register_class(D1_select_loose)
    bpy.utils.register_class(D1_select_loose_panel)
    
    # short
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Fedge', space_type='VIEW_3D')
    kmi = km.keymap_items.new('object.d1_select_loose_edges', 'L', 'PRESS', shift=True, ctrl=True, alt=True)
    addons_keymap.append((km, kmi))
    km = wm.keyconfigs.addon.keymaps.new(name='Fedge', space_type='VIEW_3D')
    kmi = km.keymap_items.new('object.d1_select_loose_edges', 'L', 'PRESS', shift=True, ctrl=True, alt=True)
    addons_keymap.append((km, kmi))
    #new_shortcut.properties.name = 'd1_select_loose_edges'

def unregister():
    bpy.utils.unregister_class(D1_select_loose)
    bpy.utils.unregister_class(D1_select_loose_panel)
    
    for a, b in addons_keymap:
        a.keymap_items.remove(b)
        del a, b
    
if __name__ == "__main__":
    register()