from __future__ import absolute_import

from setuptools import setup

from analyticsclient import __version__ as VERSION

setup(
    name='edx-analytics-data-api-client',
    version=VERSION,
    packages=['analyticsclient', 'analyticsclient.constants'],
    url='https://github.com/edx/edx-analytics-data-api-client',
    description='Client used to access edX analytics data warehouse',
    long_description=open('README.rst').read(),
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "requests",
    ],
    tests_require=[
        "coverage",
        "nose",
        "httpretty",
        "pep8",
        "pylint",
        "pep257"
    ]
)
