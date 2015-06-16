#!/usr/bin/env python


from distutils.core import setup

import gscholar

setup(name='gscholar',
      version=gscholar.__VERSION__,
      description='Python library to query Google Scholar.',
      author='Bastian Venthur',
      author_email='mail@venthur.de',
      url='http://github.com/venthur/gscholar',
      packages=['gscholar'],
      license='GPL2',
)
