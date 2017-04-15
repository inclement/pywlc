
from wlc import ffi, lib

print(lib)

print('checking required functions exist')

print(lib.wlc_view_set_mask)
print(lib.wlc_output_get_mask)
print(lib.wlc_view_bring_to_front)
print(lib.wlc_view_focus)
print(lib.wlc_view_set_state)
print(lib.wlc_set_view_created_cb)
print(lib.wlc_set_view_focus_cb)


@ffi.def_extern()
def view_created(view):
    print('view created!')
    print(view)
    lib.wlc_view_set_mask(view, lib.wlc_output_get_mask(lib.wlc_view_get_output(view)))
    lib.wlc_view_focus(view)
    return 1

@ffi.def_extern()
def view_focus(view, focus):
    print('view focus!')
    print(view, focus)

    lib.wlc_view_set_state(view, lib.WLC_BIT_ACTIVATED, focus)


lib.wlc_set_view_created_cb(lib.view_created)
lib.wlc_set_view_focus_cb(lib.view_focus)

if lib.wlc_init() != 1:
    exit(1)

lib.wlc_run()
