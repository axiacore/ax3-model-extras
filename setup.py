import os

import setuptools

__VERSION__ = '2.0.1'

with open('README.md') as fh:
    long_description = fh.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='ax3-model-extras',
    version=__VERSION__,
    author='Axiacore',
    author_email='info@axiacore.com',
    description='Django app extras for AX3 models',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/axiacore/ax3-model-extras',
    packages=setuptools.find_packages(),
    install_requires=[
        'django >= 3.2',
        'python-resize-image',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
