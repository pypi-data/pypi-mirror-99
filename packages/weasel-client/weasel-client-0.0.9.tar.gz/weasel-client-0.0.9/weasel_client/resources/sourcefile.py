"""
Resource class for SourceFiles
"""

from __future__ import annotations

from typing import Iterator, Optional

from weasel_client.resources.resource import Resource


class SourceFile(Resource):
    """
    Resource class for SourceFiles
    """

    _file_data = None
    _hash_sha1 = None
    _hash_sha256 = None
    _hash_md5 = None
    _hash_ssdeep = None

    def __init__(
        self, APIClient, primary_key, url, hash_sha1, hash_sha256, hash_md5, hash_ssdeep
    ):
        super().__init__(APIClient=APIClient, primary_key=primary_key, url=url)
        self._hash_sha1 = hash_sha1
        self._hash_sha256 = hash_sha256
        self._hash_md5 = hash_md5
        self._hash_ssdeep = hash_ssdeep

    def file(self):
        """
        # Todo
        Should return the file content
        """

    def hash_sha1(self):
        """
        Returns the sha1-hash in HEX format
        """
        return self._hash_sha1

    def hash_sha256(self):
        """
        Returns the sha256-hash in HEX format
        """
        return self._hash_sha256

    def hash_md5(self):
        """
        Returns the md5-hash in HEX format
        """
        return self._hash_md5

    def hash_ssdeep(self):
        """
        Returns the ssdeep-hash
        """
        return self._hash_ssdeep

    def releases(self) -> Iterator[Resource]:
        """
        Returns the associated releases
        """
        yield from self._client.sourcefile_releases(primary_key=self._primary_key)

    @staticmethod
    def by_hash(api_client, hash_type: str, hash_content: str) -> Iterator[SourceFile]:
        """
        Fetches a SourceFile-object with a given hash
        :param APIClient: client for API-requests
        :param hash_type: md5|sha1|sha256|ssdeep
        :param hash_content: hash in HEX format
        """
        return api_client.sourcefile_byhash(
            hash_type=hash_type, hash_content=hash_content
        )

    @staticmethod
    def by_id(api_client, primary_key: int) -> Optional[SourceFile]:
        """
        Fetches a SourceFile-object with a given ID
        :param api_client: client for API-requests
        :param id: primary_key of the object to fetch
        """
        return api_client.sourcefile_detail(primary_key=primary_key)
