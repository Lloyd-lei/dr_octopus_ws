"""
用全局坐标 STL 组装 - 所有 mesh 直接放在原点
"""
import bpy
import os
from mathutils import Vector

MESH_DIR = "/home/arenalabs/Desktop/Gen2Humanoid/dr_octopus_ws/meshes_global"
OUTPUT = "/home/arenalabs/Desktop/Gen2Humanoid/dr_octopus_ws/dr_octopus_assembled.blend"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in bpy.data.meshes:
    bpy.data.meshes.remove(m)

links = [
    ("L0R.stl", "Link0", (0.9, 0.9, 0.9, 1)),
    ("L1R.stl", "Link1", (0.75, 0.75, 0.75, 1)),
    ("L2R.stl", "Link2", (0.85, 0.85, 0.85, 1)),
    ("L3.stl", "Link3_Prime", (0.2, 0.4, 0.8, 1)),
    ("L41.stl", "Link4_Prime_LBracket", (1.0, 0.5, 0.0, 1)),
    ("L3_part2.stl", "Link3", (0.3, 0.5, 0.9, 1)),
    ("L4.stl", "Link4", (0.65, 0.65, 0.65, 1)),
    ("L5R.stl", "Link5", (0.85, 0.85, 0.85, 1)),
    ("L6R.stl", "Link6", (0.75, 0.75, 0.75, 1)),
    ("L7R.stl", "Link7", (0.9, 0.9, 0.9, 1)),
    ("EE_Sub_Assembly^RB1 - 副本.stl", "EE", (0.3, 0.8, 0.3, 1)),
]

count = 0
for stl_file, name, color in links:
    path = os.path.join(MESH_DIR, stl_file)
    if not os.path.exists(path):
        print(f"SKIP {name}: {stl_file}")
        continue
    
    bpy.ops.wm.stl_import(filepath=path)
    obj = bpy.context.active_object
    obj.name = name
    
    # STL is in mm, scale to m
    obj.scale = (0.001, 0.001, 0.001)
    bpy.ops.object.transform_apply(scale=True)
    
    mat = bpy.data.materials.new(name=f"mat_{name}")
    mat.diffuse_color = color
    obj.data.materials.append(mat)
    
    count += 1
    print(f"OK {name}")

# Center view
bpy.ops.object.select_all(action='SELECT')

# Add light
bpy.ops.object.light_add(type='SUN', location=(2, -2, 3))
bpy.context.active_object.data.energy = 3

bpy.ops.wm.save_as_mainfile(filepath=OUTPUT)
print(f"\nDONE: {count} objects saved to {OUTPUT}")
