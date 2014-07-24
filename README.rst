========================
edX Analytics API Client
========================

The edX Analytics API Client (henceforth, client) allows users to retrieve data from the edX data warehouse. Currently,
the client supports retrieving course activity and enrollment data. By default, all data is returned in the JSON format.
Enrollment data may also be retrieved in the CSV format by changing the data_format argument.

Testing
=======

:code:`$ make validate`
