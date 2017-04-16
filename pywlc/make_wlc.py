from os.path import dirname, join
from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source('pywlc.wlc',
                      ('#include <wlc/wlc.h>\n'
                       '#include <sys/types.h>\n'
                       '#include <xkbcommon/xkbcommon-keysyms.h>\n'
                       '#include <linux/input-event-codes.h>\n'
                       ),
                      include_dirs=['/home/asandy/devel/wlc/include'],
                      libraries=['wlc'])

cur_dir = dirname(__file__)
with open(join(cur_dir, 'wlc_cdef.h'), 'r') as fileh:
    ffibuilder.cdef(fileh.read())

with open(join(cur_dir, 'extern_cdef.h'), 'r') as fileh:
    ffibuilder.cdef(fileh.read())

with open(join(cur_dir, 'xkb_cdef.h'), 'r') as fileh:
    ffibuilder.cdef(fileh.read())

with open(join(cur_dir, 'input-event-codes_cdef.h'), 'r') as fileh:
    ffibuilder.cdef(fileh.read())
 
if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
