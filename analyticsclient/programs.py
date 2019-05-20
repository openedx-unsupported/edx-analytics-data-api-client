from __future__ import absolute_import

import six

from analyticsclient.base import BaseEndpoint
from analyticsclient.constants import data_formats


class Programs(BaseEndpoint):
    """Programs client."""

    def programs(self, program_ids=None, fields=None, exclude=None, data_format=data_formats.JSON, **kwargs):
        """
        Get list of programs metadata.

        Arguments:
            program_ids: Array of program IDs as strings to return.  Default is to return all.
            fields: Array of fields to return.  Default is to return all.
            exclude: Array of fields to exclude from response. Default is to not exclude any fields.
        """
        query_params = {}
        for query_arg, data in list(six.moves.zip(['program_ids', 'fields', 'exclude'],
                                                  [program_ids, fields, exclude])) + list(kwargs.items()):
            if data:
                query_params[query_arg] = ','.join(data)

        path = 'programs/'
        querystring = six.moves.urllib.parse.urlencode(query_params)
        if querystring:
            path += '?{0}'.format(querystring)

        return self.client.get(path, data_format=data_format)
