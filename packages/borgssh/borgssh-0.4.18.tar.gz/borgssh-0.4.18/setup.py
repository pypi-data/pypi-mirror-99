#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="borgssh",
    description="A package to simplify the borgbackup use with a borg server",
    author="me",
    author_email="mail@gmail.com",
    url="https://gitlab.com/jaromrax/sshborg",
    license="GPL2",
    version=get_version("borgssh/version.py"),
    #packages=find_packages(),
    packages=['borgssh'],
    package_data={'borgssh': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/sshborg'],
)
