
from wlc import ffi, lib

from collections import namedtuple

Compositor = namedtuple('Compositor', ['view', 'grab', 'edges'])
compositor = Compositor(None, None, None)

def relayout(output):
    size = lib.wlc_output_get_virtual_resolution(output)
    print('size is', size)

    memb = ffi.new('size_t *')
    views = lib.wlc_output_get_views(output, memb)
    print('memb is', memb[0])

    positioned = 0
    for i in range(0, memb[0]):
        print(lib.wlc_view_positioner_get_anchor_rect(views[i]))
        positioned += 1

    toggle = False

    y = 0
    
    print('RELAYOUT')

def get_topmost(output, offset):
    memb = ffi.new('size_t *')
    views = lib.wlc_output_get_views(output, memb)
    if memb[0] > 0:
        return views[(memb - 1 + offset) % memb]
    return 0

@ffi.def_extern()
def output_resolution(output, from_size, to_size):
    print('output_resolution', output, from_size, to_size)
    relayout(output)
    
@ffi.def_extern()
def view_created(view):
    print('view_created', view)
    lib.wlc_view_set_mask(view, lib.wlc_output_get_mask(lib.wlc_view_get_output(view)))
    lib.wlc_view_bring_to_front(view)
    lib.wlc_view_focus(view)
    relayout(lib.wlc_view_get_output(view))
    return 1

@ffi.def_extern()
def view_destroyed(view):
    print('view_destroyed', view)
    lib.wlc_view_focus(get_topmost(lib.wlc_view_get_output(view), 0))
    relayout(lib.wlc_view_get_output(view))

@ffi.def_extern()
def view_focus(view, focus):
    print('view_focus', view, focus)

    lib.wlc_view_set_state(view, lib.WLC_BIT_ACTIVATED, focus)

@ffi.def_extern()
def view_request_move(view, origin):
    print('view_request_move')

@ffi.def_extern()
def view_request_resize(view, edges, origin):
    print('view_request_resize')

@ffi.def_extern()
def view_request_geometry(view, geometry):
    print('view_request_geometry')

@ffi.def_extern()
def keyboard_key(view, time, modifiers, key, state):
    print('keyboard_key', view, time, modifiers, key, state)
    weston_terminal = ffi.new('char[]', b'weston-terminal')
    if key == 28:
        lib.wlc_exec(weston_terminal, ffi.NULL)
    return 0

@ffi.def_extern()
def pointer_button(handle, time, modifiers, button, state, position):
    print('pointer_button', handle, time, modifiers, button, state, position)
    lib.wlc_pointer_set_position(position)

    return 0  # return 1 to prevent sending event to clients

@ffi.def_extern()
def pointer_motion(handle, time, position):
    # print('pointer_motion', handle, time, position)
    lib.wlc_pointer_set_position(position)

    return 0  # return 1 to prevent sending event to clients

lib.wlc_set_output_resolution_cb(lib.output_resolution)
lib.wlc_set_view_created_cb(lib.view_created)
lib.wlc_set_view_destroyed_cb(lib.view_destroyed)
lib.wlc_set_view_focus_cb(lib.view_focus)
lib.wlc_set_view_request_move_cb(lib.view_request_move)
lib.wlc_set_view_request_resize_cb(lib.view_request_resize)
lib.wlc_set_view_request_geometry_cb(lib.view_request_geometry)
lib.wlc_set_keyboard_key_cb(lib.keyboard_key)
lib.wlc_set_pointer_button_cb(lib.pointer_button)
lib.wlc_set_pointer_motion_cb(lib.pointer_motion)

if lib.wlc_init() != 1:
    exit(1)

lib.wlc_run()
