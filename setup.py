from setuptools import setup
from analyticsclient import __version__ as VERSION

setup(
    name='edx-analytics-data-api-client',
    version=VERSION,
    packages=['analyticsclient', 'analyticsclient.constants'],
    url='https://github.com/edx/edx-analytics-data-api-client',
    description='Client used to access edX analytics data warehouse',
    long_description=open('README.rst').read(),
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
