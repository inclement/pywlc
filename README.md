
pywlc
====

Python bindings for [wlc](https://github.com/Cloudef/wlc), using cffi.

pywlc currently provides just a thin wrapper, rather than full
Pythonic wrappers for each function. It has been tested only with
Python 3, but it might work with Python 2.

Install
-------

You must first install [wlc](https://github.com/Cloudef/wlc), then
install pywlc as a normal python module:

    $ python3 setup.py install

Example
-------

Basic usage:

    >>> from pywlc import lib, ffi

    >>> lib.wlc_init()
    
    >>> lib.wlc_run()  # starts wlc (but with no extra behaviour)
    
Access wlc functions using the `lib` object. It wraps all the
functions in `wlc.h`, plus some other wlc data structures. Other
instructions for working with `lib` and `ffi` can be found in
the
[cffi documentation](http://cffi.readthedocs.io/en/latest/using.html).

An example window manager using these bindings is provided at
`pywlc/example.py`. It is a clone of the C example from
the
[wlc repository](https://github.com/Cloudef/wlc/blob/master/example/example.c),
and can be run from inside an X session (where it will appear as a new
window).

    $ python3 pywlc/example.py

If you install pywlc with `python3 setup.py install`, you can run the
example window manager with 

    $ pywlc-example
