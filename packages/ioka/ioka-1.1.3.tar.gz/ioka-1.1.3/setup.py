import re

from setuptools import setup
from io import open

VERSION = "1.1.3"

long_description = open('README.rst', 'rt', encoding='utf8').read()

# PyPI can't process links with anchors
long_description = re.sub(r'<(.*)#.*>`_', '<\g<1>>`_', long_description)

# This call to setup() does all the work
setup(
    name="ioka",
    packages=["ioka"],

    version=VERSION,

    description="IOKA Asynchronous Python Client Library",
    long_description_content_type="text/x-rst",
    long_description=long_description,

    url="https://github.com/mortilele/ioka-python-sdk",

    author="Alik Akhmetov",
    author_email="ali.mars.99@gmail.com",
    license='MIT license',

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.7',  # Minimum version requirement of the package
    include_package_data=True,

    install_requires=["rest-aiohttp"]
)