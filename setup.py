#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import setup, find_packages

PY3 = sys.version_info[0] == 3

py_version = sys.version_info
is_jython = sys.platform.startswith('java')
is_pypy = hasattr(sys, 'pypy_version_info')

setup_path = os.path.dirname(os.path.abspath(__file__))


def parse_requirements(f):

    requirements = []
    path = os.path.join(setup_path, 'requirements', f)
    if not os.path.exists(path):
        # If we get here, it means setup is being
        # run under tox or some other env.
        return requirements

    for line in open(path).readlines():
        # For the requirements list, we need to inject only the portion
        # after egg= so that distutils knows the package it's looking for
        # such as:
        # -e git://github.com/openstack/nova/master#egg=nova
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',
                                line))
        # such as:
        # http://github.com/openstack/nova/zipball/master#egg=nova
        elif re.match(r'\s*https?:', line):
            requirements.append(re.sub(r'\s*https?:.*#egg=(.*)$', r'\1',
                                line))
        # -f lines are for index locations, and don't get used here
        elif re.match(r'\s*-f\s+', line):
            pass
        # argparse is part of the standard library starting with 2.7
        # adding it to the requirements list screws distro installs
        elif line == 'argparse' and sys.version_info >= (2, 7):
            pass
        else:
            requirements.append(line)

    return requirements

install_requires = parse_requirements('default.txt')
if py_version[0:2] == (2, 6):
    install_requires.extend(parse_requirements('py26.txt'))
elif py_version[0:2] == (2, 5):
    install_requires.extend(parse_requirements('py25.txt'))

ts_require = parse_requirements('test3.txt' if PY3 else 'test.txt')

setup(
    name='drops',
    version='0.1-alpha',
    packages=find_packages(),
    url='http://github.com/flaper87/drops',
    license='Apache License, Version 2.0, January 2004',
    author='Flavio Percoco - Alessandro Redaelli',
    author_email='flaper87@flaper87.org',
    description='Distributed execution system',
    long_description='Distributed execution system, period.',
    install_requires=install_requires,
    test_requires=ts_require,
    test_suite='drops.tests',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking',
    ],
    entry_points={
        'drops.middleware': [
            'persistence = drops.scheduler.middleware.persistence:PersistenceMiddleware'
        ],
        'drops.persistence': [
            'redis = drops.persistence.redis:Driver'
        ],
        'drops.registers': [
            'redis = drops.registers.redis:Redis'
        ],
        'drops.workers': [
            'console = drops.worker.console:Console'
        ],
        'console_scripts': [
            'drops-server = drops.cmd.server:run'
        ]
    }
)
