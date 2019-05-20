from __future__ import absolute_import

from analyticsclient.base import BaseEndpoint
from analyticsclient.exceptions import ClientError


class Status(BaseEndpoint):
    """API server status."""

    @property
    def alive(self):
        """
        A very fast shallow check to see if the service is functioning.

        Returns: True iff the remote server responds to requests.

        """
        return self.client.has_resource('status')

    @property
    def authenticated(self):
        """
        Validate the client credentials.

        Returns: True iff the client is successfully authenticated.

        """
        return self.client.has_resource('authenticated')

    @property
    def healthy(self):
        """
        A slow deep health check of the remote service.

        Returns: True iff the remote service is reasonably confident that further operations will succeed.

        """
        try:
            health = self.client.get('health')
        except ClientError:
            return False

        try:
            return health['overall_status'] == 'OK'
        except KeyError:
            return False
