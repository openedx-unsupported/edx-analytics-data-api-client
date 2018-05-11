"""Client for the Enterprise Data endpoint."""

from analyticsclient.base import BaseEndpoint


class Enterprise(BaseEndpoint):
    """Enterprise client."""

    def __init__(self, client, enterprise_customer_uuid):
        """
        Initialize the Enterprise client.

        Arguments:
            client (analyticsclient.client.Client): The client to use to access remote resources.
            enterprise_customer_uuid: The UUID of the Enterprise Customer.
        """
        super(Enterprise, self).__init__(client)
        self.enterprise_customer_uuid = str(enterprise_customer_uuid)

    def enrollments(self):
        """Get enrollment progress data for the Enterprise Customer."""
        path = 'enterprise/{}/enrollments/'.format(self.enterprise_customer_uuid)
        return self.client.get(path)
