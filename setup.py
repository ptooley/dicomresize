#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='dicomresize',
      version='0.1',
      description='Routines for resizing dicom images',
      author='Phil Tooley, INSIGNEO',
      author_email='phil.tooley@sheffield.ac.uk',
      url='insigneo.org',
      packages=find_packages('.'),
      install_requires=['numpy', 'pydicom'],
      entry_points={
          'console_scripts' : [
              'dicomresize = dicomresize.dicomresize:dicomresize',
          ],
          'gui_scripts' : []})
