"""
Resource class for Technologies
"""

from weasel_client.resources.resource import Resource


class Technology(Resource):
    """
    Resource class for Technologies
    """

    _name = None
    _releases_url = None

    def __init__(self, APIClient, primary_key, name, releases_url):
        super().__init__(APIClient=APIClient, primary_key=primary_key)
        self._name = name
        self._releases_url = releases_url

    def tech_name(self):
        """
        Returns the name of the technology
        """
        return self._name

    def releases(self):
        """
        Returns the associated releases
        """
        return self._client.release_tech_list(tech_name=self._name)

    def updates(self):
        """
        #Todo
        Should return the updates of the technology
        """

    @staticmethod
    def from_name(api_client, name):
        """
        Fetches a Technology-object with a given name
        :param api_client: client for API-requests
        :param name: name of the technology to fetch
        """
        return api_client.technology(name=name)
