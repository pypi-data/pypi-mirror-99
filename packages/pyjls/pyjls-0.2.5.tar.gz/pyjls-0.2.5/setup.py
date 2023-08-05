#!/usr/bin/env python3
# Copyright 2018-2021 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Joulescope file format python setuptools module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
import setuptools
import setuptools.dist
import distutils.cmd
from distutils.errors import DistutilsExecError
import os
import platform
import sys

if platform.system() == 'Windows':
    numpy_req = 'numpy>=1.20'
else:
    numpy_req = 'numpy>=1.16'

setuptools.dist.Distribution().fetch_build_eggs(['Cython>=0.29.3', numpy_req])

import numpy as np


MYPATH = os.path.dirname(os.path.abspath(__file__))
VERSION_PATH = os.path.join(MYPATH, 'pyjls', 'version.py')


try:
    from Cython.Build import cythonize
    USE_CYTHON = os.path.isfile(os.path.join(MYPATH, 'pyjls', 'binding.pyx'))
except ImportError:
    USE_CYTHON = False


about = {}
with open(VERSION_PATH, 'r', encoding='utf-8') as f:
    exec(f.read(), about)


if platform.system() == 'Windows':
    sources = ['src/backend_win.c', 'src/crc32c_intel_sse4.c']
    libraries = []
    extra_compile_args = []
elif 'armv7' in platform.machine():
    sources = ['src/backend_posix.c', 'src/crc32c_sw.c']
    libraries = ['pthread', 'm']
    extra_compile_args = []
elif platform.processor() == 'aarch64' or platform.machine() == 'arm64':
    sources = ['src/backend_posix.c', 'src/crc32c_arm_neon.c']
    libraries = ['pthread', 'm']
    extra_compile_args = ['-march=armv8-a+crc+simd']
else:
    sources = ['src/backend_posix.c', 'src/crc32c_intel_sse4.c']
    libraries = ['pthread', 'm']
    extra_compile_args = ['-msse4']


ext = '.pyx' if USE_CYTHON else '.c'
extensions = [
    setuptools.Extension('pyjls.binding',
        sources=[
            'pyjls/binding' + ext,
            'src/ec.c',
            'src/log.c',
            'src/msg_ring_buffer.c',
            'src/raw.c',
            'src/reader.c',
            'src/statistics.c',
            'src/threaded_writer.c',
            'src/wf_f32.c',
            'src/writer.c',
        ] + sources,
        include_dirs=['include', 'include_prv', np.get_include()],
        libraries = libraries,
        extra_compile_args=[] + extra_compile_args,
    ),
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions, compiler_directives={'language_level': '3'})  # , annotate=True)


# Get the long description from the README file
with open(os.path.join(MYPATH, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()


if sys.platform.startswith('win'):
    PLATFORM_INSTALL_REQUIRES = ['pypiwin32>=223']
else:
    PLATFORM_INSTALL_REQUIRES = []


class CustomBuildDocs(distutils.cmd.Command):
    """Custom command to build docs locally."""

    description = 'Build docs.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # sphinx-build -b html docs build\docs_html
        # defer import so not all setups require sphinx
        from sphinx.application import Sphinx
        from sphinx.util.console import nocolor, color_terminal
        nocolor()
        source_dir = os.path.join(MYPATH, 'docs')
        target_dir = os.path.join(MYPATH, 'build', 'docs_html')
        doctree_dir = os.path.join(target_dir, '.doctree')
        app = Sphinx(source_dir, source_dir, target_dir, doctree_dir, 'html')
        app.build()
        if app.statuscode:
            raise DistutilsExecError(
                'caused by %s builder.' % app.builder.name)


setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Operating systems
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',

        # Supported Python versions
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        
        # Topics
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Utilities',
    ],

    keywords='JLS,Joulescope',

    packages=setuptools.find_packages(exclude=['native', 'docs', 'test', 'dist', 'build']),
    ext_modules=extensions,
    cmdclass={
        'docs': CustomBuildDocs,
    },
    include_dirs=[],
    
    # See https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='~=3.7',

    setup_requires=[
        # https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html
        numpy_req,
        'Cython>=0.29.3',
    ],

    # See https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        numpy_req,
    ] + PLATFORM_INSTALL_REQUIRES,

    extras_require={
        'dev': ['check-manifest', 'coverage', 'Cython', 'wheel', 'sphinx', 'm2r'],
    },   

    entry_points={
        'console_scripts': [
            'pyjls=pyjls.__main__:run',
        ],
    },
    
    project_urls={
        'Bug Reports': 'https://github.com/jetperch/jls/issues',
        'Funding': 'https://www.joulescope.com',
        'Twitter': 'https://twitter.com/joulescope',
        'Source': 'https://github.com/jetperch/jls/',
    },
)
