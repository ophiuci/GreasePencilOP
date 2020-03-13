bl_info = {
    "name": "Grease Pencil Ophiuci",
    "blender": (2, 80, 0),
    "category": "3D View",
}

import bpy

class GreasePencilCursorMover(bpy.types.Operator):
    bl_idname = "view_3d.gpencil_cursor_mover"
    bl_label = "Grease Pencil Cursor Mover"
    bl_options = {'REGISTER'}

    trigger_modal: bpy.props.BoolProperty(name="Trigger Modal", default=False)
    total: bpy.props.IntProperty(name="Total", default=4)

    def modal(self, context, event):
        if(self.trigger_modal):
            print("Modal" + str(event.mouse_region_x) + " " + str(event.mouse_region_y))
            self.trigger_modal = False

            # Exit draw mode, go to edit mode
            bpy.ops.gpencil.paintmode_toggle()
            bpy.ops.gpencil.editmode_toggle()

            # Change to select grease pencil points
            bpy.context.scene.tool_settings.gpencil_selectmode_edit = 'POINT'

            bpy.ops.gpencil.select_circle(x=event.mouse_region_x, y=event.mouse_region_y, radius=15, wait_for_input=False)

            # Snap cursor to selected points
            bpy.ops.gpencil.snap_cursor_to_selected()

            # Exit edit mode, go to grease pencil mode
            bpy.ops.gpencil.editmode_toggle()
            bpy.ops.gpencil.paintmode_toggle()
            return {'FINISHED'}

    def execute(self, context):
        self.trigger_modal = True
        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

addon_keymaps = []

def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type='VIEW_3D', region_type='WINDOW', modal=False)
        kmi = km.keymap_items.new(GreasePencilCursorMover.bl_idname, "F5", "PRESS", ctrl=False, shift=False)
        addon_keymaps.append((km, kmi))
    bpy.utils.register_class(GreasePencilCursorMover)

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(GreasePencilCursorMover)

if __name__ == "__main__":
    register()