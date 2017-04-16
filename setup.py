
from setuptools import setup, find_packages
from os import walk
from os.path import join, dirname, sep
import os
import glob

packages = find_packages()

package_data = {'pywlc': ['*.py',
                          '*_cdef.h',
                          'wlc.c'], }

data_files = []

setup(name='pywlc',
      version='0.1',
      description='Python cffi wrapper for wlc (a Wayland compositor library)',
      author='Alexander Taylor',
      author_email='alexanderjohntaylor@gmail.com',
      url='https://github.com/inclement/pywlc', 
      license='MIT', 
      install_requires=['cffi>=1.0.0'],
      cffi_modules=['pywlc/make_wlc.py:ffibuilder'],
      entry_points={
          'console_scripts': [
              'pywlc-example = pywlc.example:main'
              ],
          },
      packages=packages,
      package_data=package_data,
      )
