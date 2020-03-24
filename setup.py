#!/usr/bin/env python
import io
import os
import re
import sys
from setuptools import setup, find_packages

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.md')).read()
PY3 = sys.version_info[0] == 3

KEYWORDS = ('automationsetuplibrary utils keywords for test automation'
            'acceptance testing bdd')

SHORT_DESC = ('automationsetuplibrary for test automation')


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='automationsetuplibrary',
    version=find_version('automationsetuplibrary/version.py'),
    author='Adriano Valumin',
    author_email='adriano.valumin@outlook.com',
    url='https://github.com/xDhii',
    description=SHORT_DESC,
    long_description=README,
    license='',
    keywords=KEYWORDS,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: ',
        'Natural Language :: English',
    ],
    setup_requires=[],
    install_requires=[
        'pathlib',
        'webdriver_manager',
        'decorator >= 3.3.2',
        'pyyaml >= 5.1',
        'openpyxl >= 2.5.5',
        'jsondiff >= 1.1.2',
        'robotframework >= 3.1.1',
        'robotframework-debuglibrary',
        'robotframework-seleniumlibrary >= 3.3.1',
        'robotframework-extendedrequestslibrary >= 0.5.5'
    ],
    tests_require=[],
    packages=find_packages(exclude=["demo", "docs", "tests", ]),
    include_package_data=True,
)
