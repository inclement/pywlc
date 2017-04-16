
pywlc
====

Python bindings for [wlc](https://github.com/Cloudef/wlc), using cffi.

pywlc has been tested only with Python 3, but it might work with Python 2.

Install
-------

You must first install [wlc](https://github.com/Cloudef/wlc), then
install pywlc as a normal python module:

    $ python3 setup.py install

Example
-------

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
