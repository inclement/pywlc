
from pywlc.cwlc import ffi, lib
from functools import wraps

NULL = ffi.NULL

def keysym(key):
    name = 'XKB_KEY_{}'.format(key)
    if not hasattr(lib, name):
        raise ValueError('Could not find a keysym for {} ({})'.format(key, name))
    return getattr(lib, name)

def args_to_python(*orig_args):
    def args_to_python_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            args = [(cast(arg) if cast is not None else arg)
                    for cast, arg in zip(orig_args, args)]
            return func(*args)
        return new_func
    return args_to_python_decorator

def returns_to_python(*orig_args):
    def returns_to_python_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            results = func(*args, **kwargs)
            if len(orig_args) == 1:
                results = [results]
            return_value = [(cast(result) if cast is not None else result)
                            for cast, result in zip(orig_args, results)]
            if len(orig_args) == 1:
                return_value = return_value[0]
            return return_value
        return new_func
    return returns_to_python_decorator

def args_to_cffi():
    def args_to_cffi_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            new_args = []
            for arg in args:
                if isinstance(arg, StructWrapper):
                    new_args.append(arg.struct)
                else:
                    new_args.append(arg)
            return func(*new_args)
        return new_func
    return args_to_cffi_decorator


class StructWrapper(object):
    declaration = None
    def __init__(self, struct=None):
        assert self.declaration is not None

        if struct is not None:
            self.struct = struct
        else:
            self.struct = ffi.new(self.declaration)

    def __str__(self):
        return self.string()

    def __repr__(self):
        return self.string()

    def string(self):
        return '<StructWrapper {}>'.format(str(self.struct))

    def copy(self):
        instance = self.__class__()
        for attribute in dir(self.struct):
            setattr(instance, attribute, getattr(self, attribute))


class WlcModifiers(StructWrapper):
    declaration = 'struct wlc_modifiers *'

    @property
    def leds(self):
        return self.struct.leds

    @leds.setter
    def leds(self, value):
        self.struct.leds = value

    @property
    def mods(self):
        return self.struct.mods

    @mods.setter
    def mods(self, value):
        self.struct.mods = value

    @property
    def modifiers(self):
        mods = self.mods
        modifiers = []
        for modifier in ['shift', 'caps', 'ctrl', 'alt',
                         'mod2', 'mod3', 'logo', 'mod5']:
            if getattr(lib, 'WLC_BIT_MOD_{}'.format(modifier.upper())) & mods:
                modifiers.append(modifier)

        return modifiers

    def __contains__(self, item):
        return item in self.modifiers
                       
    def string(self):
        return '<wlc_modifiers {}>'.format(self.modifiers)
        

class WlcPoint(StructWrapper):
    declaration = 'struct wlc_point *'

    @property
    def x(self):
        return self.struct.x

    @x.setter
    def x(self, value):
        self.struct.x = value

    @property
    def y(self):
        return self.struct.y

    @y.setter
    def y(self, value):
        self.struct.y = value

    def string(self):
        return '<wlc_point x={} y={}>'.format(self.x, self.y)
    


class WlcSize(StructWrapper):
    declaration = 'struct wlc_size *'

    @property
    def w(self):
        return self.struct.w

    @w.setter
    def w(self, value):
        self.struct.w = value

    @property
    def h(self):
        return self.struct.h

    @h.setter
    def h(self, value):
        self.struct.h = value

    def string(self):
        return '<wlc_size w={} h={}>'.format(self.w, self.h)

class WlcGeometry(StructWrapper):
    declaration = 'struct wlc_geometry *'

    @property
    def origin(self):
        return WlcPoint(self.struct.origin)

    @origin.setter
    def origin(self, value):
        if isinstance(value, StructWrapper):
            value = value.struct
        self.struct.origin = value

    @property
    def size(self):
        return WlcSize(self.struct.size)

    @size.setter
    def size(self, value):
        if isinstance(value, StructWrapper):
            value = value.struct
        self.struct.size = value

    def string(self):
        return '<wlc_geometry with origin {} and size {}>'.format(self.origin, self.size)

## Callbacks

callbacks = {
    'output_resolution': None,
    }
'''A dict of python callbacks to be used by the C extern functions.'''

@ffi.def_extern()
def _output_resolution(*args):
    callbacks['output_resolution'](*args)

def set_output_resolution_cb(func):
    lib.wlc_set_output_resolution_cb(lib._output_resolution)
    callbacks['output_resolution'] = func

@ffi.def_extern()
def _view_created(*args):
    return callbacks['view_created'](*args)

def set_view_created_cb(func):
    lib.wlc_set_view_created_cb(lib._view_created)
    callbacks['view_created'] = func

@ffi.def_extern()
def _view_destroyed(*args):
    callbacks['view_destroyed'](*args)

def set_view_destroyed_cb(func):
    lib.wlc_set_view_destroyed_cb(lib._view_destroyed)
    callbacks['view_destroyed'] = func

@ffi.def_extern()
def _view_focus(*args):
    print('args', args)
    callbacks['view_focus'](*args)

def set_view_focus_cb(func):
    lib.wlc_set_view_focus_cb(lib._view_focus)
    callbacks['view_focus'] = func

@ffi.def_extern()
def _view_request_move(*args):
    callbacks['view_request_move'](*args)

def set_view_request_move_cb(func):
    lib.wlc_set_view_request_move_cb(lib._view_request_move)
    callbacks['view_request_move'] = func

@ffi.def_extern()
def _view_request_resize(*args):
    callbacks['view_request_resize'](*args)

def set_view_request_resize_cb(func):
    lib.wlc_set_view_request_resize_cb(lib._view_request_resize)
    callbacks['view_request_resize'] = func

@ffi.def_extern()
def _view_request_geometry(*args):
    callbacks['view_request_geometry'](*args)

def set_view_request_geometry_cb(func):
    lib.wlc_set_view_request_geometry_cb(lib._view_request_geometry)
    callbacks['view_request_geometry'] = func

@ffi.def_extern()
@args_to_python(None, None, WlcModifiers, None, None)
def _keyboard_key(*args):
    return callbacks['keyboard_key'](*args)

def set_keyboard_key_cb(func):
    lib.wlc_set_keyboard_key_cb(lib._keyboard_key)
    callbacks['keyboard_key'] = func

@ffi.def_extern()
def _pointer_button(*args):
    return callbacks['pointer_button'](*args)

def set_pointer_button_cb(func):
    lib.wlc_set_pointer_button_cb(lib._pointer_button)
    callbacks['pointer_button'] = func

@ffi.def_extern()
@args_to_python(None, None, WlcPoint)
def _pointer_motion(*args):
    return callbacks['pointer_motion'](*args)

def set_pointer_motion_cb(func):
    lib.wlc_set_pointer_motion_cb(lib._pointer_motion)
    callbacks['pointer_motion'] = func


## API functions

@args_to_cffi()
def pointer_set_position(position):
    lib.wlc_pointer_set_position(position)

@args_to_cffi()
def keyboard_get_keysym_for_key(key, modifiers=None):
    if modifiers is None:
        modifiers = NULL
    return lib.wlc_keyboard_get_keysym_for_key(key, modifiers)

def terminate():
    lib.wlc_terminate()

def exec(name, *args):
    name_arg = ffi.new('char[]', name.encode('utf-8'))
    program_args = [name_arg]
    for arg in args:
        program_args.append(name_arg.encode('utf-8'))
    program_args.append(ffi.NULL)

    lib.wlc_exec(name_arg, program_args)
    
def view_set_mask(view, mask):
    lib.wlc_view_set_mask(view, mask)

def output_get_mask(output):
    return lib.wlc_output_get_mask(output)

def view_bring_to_front(view):
    return lib.wlc_view_bring_to_front(view)

def view_focus(view):
    return lib.wlc_view_focus(view)

def view_get_output(view):
    return lib.wlc_view_get_output(view)

@returns_to_python(WlcSize)
def output_get_virtual_resolution(output):
    return lib.wlc_output_get_virtual_resolution(output)

def view_set_state(view, state, toggle):
    lib.wlc_view_set_state(view, state, toggle)

def output_get_views(output):
    # Original function takes argument 'memb', which is just a pointer
    memb = ffi.new('size_t *')
    views = lib.wlc_output_get_views(output, memb)

    return views, memb[0]
    

def view_positioner_get_anchor_rect(view):
    return lib.wlc_view_positioner_get_anchor_rect(view)

@args_to_cffi()
def view_set_geometry(view, edges, geometry):
    print('geometry is', geometry, geometry.origin, geometry.size, geometry.origin.x, geometry.origin.y, geometry.size.w, geometry.size.h)
    return lib.wlc_view_set_geometry(view, edges, geometry)

@returns_to_python(WlcSize)
def view_positioner_get_size(view):
    return lib.wlc_view_positioner_get_size(view)

@returns_to_python(WlcGeometry)
def view_get_geometry(view):
    return lib.wlc_view_get_geometry(view)

def view_get_parent(view):
    return lib.wlc_view_get_parent(view)

def view_close(view):
    return lib.wlc_view_close(view)
