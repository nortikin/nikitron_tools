# GPL-3 license


bl_info = {
    "name": "Nikitron tools",
    "version": (0, 1, 4),
    "blender": (2, 6, 9), 
    "category": "Object",
    "author": "Nikita Gorodetskiy",
    "location": "object",
    "description": "Nikitron tools - vertices and object names, curves to 3d, material to object mode, spread objects, bounding boxes",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/Nikitron_tools",          
    "tracker_url": "http://www.blenderartists.org/forum/showthread.php?272679-Addon-WIP-Sverchok-parametric-tool-for-architects",  
}


import bpy
from mathutils.geometry import intersect_line_plane
import mathutils
from mathutils import Vector
import math
from math import radians
import re
import random
import bmesh
from bpy_extras.object_utils import object_data_add

class EdgeLength(bpy.types.Operator):
    """EdgeLength"""
    bl_idname = "object.nt_edgelength"
    bl_label = "EDG_LEN"
    bl_options = {'REGISTER', 'UNDO'}
    
    length = bpy.props.StringProperty(name='длина', default='')
    
    def execute(self, context):
        self.length = str(self.calclength())
        return {'FINISHED'}

    def calclength(self):
        obj = bpy.context.selected_objects
        allthelength = []
        for o in obj:
            v = o.data.vertices
            for e in o.data.edges:
                ev = e.vertices
                diff = v[ev[0]].co-v[ev[1]].co
                edglength = diff.length
                allthelength.append(edglength)
        summa = sum(allthelength)
        return round(summa, 4)

class AreaOfLenin(bpy.types.Operator):
    """Area of any object"""
    bl_idname = "object.nt_areaoflenin"
    bl_label = "OB_AREA"
    bl_options = {'REGISTER', 'UNDO'}
    
    area = bpy.props.StringProperty(name='площадь', default='')
    
    def execute(self, context):
        self.area = str(self.calcarea())
        return {'FINISHED'}

    def calcarea(self):
        obj = bpy.context.selected_objects
        allthearea = []
        for o in obj:
            for p in o.data.polygons:
                allthearea.append(p.area)
        summa = sum(allthearea)
        return round(summa, 4)

class CliffordAttractors(bpy.types.Operator):
    """ Clifford Attractors with curves """
    bl_idname = "object.nt_cliffordattractors"
    bl_label = "CLIF_CURVES"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Code adapted by Eduardo Maldonado (Elbrujodelatribu)
    # Most of them from addon add_curve_extra_objects
    #      -> add_curve_spirals.py (see it in your Blender release)
    # Info about the attractor in http://paulbourke.net/fractals/clifford/
    
    # STARTING LOCATION
    position_x = bpy.props.FloatProperty(name='позиция_x', default=0.1)
    position_y = bpy.props.FloatProperty(name='позиция_y', default=0.0)
    position_z = bpy.props.FloatProperty(name='позиция_z', default=0.0)
    
    # SEED / CONSTANTS
    x_1 = bpy.props.FloatProperty(name='x_волна', default=-1.4, description='размер волны')
    x_2 = bpy.props.FloatProperty(name='x_габарит', default=1.0, description='ширина')
    y_1 = bpy.props.FloatProperty(name='y_волна', default=1.6, description='размер волны')
    y_2 = bpy.props.FloatProperty(name='y_габарит', default=0.7, description='глубина')
    z_1 = bpy.props.FloatProperty(name='z_волна', default=0.2, description='размер волны')
    z_2 = bpy.props.FloatProperty(name='z_габарит', default=0.5, description='высота')
    
    iterations = bpy.props.IntProperty(name='iterations', default=500, min=200, max=4000)
    
    #ADD VERTICES TO A SPLINE
    def makeBezier(self, spline, vertList):
        numPoints = (len(vertList) / 3) - 1
        spline.bezier_points.add(numPoints)
        spline.bezier_points.foreach_set("co", vertList)
        for point in spline.bezier_points:
            point.handle_left_type = "AUTO"
            point.handle_right_type = "AUTO"
    
    def execute(self, context):
        # VERTEX LIST FOR THE ATTRACTOR
        vertList = []
        px = self.position_x
        py = self.position_y
        pz = self.position_z

        # SEED / CONSTANTS
        a = self.x_1
        b = self.y_1
        c = self.x_2
        d = self.y_2
        e = self.z_1
        f = self.z_2

        # INIT itr VARIABLE
        itr = 0

        #CREATE AND ADD VERTICES
        while itr < self.iterations:
            #CLIFFORD ATTRACTOR ALGORITHM MODIFIED FOR 3D
            newpx = math.sin(a*py) + c*math.cos(a*px)
            newpy = math.sin(b*px) + d*math.cos(b*py)
            newpz = math.sin(e*px) + f*math.cos(e*pz)
            
            #SAVE CURRENT POINT FOR NEXT ITERATION
            px = newpx
            py = newpy
            pz = newpz

            #SKIP FIRST 100 ITERATIONS AND ADD VERTICES
            if (itr > 100):
                vertList.append( newpx )
                vertList.append( newpy )
                vertList.append( newpz )
            itr += 1

        # BUILD THE ATTRACTOR - A BEZIER CURVE
        crv = bpy.data.curves.new("Attractor", type = "CURVE")
        crv.dimensions = '3D'
        crv.splines.new(type = 'BEZIER')
        spline = crv.splines[0]
        self.makeBezier(spline, vertList)
        
        # CREATE OBJECT
        new_obj = object_data_add(bpy.context, crv)
        return {'FINISHED'}

class ComplimentWoman(bpy.types.Operator):
    """Делайте дамам приятно"""
    bl_idname = "object.nt_compliment_wom"
    bl_label = "комплимент"
    bl_options = {'REGISTER', 'UNDO'}
    
    compliment = bpy.props.StringProperty(name='compliment', default='')
    
    def execute(self, context):
        #a = context.window_manager
        #a.progress_begin(0,1)
        self.report({'INFO'}, self.main())
        #a.progress_update(0.5)
        #a.progress_end()
        return {'FINISHED'}
    
    def w(self, a):
        return random.choice(a)
    
    def main(self):
        a1 = ['Ты',]
        a2 = ['так', 'офигенски', 'просто', 'невероятно', 'супер', 'безумно', 'нереально']
        a3 = ['круто','потрясно','вкусно','улётно','клёво','прелестно','замечательно']
        a4 = ['выглядишь','пахнешь','целуешься','печёшь пирожки','двигаешься','танцуешь','готовишь','поёшь','смеёшься','работаешь']
        a5 = ['пупсик','дорогая','милая','солнце','зайка','как всегда','моя королева','бегемотик']
        compliment = (str(self.w(a1))+' '+ str(self.w(a2))+ ' '+ str(self.w(a3))+ \
                        ' '+ str(self.w(a4)) + ','+ ' '+ str(self.w(a5)) + '!'
                        )
        self.compliment = compliment
        return compliment
    
    #def invoke(self, context, event):
        #wm = context.window_manager
        #return wm.invoke_props_dialog(self)
    
class CurvesTo3D (bpy.types.Operator):
    """Put curves to ground and turn to 3d mode (wiring them) for farthere spread to layout sheet"""
    bl_idname = "object.nt_curv_to_3d"
    bl_label = "CURV_3D"
    bl_options = {'REGISTER', 'UNDO'} 
    
    thikns = bpy.props.FloatProperty(name='толщина', default=0.0)
    resolution = bpy.props.IntProperty(name='разрешение', default=12)
    smooth = bpy.props.BoolProperty(name='сгладить', default=True)
    bezier = bpy.props.BoolProperty(name='безье', default=False)
    variants_ = ['AUTOMATIC', 'VECTOR', 'ALIGNED', 'FREE_ALIGN', 'TOGGLE_FREE_ALIGN']
    variants = [tuple(3*[x]) for x in variants_]
    handle = bpy.props.EnumProperty(items=variants, name='тип рычажков', default='VECTOR')
    bevel = bpy.props.FloatProperty(name='закругление', default=0.0)
    bev_resolution = bpy.props.IntProperty(name='разрешение', default=0)
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        if obj[0].type == 'CURVE':
            bpy.ops.object.select_all(action='DESELECT')
            for o in obj:
                o.data.extrude = self.thikns
                o.data.dimensions = '3D'
                #o.matrix_world.translation[2] = 0
                nam = o.data.name
                # Я фанат группы "Сплин", ребята.
                for splin in bpy.data.curves[nam].splines:
                    splin.use_smooth = self.smooth
                o.data.resolution_u = self.resolution
                o.data.bevel_depth = self.bevel
                o.data.bevel_resolution = self.bev_resolution
                if self.bezier:
                    bpy.data.objects[nam].select = True
                    bpy.context.scene.objects.active = bpy.data.objects[nam]
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.curve.select_all(action='SELECT')
                    bpy.ops.curve.spline_type_set(type='BEZIER', use_handles=False)
                    bpy.ops.curve.handle_type_set(type=self.handle)
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return {'FINISHED'}

class CurvesTo2D (bpy.types.Operator):
    """Curves turn to 2d mode (and thicken 0.03 mm)"""
    bl_idname = "object.nt_curv_to_2d"
    bl_label = "CURV_2D"
    bl_options = {'REGISTER', 'UNDO'} 
    
    thikns = bpy.props.FloatProperty(name='толщина', default=0.0016)
    resolution = bpy.props.IntProperty(name='разрешение', default=12)
    smooth = bpy.props.BoolProperty(name='сгладить', default=False)
    bezier = bpy.props.BoolProperty(name='безье', default=False)
    variants_ = ['AUTOMATIC', 'VECTOR', 'ALIGNED', 'FREE_ALIGN', 'TOGGLE_FREE_ALIGN']
    variants = [tuple(3*[x]) for x in variants_]
    handle = bpy.props.EnumProperty(items=variants, name='тип рычажков', default='VECTOR')
    bevel = bpy.props.FloatProperty(name='закругление', default=0.0)
    bev_resolution = bpy.props.IntProperty(name='разрешение', default=0)
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        if obj[0].type == 'CURVE':
            bpy.ops.object.select_all(action='DESELECT')
            for o in obj:
                o.data.extrude = self.thikns
                o.data.dimensions = '2D'
                nam = o.data.name
                # Я фанат группы "Сплин", ребята.
                for splin in bpy.data.curves[nam].splines:
                    splin.use_smooth = self.smooth
                    for point in splin.bezier_points:
                        point.radius = 1.0
                o.data.resolution_u = self.resolution
                o.data.bevel_depth = self.bevel
                o.data.bevel_resolution = self.bev_resolution

                if self.bezier:
                    bpy.data.objects[nam].select = True
                    bpy.context.scene.objects.active = bpy.data.objects[nam]
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.curve.select_all(action='SELECT')
                    bpy.ops.curve.spline_type_set(type='BEZIER', use_handles=False)
                    bpy.ops.curve.handle_type_set(type=self.handle)
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}
 #breakpoint
class ObjectNames (bpy.types.Operator):
    """Make all objects show names in 3d"""      
    bl_idname = "object.nt_name_objects" 
    bl_label = "OB_NAMES"        
    bl_options = {'REGISTER', 'UNDO'} 
    
    size = bpy.props.FloatProperty(name='размер', default=1.0)
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        
        for ob in obj:
            mw = ob.matrix_world
            name_all = re.match(r'(\w+)', ob.name)
            name = name_all.group(1)
            len = 1#abs(max(ob.dimensions) * (sum(mw.to_scale()) / 3))
            #print ()
            self.run(mw,name,len)
        return {'FINISHED'}

    def run(self, origin,text,length):
       # Create and name TextCurve object
        bpy.ops.object.text_add(view_align=False,
        enter_editmode=False,location=origin.translation[:], 
        rotation=origin.to_euler()[:])
        ob = bpy.context.object
        ob.name = 'lable_'+str(text)
        tcu = ob.data
        tcu.name = 'lable_'+str(text)
        # TextCurve attributes
        tcu.body = str(text)
        tcu.font = bpy.data.fonts[0]
        tcu.offset_x = 0
        tcu.offset_y = -0.25
        tcu.resolution_u = 2
        tcu.shear = 0
        Tsize = self.size #* length
        tcu.size = Tsize
        tcu.space_character = 1
        tcu.space_word = 1
        tcu.align = 'CENTER'
        # Inherited Curve attributes
        tcu.extrude = 0.0
        tcu.fill_mode = 'NONE'
        
        
class VerticesNumbers3D (bpy.types.Operator):
    """make all vertices show numbers in 3D"""      
    bl_idname = "object.nt_vertices_numbers3d"
    bl_label = "VERT_NUM"
    bl_options = {'REGISTER', 'UNDO'}
    
    size = bpy.props.FloatProperty(name='размер', default=0.1)
    
    def execute(self, context):
        obj = bpy.context.selected_objects[0]
        mw = obj.matrix_world
        mesh = obj.data
        size1 = 1#abs(max(obj.dimensions) * (sum(mw.to_scale()) / 3))
        if obj.type == 'MESH':
            mesh.update()
            ver = mesh.vertices
        else:
            ver = mesh.splines[0].bezier_points
        i = 0
        for id in ver:
            coor = mw * ver[i].co
            self.run(coor, i, size1)
            i += 1
        return {'FINISHED'}
    
    def run(self, origin, text, size1):
        # Create and name TextCurve object
        bpy.ops.object.text_add(
        location=origin,
        rotation=(radians(90),radians(0),radians(0)))
        ob = bpy.context.object
        ob.name = 'vert '+ str(text)
        tcu = ob.data
        tcu.name = 'vert '+ str(text)
        # TextCurve attributes
        tcu.body = str(text)
        tcu.font = bpy.data.fonts[0]
        tcu.offset_x = 0
        tcu.offset_y = 0
        tcu.shear = 0
        tcu.size = self.size # * size1 
        tcu.space_character = 1
        tcu.space_word = 1
        # Inherited Curve attributes
        tcu.extrude = 0
        tcu.fill_mode = 'BOTH'

vert_max = 0

class Connect2Meshes (bpy.types.Operator):
    """connect two objects by mesh edges with vertices shift and hooks to initial objects. Соединить два объекта"""      
    bl_idname = "object.nt_connect2objects"
    bl_label = "CONNECT_2_OB"
    bl_options = {'REGISTER', 'UNDO'}
    
    nt_shift_verts = bpy.props.IntProperty(name="смещение вершин", description="shift vertices of smaller object, it can reach     maximum (look right), to make patterns", default=0, min=0, max=1000)
    
    def dis(self, x,y):
        vec = mathutils.Vector((x[0]-y[0], x[1]-y[1], x[2]-y[2]))
        return vec.length
    
    def maxObj(self, ver1, ver2, mw1, mw2):
        if len(ver1) > len(ver2):
            inverc = 0
            vert1 = ver1
            mworld1 = mw1
            vert2 = ver2
            mworld2 = mw2
        else:
            inverc = 1
            vert1 = ver2
            mworld1 = mw2
            vert2 = ver1
            mworld2 = mw1
        cache_max = [vert1, mworld1]
        cache_min = [vert2, mworld2]
        return cache_max, cache_min, inverc
    
    def points(self, ver1, ver2, mw1, mw2, shift):
        vert_new = []
        # choosing maximum vertex count in ver1/2, esteblish vert2 - mincount of vertex
        cache = self.maxObj(ver1, ver2, mw1, mw2)
        vert1 = cache[0][0]
        vert2 = cache[1][0]
        mworld1 = cache[0][1]
        mworld2 = cache[1][1]
        inverc = cache[2]
        # append new verts in new obj
        for v in vert2:
            v2 = mworld2 * v.co
            if len(vert2) > v.index + shift:
                v1 = mworld1 * vert1[v.index + shift].co
            else:
                v1 = mworld1 * vert1[v.index + shift - len(vert2)].co
            if inverc == True:
                m1 = mworld2.translation
                m2 = mworld2.translation
            else:
                m1 = mworld1.translation
                m2 = mworld1.translation
            vert_new.append(v2 - m2)
            vert_new.append(v1 - m1)
        return vert_new
    
    def edges(self, vert_new):
        edges_new = []
        i = -2
        for v in vert_new:
            # dis(vert_new[i],vert_new[i+1]) < 10 and 
            if i > -1 and i < (len(vert_new)):
                edges_new.append((i,i + 1))
            i += 2
        return edges_new
    
    def mk_me(self, name):
        me = bpy.data.meshes.new(name+'Mesh')
        return me
    
    def mk_ob(self, mesh, name, mw):
        loc = mw.translation.to_tuple()
        ob = bpy.data.objects.new(name, mesh)
        ob.location = loc
        ob.show_name = True
        bpy.context.scene.objects.link(ob)
        return ob
    
    def def_me(self, mesh, ver1, ver2, mw1, mw2, obj1, obj2, nam):
        ver = self.points(ver1, ver2, mw1, mw2, bpy.context.scene.nt_shift_verts)
        edg = self.edges(ver)
        mesh.from_pydata(ver, edg, [])
        mesh.update(calc_edges=True)
        if bpy.context.scene.nt_hook_or_not:
            self.hook_verts(ver, obj1, obj2, nam, ver1, ver2, mw1, mw2)
        return
    
    # preparations for hooking
    def hook_verts(self, ver, obj1, obj2, nam, ver1, ver2, mw1, mw2):
        # pull cache from maxObj
        cache = self.maxObj(ver1, ver2, mw1, mw2)
        vert1 = cache[0][0]
        vert2 = cache[1][0]
        mworld1 = cache[0][1]
        mworld2 = cache[1][1]
        inverc = cache[2]
        points_ev = []
        points_od = []
        # devide even/odd verts
        for v in ver:
            if (ver.index(v) % 2) == 0:
                points_ev.append(ver.index(v))
                # print ('чёт ' + str(ver.index(v)))
            else:
                points_od.append(ver.index(v))
                # print ('нечет ' + str(ver.index(v)))
        if bpy.context.selected_objects:
            bpy.ops.object.select_all(action='TOGGLE')
        # depend on bigger (more verts) object it hooks even or odd verts
        if inverc == False:
            # ob1 = obj1 ob2 = obj2, 1 - bigger
            self.hooking_action(obj2, nam, points_ev, ver)
            self.hooking_action(obj1, nam, points_od, ver)
        else:
            # ob1 = obj2 ob2 = obj1, 2 - bigger
            self.hooking_action(obj2, nam, points_od, ver)
            self.hooking_action(obj1, nam, points_ev, ver)
        
    # free hooks :-)
    def hooking_action(self, ob, nam, points, verts_of_object):
        # select 1st obj, second connection
        bpy.data.scenes[bpy.context.scene.name].objects[ob.name].select = True
        bpy.data.scenes[bpy.context.scene.name].objects[nam].select = True
        bpy.data.scenes[bpy.context.scene.name].objects.active = bpy.data.objects[nam]
        # deselect vertices
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.editmode_toggle()
        # select nearby vertices
        for vert in points:
            bpy.context.object.data.vertices[vert].select = True
        # hook itself
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.hook_add_selob(use_bone=False)
        #bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.editmode_toggle()
        # deselect all
        bpy.ops.object.select_all(action='TOGGLE')

    def maxim(self):
        if bpy.context.selected_objects[0].type == 'MESH':
            if len(bpy.context.selected_objects) >= 2:     
                len1 = len(bpy.context.selected_objects[0].data.vertices)
                len2 = len(bpy.context.selected_objects[1].data.vertices)
                maxim = min(len1, len2)
                #print (maxim)
        return maxim
    
    def execute(self, context):
        
        bpy.types.Scene.nt_shift_verts = self.nt_shift_verts
        context.scene.update()
        obj1 = context.selected_objects[0]
        obj2 = context.selected_objects[1]
        mw1 = obj1.matrix_world
        mw2 = obj2.matrix_world
        mesh1 = obj1.data
        mesh1.update()
        mesh2 = obj2.data
        mesh2.update()
        ver1 = mesh1.vertices
        ver2 = mesh2.vertices
        nam = 'linked_' + str(obj1.name) + str(obj2.name)
        me = self.mk_me(nam)
        ob = self.mk_ob(me, nam, mw1)
        self.def_me(me, ver1, ver2, mw1, mw2, obj1, obj2, nam)
        print ('---- NIKITRON_connect2objects MADE CONNECTION BETWEEN: ' + str(obj1.name) + ' AND ' + str(obj2.name) + ' AND GOT ' + str(ob.name) + ' ----')
        return {'FINISHED'}


class MaterialToObjectAll (bpy.types.Operator):
    """all materials turned to object mode"""      
    bl_idname = "object.nt_materials_to_object"
    bl_label = "MAT_OB"
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        mode = 'OBJECT'
        for o in obj:
            materials = bpy.data.objects[o.name].material_slots
            for m in materials:
                m.link = mode
                print('материал "'+str(m.name)+'", объект "'+o.name+'", режим материала: '+mode)
        return {'FINISHED'}
    
class MaterialToDataAll (bpy.types.Operator):
    """all materials turned to data mode"""      
    bl_idname = "object.nt_materials_to_data"
    bl_label = "MAT_DAT"
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        mode = 'DATA'
        for o in obj:
            materials = bpy.data.objects[o.name].material_slots
            for m in materials:
                m.link = mode
                print('материал "'+str(m.name)+'", объект "'+o.name+'", режим материала: '+mode)
        return {'FINISHED'}


class NT_ClearNodesLayouts (bpy.types.Operator):
    """Delete nodes layouts, not active if node area presented in current screen layout. Change screen layout first"""      
    bl_idname = "object.nt_delete_nodelayouts"
    bl_label = "DEL_LAYOUTS"
    bl_options = {'REGISTER', 'UNDO'} 
    
    do_clear = bpy.props.BoolProperty(default=False, name='even used', description='remove even if layout has one user (not fake user)')
    
    def execute(self, context):
        self.do_clear = context.scene.nt_clean_layout_used
        trees = bpy.data.node_groups
        for area in bpy.context.window.screen.areas:
            if area.type == 'NODE_EDITOR':
                self.do_clear = False
        for T in trees:
            if T.bl_rna.name in ['Shader Node Tree']:
                continue
            if trees[T.name].users > 1 and T.use_fake_user == True:
                print ('Layout '+str(T.name)+' protected by fake user.')
            if trees[T.name].users == 1 and self.do_clear and T.use_fake_user == False:
                print ('cleaning user: '+str(T.name))
                trees[T.name].user_clear()
            if trees[T.name].users == 0:
                print ('removing layout: '+str(T.name)+' | '+str(T.bl_rna.name))
                bpy.data.node_groups.remove(T)
                
        return {'FINISHED'}


class DeleteOrientation (bpy.types.Operator):
    """Delete local Orientations (alt+space) for all objects you created"""      
    bl_idname = "object.nt_delete_orientation"
    bl_label = "DEL_ORIENT"
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        orients = bpy.data.scenes[bpy.context.scene.name].orientations
        for o in orients:
            if o.name != 'Global' or o.name != 'Local' or o.name != 'Normal' or o.name != 'Gimbal' or o.name != 'View':
                bpy.ops.transform.select_orientation(orientation=o.name)
                print (str(o.name)+' orientation deleted')
                bpy.ops.transform.delete_orientation()
        return {'FINISHED'}

class BooleratorRandom (bpy.types.Operator):
    """Boolen union Randomly
    Булен объединение
    nt_hook_or_not, Случайном порядке
    если нет - Обычном порядке поимённо"""      
    bl_idname = "object.nt_boolerator_random"
    bl_label = "BOOL_R"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        if bpy.context.scene.nt_hook_or_not:
            random.shuffle(objects)
        lenth = len(objects) - 1
        while lenth:
            bpy.ops.object.select_all(action='DESELECT')
            obj2 = objects[lenth]
            obj1 = objects[lenth - 1]
            name1 = obj1.name
            name2 = obj2.name
            bpy.data.objects[name2].select = True
            bpy.data.objects[name1].select = True
            bpy.context.scene.objects.active = bpy.data.objects[name1]
            md = obj1.modifiers.new('booleanunion', 'BOOLEAN')
            md.operation = 'UNION'
            md.object = obj2
            # apply the modifier
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleanunion")
            lenth -= 1
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[name2].select = True
            bpy.ops.object.delete()
            bpy.data.objects[name1].select = True
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}


class BooleratorIntersection (bpy.types.Operator):
    """Boolen union by Intersection
    Булен единство Пересечения"""      
    bl_idname = "object.nt_boolerator_intersection"
    bl_label = "BOOL_X"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        lenth = len(objects) - 1
        while lenth:
            bpy.ops.object.select_all(action='DESELECT')
            obj2 = objects[lenth]
            obj1 = objects[lenth - 1]
            self.check_bool(objects, lenth, obj1, obj2)
            lenth -= 1
        return {'FINISHED'}
    def interinsects(self, ob1, ob0):
        name1 = ob1.name
        name0 = ob0.name
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[name1].select = True
        bpy.data.objects[name0].select = True
        bpy.context.scene.objects.active = bpy.data.objects[name1]
        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        bpy.ops.object.join()
        obj = bpy.context.selected_objects[0]
        faces_intersect = self.bmesh_check_self_intersect_object(obj)
        bpy.ops.object.delete()
        if faces_intersect:
            bpy.data.objects[name1].select = True
            bpy.data.objects[name0].select = True
            return True
        else:
            return False
    
    def bmesh_check_self_intersect_object(self, obj):
        """
        Check if any faces self intersect
    
        returns an array of edge index values.
        """
        # Heres what we do!
        #
        # * Take original Mesh.
        # * Copy it and triangulate it (keeping list of original edge index values)
        # * Move the BMesh into a temp Mesh.
        # * Make a temp Object in the scene and assign the temp Mesh.
        # * For every original edge - ray-cast on the object to find which intersect.
        # * Report all edge intersections.
        # Triangulate
        bm = self.bmesh_copy_from_object(obj, transform=False, triangulate=False)
        face_map_index_org = {f: i for i, f in enumerate(bm.faces)}
        ret = bmesh.ops.triangulate(bm, faces=bm.faces, use_beauty=False)
        face_map = ret["face_map"]
        # map new index to original index
        face_map_index = {i: face_map_index_org[face_map.get(f, f)] for i, f in enumerate(bm.faces)}
        del face_map_index_org
        del ret
        # Create a real mesh (lame!)
        scene = bpy.context.scene
        me_tmp = bpy.data.meshes.new(name="~temp~")
        bm.to_mesh(me_tmp)
        bm.free()
        obj_tmp = bpy.data.objects.new(name=me_tmp.name, object_data=me_tmp)
        scene.objects.link(obj_tmp)
        scene.update()
        ray_cast = obj_tmp.ray_cast
        faces_error = False
        EPS_NORMAL = 0.000001
        EPS_CENTER = 0.01  # should always be bigger
        for ed in me_tmp.edges:
            v1i, v2i = ed.vertices
            v1 = me_tmp.vertices[v1i]
            v2 = me_tmp.vertices[v2i]
            # setup the edge with an offset
            co_1 = v1.co.copy()
            co_2 = v2.co.copy()
            co_mid = (co_1 + co_2) * 0.5
            no_mid = (v1.normal + v2.normal).normalized() * EPS_NORMAL
            co_1 = co_1.lerp(co_mid, EPS_CENTER) + no_mid
            co_2 = co_2.lerp(co_mid, EPS_CENTER) + no_mid
            co, no, index = ray_cast(co_1, co_2)
            if index != -1:
                faces_error = True
        scene.objects.unlink(obj_tmp)
        bpy.data.objects.remove(obj_tmp)
        bpy.data.meshes.remove(me_tmp)
        scene.update()
        return faces_error
    
    def bmesh_copy_from_object(self, obj, transform=True, triangulate=True, apply_modifiers=False):
        """
        Returns a transformed, triangulated copy of the mesh
        """
        #assert(obj.type == 'MESH')
        if apply_modifiers and obj.modifiers:
            import bpy
            me = obj.to_mesh(bpy.context.scene, True, 'PREVIEW', calc_tessface=False)
            bm = bmesh.new()
            bm.from_mesh(me)
            bpy.data.meshes.remove(me)
            del bpy
        else:
            me = obj.data
            if obj.mode == 'EDIT':
                bm_orig = bmesh.from_edit_mesh(me)
                bm = bm_orig.copy()
            else:
                bm = bmesh.new()
                bm.from_mesh(me)
        # TODO. remove all customdata layers.
        # would save ram
        if transform:
            bm.transform(obj.matrix_world)
        if triangulate:
            bmesh.ops.triangulate(bm, faces=bm.faces, use_beauty=True)
        return bm
    
    def check_bool(self, objects, lenth, obj1, obj2):
        inters = self.interinsects(obj1, obj2)
        if inters:
            self.boolerator(obj1, obj2)
        elif lenth > 2:
            obj1 = objects[lenth - 2]
            self.check_bool(objects, lenth - 1, obj1, obj2)
    
    def boolerator(self, obj1, obj2):
        name1 = obj1.name
        name2 = obj2.name
        bpy.data.objects[name2].select = True
        bpy.data.objects[name1].select = True
        bpy.context.scene.objects.active = bpy.data.objects[name1]
        md = obj1.modifiers.new('booleanunion', 'BOOLEAN')
        md.operation = 'UNION'
        md.object = obj2
        # apply the modifier
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleanunion")
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[name2].select = True
        bpy.ops.object.delete()
        bpy.data.objects[name1].select = True
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

class BooleratorTranslation (bpy.types.Operator):
    """Boolen union by Translation
    Булен единство от Перемещения"""      
    bl_idname = "object.nt_boolerator_translation"
    bl_label = "BOOL_T"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects_init = bpy.context.selected_objects
        lenth = len(objects_init)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        objects_dic = {}
        trans_init = objects_init[0].matrix_world.translation
        for obj in objects_init:
            trans_obj = obj.matrix_world.translation
            trans = Vector(((trans_obj[0]-trans_init[0]),
                            (trans_obj[1]-trans_init[1]),
                            (trans_obj[2]-trans_init[2])
                            ))
            lenth_obj = trans.length
            objects_dic[obj] = lenth_obj
        objects = sorted(objects_dic.items(), key=lambda x: x[1], reverse=True)
        for l in range(lenth):
            bpy.ops.object.select_all(action='DESELECT')
            #print ('l is:'+ str(l))
            if l == 0:
                continue
            elif l == lenth:
                break
            obj2 = objects[lenth-1][0]
            obj1 = objects[l - 1][0]
            name1 = obj1.name
            name2 = obj2.name
            #print (name1, name2)
            bpy.data.objects[name1].select = True
            bpy.data.objects[name2].select = True
            bpy.context.scene.objects.active = bpy.data.objects[name2]
            md = obj2.modifiers.new('booleanunion', 'BOOLEAN')
            md.operation = 'UNION'
            md.object = obj1
            # apply the modifier
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleanunion")
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[name1].select = True
            bpy.ops.object.delete()
        return {'FINISHED'}

class SeparatorM (bpy.types.Operator):
    """Objects separator on vert number count. разделитель объектов по количеству вершин"""      
    bl_idname = "object.nt_separator_multi"
    bl_label = "SEPARATE_OB"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.separate()
        return {'FINISHED'}
    def separate(self):
        objects = bpy.context.selected_objects
        goon = False
        vert_limit1 = bpy.context.scene.NS_vertices_separator
        vert_limit2 = vert_limit1*2
        vert_limit3 = vert_limit2-1
        vert_limit4 = vert_limit1*75
        for obj in objects:
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            name = obj.name
            lenth = len(bpy.data.objects[name].data.vertices)
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[name].select = True
            bpy.context.scene.objects.active = bpy.data.objects[name]
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            if lenth == vert_limit1:
                print ('объект ' + str(name) + ' готов')
            elif lenth == 0:
                print ('объект ' + str(name) + ' удаляется')
                bpy.ops.object.delete()
            else:
                print ('объект ' + str(name) + ' пока ещё НЕ разделан :-( ' + str(lenth))
            if lenth > vert_limit4:
                i = 3
                goon = True
                while i:
                    division = round(lenth / 3)
                    for v in bpy.data.objects[name].data.vertices[0:division]:
                        v.select = True
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.mesh.select_linked(limit=True)
                    bpy.ops.mesh.separate(type='SELECTED')
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    lenth = len(bpy.data.objects[name].data.vertices)
                    i -= 1
            
            elif lenth > vert_limit2:
                goon = True
                while lenth:
                    #bpy.ops.object.select_all(action='DESELECT')
                    #bpy.data.objects[name].select = True
                    if lenth <= vert_limit3:
                        lenth = 0
                        break
                    bpy.data.objects[name].data.vertices[0].select = True
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.mesh.select_linked(limit=True)
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.mesh.separate(type='SELECTED')
                    lenth = len(bpy.data.objects[name].data.vertices)
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            else:
                pass
        if goon:
            self.separate()
        print ('---- Разделка объектов окончена. ----  \n')


class BoundingBox (bpy.types.Operator):
    """Make bound boxes for selected objects in mesh. Делает габаритный куб"""      
    bl_idname = "object.nt_bounding_boxers"
    bl_label = "BOUND_BOX"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        i = 0
        for a in objects:
            self.make_it(i, a)
            i += 1
        return {'FINISHED'}
    
    def make_it(self, i, obj):
        box = bpy.context.selected_objects[i].bound_box
        mw = bpy.context.selected_objects[i].matrix_world
        name = (bpy.context.selected_objects[i].name + '_bounding_box')
        me = bpy.data.meshes.new(name+'Mesh')
        ob = bpy.data.objects.new(name, me)
        ob.location = mw.translation
        ob.scale = mw.to_scale()
        ob.rotation_euler = mw.to_euler()
        ob.show_name = True
        bpy.context.scene.objects.link(ob)
        loc = []
        for ver in box:
            loc.append(mathutils.Vector((ver[0],ver[1],ver[2])))
        me.from_pydata((loc), [], ((0,1,2,3),(0,1,5,4),(4,5,6,7), (6,7,3,2),(0,3,7,4),(1,2,6,5)))
        me.update(calc_edges=True)
        return

class SpreadObjects (bpy.types.Operator):
    """spread all objects on sheet for farthere use in dxf layout export. Раскладывает объекты по полу."""
    bl_idname = "object.nt_spread_objects"
    bl_label = "ORGANISE"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = bpy.context.selected_objects
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        count = len(obj) - 1                # items number
        row = math.modf(math.sqrt(count))[1] or 1 #optimal number of rows and columns !!! temporery solution
        locata = mathutils.Vector()    # while veriable 
        dx, dy, ddy = 0, 0, 0                       # distance
        while count > -1:   # iterations X
            locata[2] = 0               # Z = 0
            row1 = row
            x_curr = []                     # X bounds collection
            locata[1] = 0              # Y = 0
            while row1:         # iteratiorns Y
                # counting bounds
                bb = obj[count].bound_box
                mwscale = obj[count].matrix_world.to_scale()
                mwscalex = mwscale[0]
                mwscaley = mwscale[1]
                x0 = bb[0][0]
                x1 = bb[4][0]
                y0 = bb[0][1]
                y1 = bb[2][1]
                ddy = dy            # secondary distance to calculate avverage
                dx = mwscalex*(max(x0,x1)-min(x0,x1)) + 0.03        # seek for distance !!! temporery solution
                dy = mwscaley*(max(y0,y1)-min(y0,y1)) + 0.03        # seek for distance !!! temporery solution
                # shift y
                locata[1] += ((dy + ddy) / 2)
                # append x bounds
                x_curr.append(dx)
                bpy.ops.object.rotation_clear()
                bpy.context.selected_objects[count].location = locata
                row1 -= 1
                count -= 1
            locata[0] += max(x_curr)        # X += 1
            dx, dy, ddy = 0, 0, 0
            del(x_curr)
        return {'FINISHED'}
    
from bpy.props import IntProperty, BoolProperty

# this def for connect2objects maximum shift (it cannot update scene's veriable somehow)
def maxim():
    if len(bpy.context.selected_objects) >= 2:   
        if bpy.context.selected_objects[0].type == 'MESH':
            len1 = len(bpy.context.selected_objects[0].data.vertices)
            len2 = len(bpy.context.selected_objects[1].data.vertices)
            maxim = min(len1, len2)
            return maxim
bpy.types.Scene.nt_shift_verts = IntProperty(name="nt_shift_verts", description="shift vertices of smaller object. смещает вершины для соединения",  min=0, max=1000,  default = 0, options={'ANIMATABLE', 'LIBRARY_EDITABLE'})
bpy.types.Scene.NS_vertices_separator = IntProperty(name="separate", description="how many vertices in one object",  min=3, max=1000,  default = 8)
bpy.types.Scene.nt_clean_layout_used = BoolProperty(name="clean_layout_used", description="remove even if layout has one user (not fake user)", default = False)

    
# this flag for connetc2objects, hook or not?
bpy.types.Scene.nt_hook_or_not = BoolProperty(
    name="nt_hook_or_not",
    description="зацепить вершины к изначальным объектам.",
    default = True)



# this cache for define vertex count of currently selected materials.
#cache_obj = []
#def cache_add():
#    for i in bpy.context.selected_objects:
#        cache_obj.append(i)
#    print (cache_obj)
#cache_add()






class NikitronPanel(bpy.types.Panel):
    """ Panel Nikitron. Инструменты для работы """
    bl_idname = "panel.nikitron"
    bl_label = "Nikitron tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'NT'
    #bl_context = 'objectmode'
    #bl_options = {'HIDE_HEADER'}


    def draw(self, context):
        #global cache_obj
        #global cache_add
        #global shift
        global maxim
        layout = self.layout
        
        # it is all about maximum shift, it cannot update scene's veriable 'shift_verts' with 'maxim' veriable somehow
        #if context.selected_objects[0] != cache_obj[0]:
        #    bpy.data.scenes[0].update_tag()
        #    cache_obj = []
        #    cache_add()
        #    shift()

        
        box = layout.box()
        
        row = box.row(align=True)
        row.label(text="nt. GENERAL")
        #row = box.row(align=True)
        #row.operator("object.nt_compliment_wom")
        #row.operator('wm.url_open', text='мужицкий').url = 'http://w-o-s.ru/article/2469'
        
        
        col = box.column(align=True)
        col.scale_y=1.1
        col.operator("object.nt_spread_objects",icon="GRID")
        row = col.row(align=True)
        row.operator("object.nt_cliffordattractors",icon="OUTLINER_OB_CURVE")
        row = col.row(align=True)
        row.operator("object.nt_materials_to_object",icon="MATERIAL_DATA")
        row.operator("object.nt_materials_to_data",icon="MATERIAL_DATA")
            
        row = col.row(align=True)
        row.operator("object.nt_name_objects",icon="OUTLINER_OB_FONT")
        row.operator("object.nt_vertices_numbers3d",icon="FONT_DATA")
        
        row = col.row(align=True)
        row.operator("object.nt_bounding_boxers",icon="SNAP_VOLUME")
        row.operator("object.nt_delete_orientation",icon="MANIPUL")
        
        row = col.row(align=True)
        row.scale_y=1.1
        row.operator("object.nt_delete_nodelayouts",icon="NODE")
        row.prop(bpy.context.scene, "nt_clean_layout_used", text='AND USED')
        
        
        
        if context.selected_objects:
            if context.selected_objects[0].type == 'CURVE':
                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                row.scale_y=1.1
                row.label(text="nt. CURVES")
                row = col.row(align=True)
                row.operator("object.nt_curv_to_3d",icon="CURVE_DATA")
                row.operator("object.nt_curv_to_2d",icon="CURVE_DATA")
        
        if context.selected_objects:
            if context.selected_objects[0].type == 'MESH':
                box = layout.box()
                col = box.column(align=True)
                col.scale_y=1.1
                col.label(text="nt. MESH")
                row = col.row(align=True)
                row.scale_y=1.1
                row.operator("object.nt_edgelength",icon="FONT_DATA")
                row.operator("object.nt_areaoflenin",icon="FONT_DATA")
                row = col.row(align=True)
                row.operator("object.nt_separator_multi",icon="MOD_BUILD")
                row.prop(bpy.context.scene, "NS_vertices_separator", text='VERTS')
                row = col.row(align=True)
                row.operator("object.nt_boolerator_random",icon="MOD_BOOLEAN")
                row.operator("object.nt_boolerator_intersection",icon="MOD_BOOLEAN")
                row.operator("object.nt_boolerator_translation",icon="MOD_BOOLEAN")
                
                row = col.row(align=True)
                row.operator("object.nt_connect2objects",icon="LINKED")
                row = col.row(align=True)
                row.scale_y=1.1
                row.prop(bpy.context.scene, "nt_shift_verts", text="SHIFT")
                row.prop(bpy.context.scene, "nt_hook_or_not", text="HOOK?")
                row.label(text="MAX " + str(maxim()))
                
        
my_classes = [
                CurvesTo3D, CurvesTo2D, NikitronPanel, ObjectNames,
                VerticesNumbers3D, Connect2Meshes, MaterialToObjectAll,
                MaterialToDataAll, BoundingBox, SpreadObjects,
                DeleteOrientation, SeparatorM, BooleratorRandom,
                BooleratorTranslation, BooleratorIntersection,
                ComplimentWoman, AreaOfLenin, EdgeLength,
                CliffordAttractors, NT_ClearNodesLayouts
                ]
    
def register():
    for clas in my_classes:
        bpy.utils.register_class(clas)

def unregister():
    for clas in my_classes:
        bpy.utils.unregister_class(clas)
    
if __name__ == "__main__":
    register()