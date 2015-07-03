from math import degrees
import bpy
import mathutils


def do_file():
    obj = bpy.context.selected_objects[0]
    data = obj.data

    outdict = {}
    for i, e in enumerate(data.edges):
        ver1, ver2 = data.vertices[e.vertices[0]].co, data.vertices[e.vertices[1]].co
        vec1 = mathutils.Vector((0,1,0))
        vec2 = ver2-ver1
        angle = int(degrees(vec1.angle(vec2)))
        outdict[i] = [angle, round(ver2[0],3), round(ver2[1],3), round(ver1[0],3), round(ver1[1],3), round(vec2.length,3), round(-vec2.length,3)]

    a_file = '''*PATTERN1, Nikitron'''

    for val in outdict.values():
        out = str(val[:])[1:-1]
        a_file += '\n'+out
    return a_file

def do_text(a_file):
    texts = bpy.data.texts.items()
    ex = False
    for t in texts:
        if bpy.data.texts[t[0]].name == 'pattern_zwcad':
            bpy.data.texts['pattern_zwcad'].clear()
            ex=True
            break
    if not ex:
        bpy.data.texts.new('pattern_zwcad')
        bpy.data.texts['pattern_zwcad'].clear()
    bpy.data.texts['pattern_zwcad'].write(a_file)

a_file = do_file()
do_text(a_file)
