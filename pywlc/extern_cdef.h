
extern "Python" void output_resolution(wlc_handle, struct wlc_size *from, struct wlc_size *to);
extern "Python" bool view_created(wlc_handle);
extern "Python" void view_destroyed(wlc_handle);
extern "Python" void view_focus(wlc_handle, bool);
extern "Python" void view_request_move(wlc_handle, struct wlc_point *origin);
extern "Python" void view_request_resize(wlc_handle, uint32_t edges, struct wlc_point *origin);
extern "Python" void view_request_geometry(wlc_handle, struct wlc_geometry *g);
extern "Python" bool keyboard_key(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint32_t, enum wlc_key_state state);
extern "Python" bool pointer_button(wlc_handle, uint32_t, struct wlc_modifiers *modifiers, uint32_t, enum wlc_button_state state, struct wlc_point *position);

extern "Python" bool pointer_motion(wlc_handle, uint32_t, struct wlc_point *position);
