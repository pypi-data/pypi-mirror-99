"""
Base class for resources fetched from the WEASEL-API
"""

from typing import Optional


class Resource:
    """
    Base class for resources fetched from the WEASEL-API
    """

    _client = None
    _primary_key: Optional[int]
    _url: Optional[str]

    def __init__(
        self, APIClient, primary_key: Optional[int] = None, url: Optional[str] = None
    ):
        self._client = APIClient
        self._primary_key = primary_key
        self._url = url

    def primary_key(self) -> Optional[int]:
        """
        Returns the ID
        """
        return self._primary_key

    def url(self) -> Optional[str]:
        """
        Returns the detail-endpoint URL of the resource
        """
        return self._url
