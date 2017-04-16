
extern "Python" void _example_output_resolution(wlc_handle, struct wlc_size *from, struct wlc_size *to);
extern "Python" bool _example_view_created(wlc_handle);
extern "Python" void _example_view_destroyed(wlc_handle);
extern "Python" void _example_view_focus(wlc_handle, bool);
extern "Python" void _example_view_request_move(wlc_handle, struct wlc_point *origin);
extern "Python" void _example_view_request_resize(wlc_handle, uint32_t edges, struct wlc_point *origin);
extern "Python" void _example_view_request_geometry(wlc_handle, struct wlc_geometry *g);
extern "Python" bool _example_keyboard_key(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint32_t, enum wlc_key_state state);
extern "Python" bool _example_pointer_button(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint32_t, enum wlc_button_state state, struct wlc_point *position);

extern "Python" bool _example_pointer_motion(wlc_handle, uint32_t, struct wlc_point *position);
