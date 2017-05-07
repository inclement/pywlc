
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


extern "Python" bool _output_created(wlc_handle);
extern "Python" void _output_destroyed(wlc_handle);
extern "Python" void _output_focus(wlc_handle, bool);
extern "Python" void _output_resolution(wlc_handle, struct wlc_size *from, struct wlc_size *to);
extern "Python" void _output_render_pre(wlc_handle);
extern "Python" void _output_render_post(wlc_handle);
extern "Python" void _output_context_created(wlc_handle);
extern "Python" void _output_context_destroyed(wlc_handle);
extern "Python" bool _view_created(wlc_handle);
extern "Python" void _view_destroyed(wlc_handle);
extern "Python" void _view_focus(wlc_handle, bool);
extern "Python" void _view_move_to_output(wlc_handle, wlc_handle, wlc_handle);
extern "Python" void _view_request_geometry(wlc_handle, struct wlc_geometry *g);
extern "Python" void _view_request_state(wlc_handle, enum wlc_view_state_bit, bool);
extern "Python" void _view_request_move(wlc_handle, struct wlc_point *origin);
extern "Python" void _view_request_resize(wlc_handle, uint32_t edges, struct wlc_point *origin);
extern "Python" void _view_render_pre(wlc_handle);
extern "Python" void _view_render_post(wlc_handle);
extern "Python" void _view_properties_updated(wlc_handle, uint32_t);
extern "Python" bool _keyboard_key(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint32_t, enum wlc_key_state state);
extern "Python" bool _pointer_button(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint32_t, enum wlc_button_state state, struct wlc_point *position);
extern "Python" bool _pointer_scroll(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint8_t, double amount[2]);
extern "Python" bool _pointer_motion(wlc_handle, uint32_t, struct wlc_point *position);
extern "Python" bool _touch(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, enum wlc_touch_type, int32_t, struct wlc_point*);
extern "Python" void _compositor_ready();
extern "Python" void _compositor_terminate();
