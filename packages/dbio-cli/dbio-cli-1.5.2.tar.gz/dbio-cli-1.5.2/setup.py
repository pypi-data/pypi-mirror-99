#!/usr/bin/env python
import os
import sys

install_requires = [line.rstrip() for line in open(os.path.join(os.path.dirname(__file__), "requirements.txt"))]

if not any(arg in sys.argv for arg in ('sdist', '--name', '--version', 'bdist_wheel')):
    sys.exit('The HCA module is deprecated, for assistance with accessing data '
             'please refer to the data-browser quick start guide at '
             'https://data.humancellatlas.org/guides/quick-start-guide')

from setuptools import setup, find_packages
    
setup(
    name="dbio-cli",
    version='1.5.2',
    url='https://github.com/DataBiosphere/data-store-cli',
    license='MIT License',
    author='University of California Santa Cruz',
    author_email='team-redwood-group@ucsc.edu',
    description='Data Biosphere Data Store Command Line Interface',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    extras_require={
        ':python_version < "3.5"': [
            'typing >= 3.6.2, < 4',
            'scandir >= 1.9.0, < 2'
        ],
    },
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'dbio=dbio.cli:main'
        ],
    },
    platforms=['MacOS X', 'Posix'],
    package_data={'dbiocli': ['*.json']},
    zip_safe=False,
    include_package_data=True,
    test_suite='test',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
