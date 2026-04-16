"""
Dr Octopus 手臂组装脚本
直接使用本地变换（不叠加父装配体变换）
两个子装配体共享同一坐标系
"""

import bpy
import json
import os
from mathutils import Matrix, Euler, Vector
import math

BASE_PATH = "/home/arenalabs/Desktop/Gen2Humanoid/dr_octopus_ws"
MESH_PATH = os.path.join(BASE_PATH, "meshes_from_step")
ASSEMBLY_JSON = os.path.join(BASE_PATH, "assembly_params.json")
OUTPUT_PATH = os.path.join(BASE_PATH, "dr_octopus_assembled.blend")

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for m in bpy.data.meshes:
        bpy.data.meshes.remove(m)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def make_matrix(xyz_mm, rpy_rad):
    loc = Vector([x / 1000.0 for x in xyz_mm])
    rot = Euler(rpy_rad, 'XYZ')
    return Matrix.Translation(loc) @ rot.to_matrix().to_4x4()

def set_material(obj, color, name):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def import_stl(filepath, name):
    bpy.ops.wm.stl_import(filepath=filepath)
    obj = bpy.context.active_object
    if obj:
        obj.name = name
    return obj

def assemble():
    clear_scene()

    with open(ASSEMBLY_JSON) as f:
        params = json.load(f)

    stl_map = {
        "L0R": ("L0R.stl", (0.9, 0.9, 0.9, 1), "Link0_Base"),
        "L1R": ("L1R.stl", (0.7, 0.7, 0.7, 1), "Link1"),
        "L2R": ("L2R.stl", (0.85, 0.85, 0.85, 1), "Link2"),
    }

    arm1_links = {
        "L3":  ("L3.stl",  (0.2, 0.4, 0.8, 1), "Link3_Prime"),
        "L41": ("L41.stl", (1.0, 0.5, 0.0, 1), "Link4_Prime_LBracket"),
    }

    arm2_links = {
        "L3":  ("L3_2.stl", (0.2, 0.6, 0.9, 1), "Link3"),
        "L4":  ("L4.stl",   (0.6, 0.6, 0.6, 1), "Link4"),
        "L5R": ("L5R.stl",  (0.85, 0.85, 0.85, 1), "Link5"),
        "L6R": ("L6R.stl",  (0.7, 0.7, 0.7, 1), "Link6"),
        "L7R": ("L7R.stl",  (0.9, 0.9, 0.9, 1), "Link7"),
    }

    imported = []

    for item in params:
        name = item["name"]
        parent = item.get("parent")
        t = item.get("transform", {})
        xyz = t.get("xyz_mm", [0, 0, 0])
        rpy = t.get("rpy_rad", [0, 0, 0])

        stl_file = None
        color = None
        label = None

        if parent == "右臂" and name in stl_map:
            stl_file, color, label = stl_map[name]
        elif parent == "右臂" and name in arm1_links:
            stl_file, color, label = arm1_links[name]
        elif parent == "右臂 - 副本" and name in arm2_links:
            stl_file, color, label = arm2_links[name]
        else:
            continue

        filepath = os.path.join(MESH_PATH, stl_file)
        if not os.path.exists(filepath):
            print(f"SKIP {name}: file not found {stl_file}")
            continue

        obj = import_stl(filepath, label)
        if not obj:
            continue

        local_mat = make_matrix(xyz, rpy)
        obj.matrix_world = local_mat

        set_material(obj, color, f"mat_{label}")

        imported.append(label)
        print(f"OK {label} @ xyz={[round(x,1) for x in xyz]} rpy_deg={[round(math.degrees(r),1) for r in rpy]}")

    # Add EE from sub-assembly if available
    ee_path = os.path.join(MESH_PATH, "EE_Sub_Assembly_RB1 - 副本.stl")
    if os.path.exists(ee_path):
        for item in params:
            if "EE_Sub_Assembly" in item.get("name", "") and item.get("parent") == "L7R":
                t = item["transform"]
                obj = import_stl(ee_path, "EE_Assembly")
                if obj:
                    obj.matrix_world = make_matrix(t["xyz_mm"], t["rpy_rad"])
                    set_material(obj, (0.3, 0.8, 0.3, 1), "mat_EE")
                    imported.append("EE_Assembly")
                    print(f"OK EE_Assembly")
                break

    print(f"\n=== Imported {len(imported)} objects ===")

    bpy.ops.object.select_all(action='SELECT')

    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    assemble()
