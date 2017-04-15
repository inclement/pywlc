
from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source('wlc',
                      ('#include <wlc/wlc.h>\n'
                       '#include <sys/types.h>\n'),
                      include_dirs=['/home/asandy/devel/wlc/include'],
                      libraries=['wlc'])

with open('wlc_cdef.h', 'r') as fileh:
    ffibuilder.cdef(fileh.read())

with open('extern_cdef.h', 'r') as fileh:
    ffibuilder.cdef(fileh.read())
 
ffibuilder.compile(verbose=True)
