#!/usr/bin/env python


from setuptools import setup

import gscholar

setup(name='gscholar',
      version=gscholar.__VERSION__,
      description='Python library to query Google Scholar.',
      long_description='This package provides a python package and CLI to query google scholar and get references in various formats (e.g. bibtex, endnote, etc.)',
      classifiers=[
          'Development Status :: 5 :: Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          ],
      keywords='google scholar cli',
      author='Bastian Venthur',
      author_email='mail@venthur.de',
      url='http://github.com/venthur/gscholar',
      packages=['gscholar'],
      scripts=['bin/gscholar'],
      license='MIT',
)
