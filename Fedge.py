bl_info = {
    "name": "Fedge",
    "author": "nikitron.cc.ua",
    "version": (0, 1, 2),
    "blender": (2, 7, 5),
    "location": "View3D > Tool Shelf > 1D > select loose",
    "description": "selects objects and edges that lost",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy

WRONG_AREA = 0.02

class D1_fedge(bpy.types.Operator):
    ''' \
    Select loose parts. edges first, vertices second, non-quad polygons third. \
    Выделяет потеряные рёбра, потом вершины и грани, каждый раз вызываясь. \
    '''
    bl_idname = "object.fedge"
    bl_label = "Fedge"
    
    def make_edges(self, edges, name):
        for e in edges:
            if e.is_loose:
                return True
        return False
    
    # makes indexes set for compare with vertices 
    # in object and find difference
    def make_indeces(self, list, vertices):
        for e in list:
            for i in e.vertices:
                vertices.add(i)

    def make_areas(self, pols):
        for p in pols:
            if p.area <= WRONG_AREA:
                return True
        return False
    
    def select_loose_objt(self):
        objects = bpy.context.selected_objects
        if not objects:
            self.report({'ERROR'},\
                'ALARMA!!!\n'+
                'Fedge founds no objects selected.\n'+
                'Select objects or enter edit mode.')
            return
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in objects:
            if obj.type != 'MESH':
                continue
            data = obj.data
            if not len(data.vertices):
                obj.select = True
                if obj.name[:9] != '__fedge__':
                    obj.name = '__fedge__' + obj.name
                continue
            vertices = set()
            self.make_indeces(data.edges, vertices)
            self.make_indeces(data.polygons, vertices)
            v = set([i for i in range(len(data.vertices))])
            if v.difference(vertices):
                obj.select = True
                continue
            if not obj.select:
                obj.select = self.make_areas(obj.data.polygons)
            lost = self.make_edges(data.edges, obj.name)
            if lost: obj.select = True
                
    
    def select_loose_edit(self):
        obj = bpy.context.active_object
        
        # stage one edges
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        selected_edges = False
        # bpy.ops.mesh.select_non_manifolds()
        # manifolds not work because we not come to next stage 
        for edg in obj.data.edges:
            if edg.is_loose:
                edg.select = True
                selected_edges = True
        bpy.ops.object.editmode_toggle()
        
        # stage two verts
        if not selected_edges:
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            vertices = set()
            self.make_indeces(obj.data.edges, vertices)
            self.make_indeces(obj.data.polygons, vertices)
            for i, ver in enumerate(obj.data.vertices):
                if i not in vertices:
                    ver.select = True
                    selected_edges = True
            bpy.ops.object.editmode_toggle()
            
        #stage
        if not selected_edges:
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            for pol in obj.data.polygons:
                if pol.area <= WRONG_AREA:
                    pol.select = True
                    selected_edges = True
            bpy.ops.object.editmode_toggle()
            
        #stage three polygons
        if not selected_edges:
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            # bpy.ops.mesh.select_face_by_sides(number=4, type='NOTEQUAL')
            # not fit ours needs selectfacesbysides
            for pol in obj.data.polygons:
                if len(pol.vertices) != 4:
                    pol.select = True
                    selected_edges = True
            # object mode if mesh clean
            if selected_edges:
                bpy.ops.object.editmode_toggle()
            else:
                self.report({'INFO'}, \
                    'FEDGE: Your object is clean')

    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            self.select_loose_objt()
        elif bpy.context.mode == 'EDIT_MESH':
            self.select_loose_edit()
        return {'FINISHED'}

class D1_fedge_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Fedge"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = '1D'
    
    def draw(self, context):
        ''' \
        If not finds loose - returs object mode \
        Если нет потеряшек - возвращается в объектный режим \
        '''
        layout = self.layout
        row = layout.row(align=True)
        row.operator('object.fedge', text='fedge')

def register():
    bpy.utils.register_class(D1_fedge)
    bpy.utils.register_class(D1_fedge_panel)
    
    # short
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Fedge', space_type='EMPTY')
    kmi = km.keymap_items.new('object.fedge', 'L', 'PRESS', shift=True, ctrl=True, alt=True)
    addons_keymap = []
    addons_keymap.append((km, kmi))
    #km = wm.keyconfigs.addon.keymaps.new(name='Fedge', space_type='VIEW_3D')
    #kmi = km.keymap_items.new('mesh.fedge', 'L', 'PRESS', shift=True, ctrl=True, alt=True)
    #addons_keymap.append((km, kmi))
    #new_shortcut.properties.name = 'd1_select_loose_edges'

def unregister():
    bpy.utils.unregister_class(D1_fedge_panel)
    bpy.utils.unregister_class(D1_fedge)
    
    for a, b in addons_keymap:
        a.keymap_items.remove(b)
        del a, b
    del addons_keymap

if __name__ == "__main__":
    register()
