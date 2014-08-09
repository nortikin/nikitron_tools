import bpy
from mathutils import Vector
from math import sqrt
i = -5
while i < 5:
    name = str(i)+'box'
    a = bpy.data.meshes.new(name)
    b = bpy.data.objects.new(name, a)
    a.from_pydata([Vector((0.5, 0.5, -0.5)), 
        Vector((0.5, -0.5, -0.5)),
        Vector((-0.5, -0.5, -0.5)),
        Vector((-0.5, 0.5, -0.5)),
        Vector((0.5, 0.5, 0.5)),
        Vector((0.5, -0.5, 0.5)),
        Vector((-0.5, -0.5, 0.5)),
        Vector((-0.5, 0.5, 0.5))],
        [],
        [[0, 1, 2, 3], [4, 7, 6, 5],
        [0, 4, 5, 1], [1, 5, 6, 2],
        [2, 6, 7, 3], [4, 0, 3, 7]])
    a.update(calc_edges=True)
    b.matrix_world.translation = \
        Vector((0,i**2,sqrt(i+0.01)))
    bpy.context.scene.objects.link(b)
    i += 0.1

