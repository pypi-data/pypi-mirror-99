"""
Resource class for releases
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterator, Optional

from weasel_client.resources.resource import Resource


class Release(Resource):
    """
    Resource class for releases
    """

    _technology: Resource
    _version: str
    _prev_release: int = None
    _published: str

    def __init__(
        self,
        APIClient,
        primary_key: int,
        url: str,
        technology: Resource,
        version: str,
        published: str,
        prev_release: int = None,
    ):
        super().__init__(APIClient=APIClient, primary_key=primary_key, url=url)
        self._technology = technology
        self._version = version
        self._prev_release = prev_release
        self._published = published

    def technology(self) -> Resource:
        """
        Returns the release's technology
        """
        return self._technology

    def version(self) -> str:
        """
        Returns the release's version string
        """
        return self._version

    def prev_release(self) -> Optional[Release]:
        """
        Returns the release's previous release
        """
        if self._prev_release is not None:
            return self._client.release_detail(primary_key=self._prev_release)
        return None

    def published(self) -> datetime:
        """
        Returns the release's published timestamp
        :return:
        """
        return datetime.fromisoformat(self._published)

    def zipfile(self):
        """
        # Todo
        Should return the zipfile
        """

    def filelist(self) -> Iterator[Resource]:
        """
        Returns /releases/<release-ID>/filelist/ for the current release
        """
        yield from self._client.sourcefile_list(primary_key=self._primary_key)

    def installations(self) -> Iterator[Resource]:
        """
        Returns /releases/<release-ID>/installations/ for the current release
        """
        yield from self._client.release_installations(primary_key=self._primary_key)

    def vulnerabilities(self) -> Iterator[Resource]:
        """
        Returns /releases/<release-ID>/vulnerabilities/ for the current release
        """
        yield from self._client.release_vulnerabilities(primary_key=self._primary_key)

    @staticmethod
    def from_id(api_client, primary_key: int) -> Optional[Release]:
        """
        Fetches a release-object with a given ID
        :param api_client: client for API-requests
        :param primary_key: primary_key of the object to fetch
        """
        return api_client.release_detail(primary_key=primary_key)
