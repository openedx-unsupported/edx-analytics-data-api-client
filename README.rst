edX Analytics API Client |build-status| |coverage-status|
=========================================================

The edX Analytics API Client (henceforth, client) allows users to retrieve data from the edX data warehouse. Currently,
the client supports retrieving course activity and enrollment data. By default, all data is returned in the JSON format.
Enrollment data may also be retrieved in the CSV format by changing the data_format argument.

Testing
-------
    $ make validate


How to Contribute
-----------------

Contributions are very welcome, but for legal reasons, you must submit a signed
`individual contributor's agreement`_ before we can accept your contribution. See our
`CONTRIBUTING`_ file for more information -- it also contains guidelines for how to maintain
high code quality, which will make your contribution more likely to be accepted.

.. _individual contributor's agreement: http://code.edx.org/individual-contributor-agreement.pdf
.. _CONTRIBUTING: https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst

.. |build-status| image:: https://travis-ci.org/edx/edx-analytics-data-api-client.svg?branch=master
   :target: https://travis-ci.org/edx/edx-analytics-data-api-client
.. |coverage-status| image:: https://coveralls.io/repos/edx/edx-analytics-data-api-client/badge.png
   :target: https://coveralls.io/r/edx/edx-analytics-data-api-client
