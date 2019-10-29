import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AX3 model extras",
    version="1.1.0",
    author="Axiacore",
    author_email="info@axiacore.com",
    description="Extras for AX3 models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Axiacore/ax3-model-extras",
    packages=setuptools.find_packages(),
    install_requires=['python-resize-image'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
