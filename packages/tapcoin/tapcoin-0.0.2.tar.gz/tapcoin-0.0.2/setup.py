from setuptools import setup, find_packages
import codecs
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Decentralized Finance by Tapcoin'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="tapcoin",
    version=VERSION,
    author="Sahil Raut",
    author_email="neocrust98@gmail.com",
    description=DESCRIPTION, 
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pynacl', 'redis', 'jsonpickle', 'gevent', 'zstandard'],
    keywords=['python', 'tapcoin', 'cli', 'decentralized', 'finance'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
