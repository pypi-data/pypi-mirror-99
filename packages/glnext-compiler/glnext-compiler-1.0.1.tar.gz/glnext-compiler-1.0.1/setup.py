import os
import sys

from setuptools import Extension, setup

define_macros = [
    ('PY_SSIZE_T_CLEAN', None),
]

extra_compile_args = []
include_dirs = []
library_dirs = []
libraries = []

if sys.platform == 'win32':
    sdk = os.getenv('VULKAN_SDK')
    if sdk is None:
        sdk = os.path.join('C:\\VulkanSDK\\', os.listdir('C:\\VulkanSDK\\')[0])
    include_dirs.append(os.path.join(sdk, 'Include'))
    library_dirs.append(os.path.join(sdk, 'Lib'))
    libraries.append('shaderc_combined')

if sys.platform == 'linux':
    extra_compile_args.append('-fpermissive')
    libraries.append('shaderc_combined')

glnext_compiler = Extension(
    name='glnext_compiler',
    sources=['./glnext_compiler.cpp'],
    define_macros=define_macros,
    extra_compile_args=extra_compile_args,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
)

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='glnext-compiler',
    version='1.0.1',
    ext_modules=[glnext_compiler],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/glnext/glnext-compiler/',
    author='Szabolcs Dombi',
    author_email='cprogrammer1994@gmail.com',
    license='MIT',
)
