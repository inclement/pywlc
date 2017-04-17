
from pywlc.cwlc import ffi, lib
from functools import wraps

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
    def cast_returns_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            results = func(*args, **kwargs)
            return [(cast(result) if cast is not None else result)
                    for cast, result in zip(orig_args, results)]
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

    def copy(self):
        instance = self.__class__()
        for attribute in dir(self.struct):
            setattr(instance, attribute, getattr(self, attribute))

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
    print('position is', position)
    lib.wlc_pointer_set_position(position)
