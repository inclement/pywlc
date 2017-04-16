from __future__ import division, print_function
from wlc import ffi, lib

from collections import namedtuple

class Compositor:
    view = None
    grab = None
    edges = None

compositor = Compositor()
'''Global object to hold details of any view that is currently being
updated.'''

def relayout(output):
    print('RELAYOUT')
    size = lib.wlc_output_get_virtual_resolution(output)
    print('size is', size)

    memb = ffi.new('size_t *')
    views = lib.wlc_output_get_views(output, memb)
    print('memb is', memb[0])

    positioned = 0
    for i in range(0, memb[0]):
        if lib.wlc_view_positioner_get_anchor_rect(views[i]) == ffi.NULL:
            positioned += 1

    toggle = 0
    y = 0

    n = max((1 + positioned) // 2, 1)
    w = size.w // 2
    h = size.h // n
    ew = size.w - w * 2
    eh = size.h - h * n
    j = 0

    print('w', w, 'h', h, 'ew', ew, 'eh', eh)

    for i in range(0, memb[0]):
        anchor_rect = lib.wlc_view_positioner_get_anchor_rect(views[i])
        print('anchor rect is', anchor_rect, anchor_rect == ffi.NULL)
        if anchor_rect == ffi.NULL:
            g = ffi.new('struct wlc_geometry *')
            g.origin.x = w + ew if toggle else 0
            g.origin.y = y
            g.size.w = size.w if ((1 - toggle) and j == positioned - 1) else (w if toggle else w + ew)
            g.size.h = h + eh if j < 2 else h

            lib.wlc_view_set_geometry(views[i], 0, g)
            toggle = 1 - toggle
            y = y + (g.size.h if not toggle else 0)
            j += 1

        else:
            size_req = lib.wlc_view_positioner_get_size(views[i])[0]
            if size_req.w <= 0 or size_req.h <= 0:
                current = lib.wlc_view_get_geometry(views[i])
                size_req = current.size

            g = ffi.new('struct wlc_geometry *')
            g.origin = anchor_rect.origin
            g.size = size_req

            parent = lib.wlc_view_get_parent(views[i])

            if parent:
                parent_geometry = lib.wlc_view_get_geometry(parent)
                g.origin.x += parent_geometry.origin.x
                g.origin.y += parent_geometry.origin.y

            lib.wlc_view_set_geometry(views[i], 0, g)
            print('second condition happened')
            
    

def get_topmost(output, offset):
    memb = ffi.new('size_t *')
    views = lib.wlc_output_get_views(output, memb)
    if memb[0] > 0:
        return views[(memb[0] - 1 + offset) % memb[0]]
    return 0

def start_interactive_move(view, origin):
    start_interactive_action(view, origin)

def start_interactive_action(view, origin):
    if compositor.view:
        return False
    compositor.view = view
    grab = ffi.new('struct wlc_point *')
    grab.x = origin.x
    grab.y = origin.y
    compositor.grab = grab
    lib.wlc_view_bring_to_front(view)
    return True

def start_interactive_resize(view, edges, origin):
    g = lib.wlc_view_get_geometry(view)
    print('g is', g)
    if not g or not start_interactive_action(view, origin):
        return

    halfw = g.origin.x + g.size.w / 2.
    halfh = g.origin.y + g.size.h / 2.

    compositor.edges = edges
    if edges != 0:
        compositor.edges = (lib.WLC_RESIZE_EDGE_LEFT if origin.x < halfw else (lib.WLC_RESIZE_EDGE_RIGHT if origin.x > halfw else 0)) | (lib.WLC_RESIZE_EDGE_TOP if origin.y < halfh else (lib.WLC_RESIZE_EDGE_BOTTOM if origin.y > halfh else 0))

    lib.wlc_view_set_state(view, lib.WLC_BIT_RESIZING, 1)


def stop_interactive_action():
    if compositor.view is None:
        return

    lib.wlc_view_set_state(compositor.view, lib.WLC_BIT_RESIZING, 0)

    compositor.view = None
    compositor.grab = None
    compositor.edges = None

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
    start_interactive_move(view, origin)

@ffi.def_extern()
def view_request_resize(view, edges, origin):
    print('view_request_resize')
    start_interactive_resize(view, edges, origin)

@ffi.def_extern()
def view_request_geometry(view, geometry):
    print('view_request_geometry')
    # intentionally blank in example.c

@ffi.def_extern()
def keyboard_key(view, time, modifiers, key, state):
    print('keyboard_key', view, time, modifiers, key, state)

    sym = lib.wlc_keyboard_get_keysym_for_key(key, ffi.NULL)
    print('sym', sym)

    if view:
        pass

    if (modifiers.mods & lib.WLC_BIT_MOD_CTRL):
        if sym == lib.XKB_KEY_Escape and state == lib.WLC_KEY_STATE_PRESSED:
            lib.wlc_terminate()
            return 1
        elif sym == lib.XKB_KEY_Return and state == lib.WLC_KEY_STATE_PRESSED:
            weston_terminal = ffi.new('char[]', b'weston-terminal')
            args = ffi.new('char * []', [weston_terminal, ffi.NULL])
            lib.wlc_exec(weston_terminal, args)
            # lib.wlc_exec(weston_terminal, ffi.NULL)
            print('execd weston-terminal')
            return 1

        if sym >= lib.XKB_KEY_1 and sym <= lib.XKB_KEY_9:
            if state == lib.WLC_KEY_STATE_PRESSED:
                print('ctrl + number in 1-9')

    return 0

@ffi.def_extern()
def pointer_button(view, time, modifiers, button, state, position):
    print('pointer_button', view, time, modifiers, button, state, position)
    lib.wlc_pointer_set_position(position)

    if state == lib.WLC_BUTTON_STATE_PRESSED:
        lib.wlc_view_focus(view)

        print('button position', position.x, position.y)
        if view is not None:
            if (modifiers.mods & lib.WLC_BIT_MOD_CTRL) and button == lib.BTN_LEFT:
                start_interactive_move(view, position)
            if (modifiers.mods & lib.WLC_BIT_MOD_CTRL) and button == lib.BTN_RIGHT:
                start_interactive_resize(view, 0, position)

    else:
        stop_interactive_action()

    print('compositor.view is', compositor.view)
    if compositor.view is not None:
        return 1

    return 0

@ffi.def_extern()
def pointer_motion(handle, time, position):
    # print('pointer_motion', handle, time, position)
    if compositor.view is not None:
        print('moving', position.x, position.y, compositor.grab.x, compositor.grab.y, compositor.grab.x, compositor.grab.y)
        dx = position.x - compositor.grab.x
        dy = position.y - compositor.grab.y
        g = lib.wlc_view_get_geometry(compositor.view)

        if compositor.edges is not None:
            mins = (80, 40)
            
            
        else:
            print('dx is', dx)
            print('dy is', dy)
            g.origin.x += dx
            g.origin.y += dy
            lib.wlc_view_set_geometry(compositor.view, 0, g)

        compositor.grab.x = position.x
        compositor.grab.y = position.y
            

    lib.wlc_pointer_set_position(position)
    return 1 if compositor.view is not None else 0

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
