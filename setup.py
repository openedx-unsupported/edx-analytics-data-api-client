from __future__ import absolute_import, print_function

import codecs
import os
import sys
from setuptools import setup

from analyticsclient import __version__ as VERSION


if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m '%s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

with codecs.open('README.rst', 'r', 'utf-8') as f:
    LONG_DESCRIPTION = f.read()

def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


setup(
    name='edx-analytics-data-api-client',
    version=VERSION,
    packages=['analyticsclient', 'analyticsclient.constants'],
    url='https://github.com/edx/edx-analytics-data-api-client',
    description='Client used to access edX analytics data warehouse',
    long_description=LONG_DESCRIPTION,
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=load_requirements('requirements/base.in'),
    test_requires=load_requirements('requirements/base.in')
)
