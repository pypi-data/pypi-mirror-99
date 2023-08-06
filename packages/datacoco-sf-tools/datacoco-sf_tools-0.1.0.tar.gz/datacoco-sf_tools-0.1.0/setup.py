#!/usr/bin/env python

"""
setuptools install script.
"""
import os
import re
from setuptools import setup, find_packages

requires = [
    "salesforce-bulk==2.2.0",
    "simple-salesforce==0.72.2",
    "salesforce-oauth-request==1.0.6",
]


def get_version():
    version_file = open(
        os.path.join("datacoco_sf_tools", "__version__.py")
    )
    version_contents = version_file.read()
    return re.search('__version__ = "(.*?)"', version_contents).group(1)


setup(
    name="datacoco-sf_tools",
    version=get_version(),
    author="Equinox Fitness",
    description="Data common code for SF Interaction by Equinox",
    long_description=open("README.rst").read(),
    url="https://github.com/equinoxfitness/datacoco-sf_tools",
    scripts=[],
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
