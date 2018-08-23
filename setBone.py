import bpy

# カーソルを中央に戻す
def area_of_type(type_name):
    for area in bpy.context.screen.areas:
        if area.type == type_name:
            return area

def get_3d_view():
    return area_of_type('VIEW_3D').spaces[0]

def reset_cursor_location():
    view3d = get_3d_view()
    view3d.pivot_point='CURSOR'
    view3d.cursor_location = (0.0, 0.0, 0.0)

# ボーンを生やす
length = 0.638819
boneCount = 40
bpy.ops.object.armature_add(view_align=False, enter_editmode=True, location=(0, 0, 0))
bpy.ops.transform.translate(value=(0, 0, length-1))

for num in range(0, (boneCount - 1)):
    bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, length), "constraint_axis":(False, False, True), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

# 板ポリ生成
ySubdivisions = boneCount + 1
polyHight = (length * boneCount) / 2
bpy.ops.mesh.primitive_grid_add(x_subdivisions=2, y_subdivisions=ySubdivisions, view_align=False, enter_editmode=False, location=(0, 0, 0))
bpy.context.object.rotation_euler[0] = -1.5708
bpy.context.object.scale[1] = polyHight
bpy.ops.transform.translate(value=(0, 0, polyHight))

reset_cursor_location()
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

bpy.ops.object.mode_set(mode='EDIT', toggle=False)
bpy.ops.uv.smart_project()
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

# スプライン生成
curvedata = bpy.data.curves.new(name="Curve", type='CURVE')
curvedata.dimensions = '3D'
curvedata.resolution_u = 2
spline = curvedata.splines.new('BEZIER')
ob = bpy.data.objects.new("boneSpline", curvedata)
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob
ob.select = True

bpy.ops.object.mode_set(mode='EDIT', toggle=False)

bpy.ops.curve.select_all(action='TOGGLE')

for num in range(0, boneCount):
    bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, length), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

bpy.ops.curve.switch_direction()
bpy.ops.curve.handle_type_set(type='AUTOMATIC')

bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
