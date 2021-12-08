#!/usr/bin/env python


from setuptools import setup


meta = {}
exec(open('./gscholar/version.py').read(), meta)
meta['long_description'] = open('./README.md').read()


setup(
    name='gscholar',
    version=meta["__VERSION__"],
    description='Python library to query Google Scholar.',
    long_description=meta['long_description'],
    long_description_content_type='text/markdown',
    keywords='google scholar cli',
    author='Bastian Venthur',
    author_email='mail@venthur.de',
    url='https://github.com/venthur/gscholar',
    project_urls={
        'Source': 'https://github.com/venthur/gscholar',
        'Changelog':
            'https://github.com/venthur/gscholar/blob/master/CHANGELOG.md',
    },
    python_requires='>=3.6',
    packages=['gscholar'],
    entry_points={
        'console_scripts': [
            'gscholar = gscholar.__main__:main'
        ]
    },
    license='MIT',
)
