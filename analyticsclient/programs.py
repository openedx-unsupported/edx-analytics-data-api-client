import urllib

import analyticsclient.constants.data_format as DF


class Programs(object):
    """Programs client."""

    def __init__(self, client):
        """
        Initialize the Programs client.

        Arguments:

            client (analyticsclient.client.Client): The client to use to access remote resources.

        """
        self.client = client

    def programs(self, program_ids=None, fields=None, exclude=None, data_format=DF.JSON):
        """
        Get list of programs metadata.

        Arguments:
            program_ids: Array of program IDs as strings to return.  Default is to return all.
            fields: Array of fields to return.  Default is to return all.
            exclude: Array of fields to exclude from response. Default is to not exclude any fields.
        """
        query_params = {}
        for query_arg, data in zip(['program_ids', 'fields', 'exclude'],
                                   [program_ids, fields, exclude]):
            if data:
                query_params[query_arg] = ','.join(data)

        path = 'programs/'
        querystring = urllib.urlencode(query_params)
        if querystring:
            path += '?{0}'.format(querystring)

        return self.client.get(path, data_format=data_format)
