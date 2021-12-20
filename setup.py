import os

import setuptools

__VERSION__ = '1.4.4'

with open('README.md', 'r') as fh:
    long_description = fh.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='AX3 model extras',
    version=__VERSION__,
    author='Axiacore',
    author_email='info@axiacore.com',
    description='Django app extras for AX3 models',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Axiacore/ax3-model-extras',
    packages=setuptools.find_packages(),
    install_requires=[
        'django >= 3.2',
        'python-resize-image',
        'python_magic'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
