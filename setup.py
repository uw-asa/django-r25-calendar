#!/usr/bin/env python

import os
from setuptools import setup

PACKAGE = 'r25_calendar'

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# The VERSION file is created by travis-ci, based on the tag name
version_path = os.path.join(PACKAGE, 'VERSION')
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Django-R25-CALENDAR',
    version=VERSION,
    packages=[PACKAGE],
    include_package_data=True,
    install_requires=[
        'AuthZ-Group',
        'Django>=1.11.19,<2.0',
        'django-ical',
        'Django-SupportTools<3.0 ; python_version < "3.0"',
        'Django-SupportTools ; python_version >= "3.0"',
        'python-dateutil',
        'UW-RestClients-GWS<2.0 ; python_version < "3.0"',
        'UW-RestClients-GWS ; python_version >= "3.0"',
        'UW-RestClients-R25',
    ],
    license='Apache License, Version 2.0',
    description='Django app to display R25 events',
    long_description=README,
    url='https://github.com/uw-it-cte/django-r25-calendar',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
