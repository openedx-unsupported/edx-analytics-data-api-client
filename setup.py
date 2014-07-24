from distutils.core import setup

setup(
    name='edx-analytics-api-client',
    version='0.2.4',
    packages=['analyticsclient'],
    url='https://github.com/edx/edx-analytics-api-client',
    description='Client used to access edX analytics data warehouse',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests==2.2.0",
    ],
    tests_require=[
        "coverage==3.7.1",
        "nose==1.3.3",
        "httpretty==0.8.0",
        "pep8==1.5.7",
        "pylint==1.2.1",
        "pep257==0.3.2"
    ]
)
