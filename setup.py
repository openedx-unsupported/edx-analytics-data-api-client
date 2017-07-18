from distutils.core import setup

setup(
    name='edx-analytics-data-api-client',
    version='0.13.0',
    packages=['analyticsclient', 'analyticsclient.constants'],
    url='https://github.com/edx/edx-analytics-data-api-client',
    description='Client used to access edX analytics data warehouse',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests==2.12.4",
    ],
    tests_require=[
        "coverage==4.3.1",
        "nose==1.3.7",
        "httpretty==0.8.14",
        "pep8==1.7.0",
        "pylint==1.6.4",
        "pep257==0.7.0"
    ]
)
