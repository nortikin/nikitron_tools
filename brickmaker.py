bl_info = {
    "name": "Bricking",
    "author": "nikitron.cc.ua",
    "version": (0, 0, 6),
    "blender": (2, 7, 9),
    "location": "View3D > Tool Shelf > 1D > bricker",
    "description": "making fasade made from bkicks",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}


import bpy
import numpy as np
import collections as col
from mathutils.geometry import intersect_point_line as IPL
from mathutils import Vector as V
from mathutils import Matrix as M
import bmesh
#import timeit

# changelog
# download url: https://github.com/nortikin/nikitron_tools/blob/master/brickmaker.py
# 0.0.2 - simplification of UVconnect
# 0.0.3 - threshold became negative
# 0.0.4 - download url
# 0.0.5 - tryclean flag to choose to use both conditions - distance and overlap
        # or use one of distance or overlap if not tryclean
# 0.0.6 - in bisect disabled remove doubles to exclude error od removed BMverts
        # but in future it needed on this step i guess

def dodo(edges,k):
    for ed in edges:
        #print(k,ed)
        if k in ed:
            # used boolean to check if k is first or second vert
            # in edge to choose other one
            i = ed[int(not ed.index(k))]
            return ed, i
    return False, False

def compare(v1,v2,v3):
    # if vertex between points on same line = True
    vec, isit = IPL(V(v1),V(v2),V(v3))
    same = v1 == v2 or v1 == v3
    return same, isit

def beginline(edges):
    ed_first = False
    e0 = edges[0][0]
    e1 = edges[0][1]
    start = e0 # initial
    edges.pop(edges.index(edges[0]))
    return ed_first, e0, e1, start

def diments(object):
    # return height and minimal Z
    #pass
    a = [i[:][2] for i in object.bound_box]
    am = min(a)
    return object.dimensions[2], am

def rows_calc(rows,height,thick,object):
    z,zm = diments(object)
    rs = int(z//rows)
    
    rwslist_bottom = [zm+i*rows for i in range(rs)]
    rwslist_top    = [zm+i*rows+height for i in range(rs)]
    return rwslist_bottom, rwslist_top
    # should not work
    # list(zip(rwslist_bottom,rwslist_top))

def bmeshing(cut_me_vertices,cut_me_polygons):
    bm = bmesh.new()
    bm_verts = [bm.verts.new(V(v)) for v in cut_me_vertices]
    for face in cut_me_polygons:
        bm.faces.new([bm_verts[i] for i in face])
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
    geom_in = bm.verts[:] + bm.edges[:] + bm.faces[:]
    return bm, geom_in

def bisec(bm,geom_in,zb):
    #bm.verts.index_update()
    #bm.edges.index_update()
    #bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.00001)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    res = bmesh.ops.bisect_plane(
        bm, geom=geom_in, dist=0.00001,
        plane_co=V((0.0,0.0,zb)), plane_no=V((0.0,0.0,1.0)), use_snap_center=False,
        clear_outer=True, clear_inner=True)
    # res = dict(geom_cut=[], geom=[])
    #bm.verts.index_update()
    #bm.edges.index_update()
    #print(res)
    edges = []
    verts = []
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    #vets = {}
    for k in res['geom']:
        if isinstance(k, bmesh.types.BMVert):
            #verts[v.index] = bm.append(k.co)
            verts.append(k.co[:])
        else:
            edges.append([v.index for v in k.verts[:]])
    #edges = [[i,i+1] for i in range(len(verts)-1)]
    #edges.append([len(verts)-1,0])
    #verts = [i.co[:] for i in bm.verts]
    #print('bisectualism . . . . . . . . . . . .',edges,verts)
    return verts, edges

def bisec_all(rows,height,thick,in_verts,in_faces,object):
    verts_low = []
    edges_low = []
    verts_up = []
    edges_up = []
    for v,f in zip(in_verts, in_faces):
        verts_low_ = []
        edges_low_ = []
        verts_up_ = []
        edges_up_ = []
        zeds = rows_calc(rows,height,thick,object)
        #print(zeds)
        for zb,zt in zip(*zeds):
            bmL, geom_inL = bmeshing(v,f)
            resL = bisec(bmL, geom_inL,zb)
            bmU, geom_inU = bmeshing(v,f)
            resU = bisec(bmU, geom_inU,zt)
            # resLU = [V(0,0,0),V(0,0,0),V(0,0,0)...], [[0,1],[0,1],[0,1]...]
            verts_low_.append(resL[0])
            edges_low_.append(resL[1])
            verts_up_.append(resU[0])
            edges_up_.append(resU[1])
            print('resL:  . . . . . .',edges_up_)
            #for i in bm.verts:
            #    print('masonry',i.co[:])
            bmL.clear()
            bmL.free()
            bmU.clear()
            bmU.free()
        verts_low.extend(verts_low_)
        edges_low.extend(edges_low_)
        verts_up.extend(verts_up_)
        edges_up.extend(edges_up_)
    return verts_low, edges_low, verts_up, edges_up
    

def sorte(in_verts,in_edges):
    # sorting with chains consistency
    eout = []
    for edges in in_edges:
        ed_first, e0, e1, start = beginline(edges)
        # for nestedness objects[groups[edges[vertices[0,1]]]]
        # groups - isolated edges chains
        eout_1 = []
        eout_2 = []
        eout_2.append(start)
        eout_2.append(e1)
        #print('initially starts with %d and %d in %s.' % (e0,e1,str([e0,e1])))
        while edges:
            ed,e0 = dodo(edges,e1)
            #print('edges length is %d' % len(edges))
            #print('e0: %d; e1: %d in %s.' % (e0,e1,str(ed)))
            if type(e0) == int:
                # if not i than nothing to add:
                if ed_first:
                    # backword
                    eout_2.insert(0,e0)
                else:
                    # forward
                    eout_2.append(e0)
                if len(edges) == 1:
                    eout_1.append(eout_2)
                edges.pop(edges.index(ed))
                e1 = e0
            elif not ed_first:
                #print('start %d' % start)
                # check from first vertex rewind
                ed_first = True
                e1 = start
            else:
                # close group
                eout_1.append(eout_2)
                # chain is over, goto any other vertex:
                ed_first, e0, e1, start = beginline(edges)
                eout_2 = []
                eout_2.append(start)
                eout_2.append(e1)

        eout.append(eout_1)
    #print(eout)

    # same grouped vertices
    vout = [[[vers[ed] for ed in group] for group in edges] for edges, vers in zip(eout,in_verts)]
    return vout,eout


def remextra(rows,height,thick,threshold,vout,eout,tryclean):
    # remove extra vertices along one line
    vouter = []
    verts_out = []
    for verts in vout:
        vouter_1 = []
        verts_out_ = []
        for group in verts:
            gl = len(group)
            if gl == 2:
                vouter_1.append(group)
                verts_out_.extend(group)
            else:
                vouter_2 = []
                for i in range(gl):
                    if 0 < i < (gl-1):
                        # choose if online or less 0.01 distance
                        comp, dist = compare(group[i-1], group[i], group[i+1])
                        print(threshold, dist, comp)
                        #if not comp and abs(dist) > abs(threshold):
                        if tryclean:
                            if not comp and abs(dist) < abs(threshold):
                                vouter_2.append(group[i])
                                verts_out_.append(group[i])
                        else:
                            if not comp or abs(dist) < abs(threshold):
                                vouter_2.append(group[i])
                                verts_out_.append(group[i])
                    elif i == 0 or i == gl-1:
                        vouter_2.append(group[i])
                        verts_out_.append(group[i])
                vouter_1.append(vouter_2)
        vouter.append(vouter_1)
        verts_out.append(verts_out_)
    # edges from vertices
    edges_out = []
    for verts in vouter:
        k = 0
        edges_out_ = []
        for group in verts:
            gl = len(group)
            for i in range(1,gl):
                edges_out_.append([k+i-1,k+i])
            k += gl
        edges_out.append(edges_out_)
    return verts_out, edges_out

def UVconnect(vertsL,edgesL,vertsU,edgesU):
    vout,eout,fout = [],[],[]
    endvert = 0
    vout_,fout_ = [],[]
    for vl,el,vu,eu in zip(vertsL,edgesL,vertsU,edgesU):
        fout_ = []
        ll = len(vl)
        lu = len(vu)
        if ll == lu:
            #fout_ = [[i+endvert,i+ll+endvert,i+ll+endvert-1,i+endvert-1] for i in range(lu) if i>0]
            #eout_ = [[]]
            #fout_ = [[l[0]+endvert,u[0]+ll+endvert,u[1]+ll+endvert,l[1]+endvert] for l,u in zip(el,eu)]
            #vout.extend(vl)
            #vout.extend(vu)
            #endvert += ll+lu
            fout_ = [[l[0]+endvert,l[0]+ll+endvert,l[1]+ll+endvert,l[1]+endvert] for l in el]
            vout.extend(vl)
            zedobensich = vu[0][2]
            vu = [[i[0],i[1],zedobensich] for i in vl]
            vout.extend(vu)
            endvert += ll+lu
        elif ll > lu:
            #fout_ = [[]]
            #ex1=[[i[0]+endvert,i[1]+endvert] for i in el]
            #ex2=[[ll+i[0]+endvert,ll+i[1]+endvert] for i in eu]
            #eout_.extend(ex1)
            #eout_.extend(ex2)
            # https://youtu.be/oLfXdvtRhb8
            fout_ = [[l[0]+endvert,l[0]+ll+endvert,l[1]+ll+endvert,l[1]+endvert] for l in el]
            vout.extend(vl)
            zedobensich = vu[0][2]
            vu = [[i[0],i[1],zedobensich] for i in vl]
            vout.extend(vu)
            endvert += ll+ll
        elif ll < lu:
            fout_ = [[u[0]+endvert,u[0]+lu+endvert,u[1]+lu+endvert,u[1]+endvert] for u in eu]
            zeduntensich = vl[0][2]
            vl = [[i[0],i[1],zeduntensich] for i in vu]
            vout.extend(vl)
            vout.extend(vu)
            endvert += lu+lu

        #vl_ = [V(i) for i in vl]
        #vu_ = [V(i) for i in vu]
        #vout_.extend(vl)
        #vout_.extend(vu)
        #eout.extend(eout_)
        fout.extend(fout_)
    return vout,eout,fout

def makemesh(v,e,p):
    a = bpy.data.meshes.new('1Dbricks')
    b = bpy.data.objects.new('1Dbricks', a)
    #print(v)
    a.validate()
    if type(v[0]) == V:
        v = [vv[:] for vv in v]
    a.from_pydata(v,e,p)
    a.update(calc_edges=True)
    return b


class OP_bricker(bpy.types.Operator):
    ''' \
    Brick maker on fasade. \
    '''
    bl_idname = "object.bricker"
    bl_label = "Bricker"

    rows = bpy.props.FloatProperty(name='rows',default=0.15)
    height = bpy.props.FloatProperty(name='height',default=0.07)
    thick = bpy.props.FloatProperty(name='thickness',default=0.05)
    threshold = bpy.props.FloatProperty(name='thresh',default=-0.001)
    modifier = bpy.props.BoolProperty(name='modifier',default=True)
    tryclean = bpy.props.BoolProperty(name='tryclean',default=True)

    def execute(self, context):
        o = bpy.context.selected_objects[0]
        mw = o.matrix_world
        in_verts = [[i.co[:] for i in o.data.vertices]]
        in_faces = [[list(i.vertices) for i in o.data.polygons]]
        verts_low, edges_low, verts_up, edges_up = bisec_all(self.rows,self.height,self.thick,in_verts,in_faces,o)
        #print(verts_up,len(verts_up),edges_up,len(edges_up))
        vl,el = sorte(verts_low,edges_low)
        vu,eu = sorte(verts_up,edges_up)
        vertsL,edgesL = remextra(self.rows,self.height,self.thick,self.threshold,vl,el,self.tryclean)
        vertsU,edgesU = remextra(self.rows,self.height,self.thick,self.threshold,vu,eu,self.tryclean)
        #print('vertsL . . . . .. . . . . . .',vertsL[0],len(vertsL),edgesL[0],len(edgesL))
        vout,eout,fout = UVconnect(vertsL,edgesL,vertsU,edgesU)
        #print('UVconnect . . . . .. . . . . . .',vout[0],len(vout),eout[0],len(eout),fout[0],len(fout))
        #for v,e in zip(vertsL,edgesL):
        #for v,e in zip(verts_up,edges_up):
        #    object = makemesh(v,e,[])
        #    object = makemesh(v,e,f) #(vout,eout,fout)
        #    bpy.context.scene.objects.link(object)
        object = makemesh(vout,eout,fout)
        bpy.context.scene.objects.link(object)
        object.matrix_world = mw
        if self.modifier:
            m = object.modifiers.new('Solid_brick',type='SOLIDIFY')
            m.thickness = self.thick*2
            m.offset = 0.0
        else:
            bpy.data.scenes[bpy.context.scene.name].objects.active = object
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.solidify(thickness=-self.thick)
            bpy.ops.object.editmode_toggle()


        return {'FINISHED'}

class OP_bricker_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Bricker"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = '1D'

    rows = bpy.props.FloatProperty(name='rows',default=0.15)
    height = bpy.props.FloatProperty(name='height',default=0.07)
    thick = bpy.props.FloatProperty(name='thickness',default=0.05)
    threshold = bpy.props.FloatProperty(name='thresh',default=-0.001)
    modifier = bpy.props.BoolProperty(name='modifier',default=True)
    tryclean = bpy.props.BoolProperty(name='tryclean',default=True)

    def draw(self, context):
        ''' \
        Brick making on facade \
        '''
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene, 'D1Brickerrows')
        row.prop(context.scene, 'D1Brickerheight')
        row = col.row(align=True)
        row.prop(context.scene, 'D1Brickerthick')
        row.prop(context.scene, 'D1Brickerthreshold')
        row = col.row(align=True)
        row.prop(context.scene, 'D1Brickermodifier')
        row.prop(context.scene, 'D1Brickertryclean')
        row = col.row(align=True)
        bm = row.operator('object.bricker', text='',icon='FACESEL_HLT')
        bm.rows = context.scene.D1Brickerrows
        bm.height = context.scene.D1Brickerheight
        bm.thick = context.scene.D1Brickerthick
        bm.threshold = context.scene.D1Brickerthreshold
        bm.modifier = context.scene.D1Brickermodifier
        bm.tryclean = context.scene.D1Brickertryclean



def register():
    bpy.types.Scene.D1Brickerrows = bpy.props.FloatProperty(name='rows',default=0.15)
    bpy.types.Scene.D1Brickerheight = bpy.props.FloatProperty(name='height',default=0.07)
    bpy.types.Scene.D1Brickerthick = bpy.props.FloatProperty(name='thick',default=0.05)
    bpy.types.Scene.D1Brickerthreshold = bpy.props.FloatProperty(name='threshold',default=-0.001)
    bpy.types.Scene.D1Brickermodifier = bpy.props.BoolProperty(name='modifier',description='use modifier or solidifier?',default=True)
    bpy.types.Scene.D1Brickertryclean = bpy.props.BoolProperty(name='tryclean',description='Try to make clean joints?',default=True)
    #bpy.types.Scene.D1Bricker = bpy.props.CollectionProperty(type=SvBricker)
    bpy.utils.register_class(OP_bricker)
    bpy.utils.register_class(OP_bricker_panel)

def unregister():
    bpy.utils.unregister_class(OP_bricker_panel)
    bpy.utils.unregister_class(OP_bricker)
    del bpy.types.Scene.D1Brickerrows
    del bpy.types.Scene.D1Brickerheight
    del bpy.types.Scene.D1Brickerthick
    del bpy.types.Scene.D1Brickerthreshold
    del bpy.types.Scene.D1Brickermodifier

if __name__ == '__main__':
    register()