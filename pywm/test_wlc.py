
from wlc import lib

print(lib.WLC_LOG_WAYLAND)

print(lib.WLC_EVENT_HANGUP, 0x04)

print(lib.WLC_BIT_FULLSCREEN, 1<<1)

print(lib.WLC_BIT_MODAL, 1<<3)

print(lib.WLC_BIT_PROPERTY_PID, 1<<3)

print(lib.WLC_RESIZE_EDGE_LEFT, 4)

print(lib.WLC_BUTTON_STATE_PRESSED, 1)

print(lib.wlc_pointer_get_position)

print(lib.wlc_pointer_set_position)

print(lib.wlc_set_output_resolution_cb)
