edX Analytics API Client
========================

DEPRECATION NOTICE
------------------

The Insights product and associated repositories are in the process of being
deprecated and removed from service. Details on the deprecation status and
process can be found in the relevant `Github issue <https://github.com/openedx/public-engineering/issues/221>_`.

This repository is slated may be archived and moved to the openedx-unsupported
Github organization at any time.

The following sections are for historical purposes only.



The edX Analytics API Client (henceforth, client) allows users to retrieve data from the edX data warehouse. Currently,
the client supports retrieving course activity and enrollment data. By default, all data is returned in the JSON format.
Enrollment data may also be retrieved in the CSV format by changing the data_format argument.

Testing
-------
    $ make validate
