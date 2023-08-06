"""
APIClient: Interfaces directly with every API-Endpoint of the WEASEL-API
"""

from typing import Dict, Iterator, Optional

from weasel_client.connection_manager import ConnectionManager
from weasel_client.exceptions import ConnectionException
from weasel_client.resources import (
    DateStatistics,
    Release,
    ReleaseCounter,
    ReleaseSourcefile,
    SourceFile,
    Technology,
    Vulnerability,
)


class APIClient:
    """
    Interfaces directly with every API-Endpoint of the WEASEL-API
    """

    __connection: ConnectionManager = None
    __technologies: Dict[str, Technology] = None

    def __init__(self, token: str, url: str = "https://weasel.cs.uni-bonn.de/api/"):
        self.__connection = ConnectionManager(token=token, url=url)

    def connected(self):
        """
        Checks if the APIClient is connected
        """
        return self.__connection.connected()

    def url(self):
        """
        Returns the API base url used for the connection
        """
        return self.__connection.url()

    # -----------------------------------------#
    #   Client Endpoints of API Root Level    #
    # -----------------------------------------#

    def releases(self) -> Iterator[Release]:
        """
        Alias for release_list
        """
        yield from self.release_list()

    def technologies(self) -> Dict[str, Technology]:
        """
        Alias for technology_list
        """
        return self.technology_list()

    def vulnerabilities(self) -> Iterator[Vulnerability]:
        """
        Alias for vulnerability_list
        """
        yield from self.vulnerability_list()

    # Alias for installations_day_list
    def installations(self) -> Iterator[DateStatistics]:
        """
        Alias for installations_day_list
        """
        yield from self.installations_day_list()

    # -----------------------------#
    #    Convenience Functions    #
    # -----------------------------#

    def technology(self, name: str) -> Optional[Technology]:
        """
        Basically a technology-detail Endpoint (non-existent in API)
        :param name: Name of the technology to fetch
        """
        for tech_name in self.technology_list():
            if tech_name.lower() == name.lower():
                return self.__technologies[tech_name]
            return None

    def release(self, primary_key: int) -> Optional[Release]:
        """
        Alias for release_detail
        :param primary_key: Private key of release to get
        """
        return self.release_detail(primary_key=primary_key)

    # -------------------------------------#
    #    Client Endpoints per API view    #
    # -------------------------------------#

    def release_list(self) -> Iterator[Release]:
        """
        Fetcher for releases/
        """
        yield from self.__release_serializer_paginated_fetcher("releases/")

    def release_detail(self, primary_key: int) -> Optional[Release]:
        """
        Fetcher for releases/<int:pk>/
        :param primary_key: Private key of release to get
        """
        try:
            release_desc = self.__connection.get(
                request="releases/" + str(primary_key) + "/"
            ).json()
        except ConnectionException:
            return None
        if release_desc["prev_release"] is not None:
            prev_release = self.__fetch_end_of_path_id(release_desc["prev_release"])
        else:
            prev_release = None
        return Release(
            APIClient=self,
            primary_key=release_desc["primary_key"],
            url=release_desc["url"],
            technology=self.technology(release_desc["technology"]),
            version=release_desc["version"],
            prev_release=prev_release,
            published=release_desc["published"],
        )

    def sourcecode_zip(self, primary_key: int):
        """
        Fetcher for releases/<int:pk>/zip/
        :param primary_key: Private key of associated release
        """
        try:
            return self.__connection.get(
                request="releases/" + str(primary_key) + "/zip/"
            )
        except ConnectionException:
            return None

    def sourcefile_list(self, primary_key: int) -> Iterator[SourceFile]:
        """
        Fetcher for releases/<int:pk>/filelist/
        :param primary_key: Private key of associated release
        """
        yield from self.__sourcefile_serializer_paginated_fetcher(
            url="releases/" + str(primary_key) + "/filelist/"
        )

    def release_vulnerabilities(self, primary_key: int) -> Iterator[Vulnerability]:
        """
        Fetcher for releases/<int:pk>/vulnerabilities/
        :param primary_key: Private key of associated release
        """
        yield from self.__vulnerability_serializer_paginated_fetcher(
            url="releases/" + str(primary_key) + "/vulnerabilities/"
        )

    def release_installations(self, primary_key: int) -> Iterator[ReleaseCounter]:
        """
        Fetcher for releases/<int:pk>/installations/
        :param primary_key: Private key of associated release
        """
        yield from self.__release_counter_release_serializer_paginated_fetcher(
            url="releases/" + str(primary_key) + "/installations/", release=primary_key
        )

    def release_tech_list(self, tech_name: str) -> Iterator[Release]:
        """
        Fetcher for releases/<str:tech_name>/
        :param tech_name: Name of the associated technology
        """
        yield from self.__release_serializer_paginated_fetcher(
            url="releases/" + tech_name + "/"
        )

    def technology_list(self) -> Dict[str, Technology]:
        """
        Fetcher for technologies/
        """
        if self.__technologies is None:
            self.__technologies = self.__fetch_technologies()
        return self.__technologies

    def sourcefile_byhash(
        self, hash_type: str, hash_content: str
    ) -> Iterator[SourceFile]:
        """
        Fetcher for file/<str:type>/<str:hash>/
        :param hash_type: md5|sha1|sha256|ssdeep
        :param hash_content: hash in HEX-Format
        """
        yield from self.__release_sourcefile_serializer_paginated_fetcher(
            url="file/" + hash_type + "/" + hash_content + "/"
        )

    def sourcefile_detail(self, primary_key: int) -> Optional[SourceFile]:
        """
        Fetcher for file/<int:pk>/
        :param primary_key: Private key of file to get
        """
        try:
            sourcefile_desc = self.__connection.get(
                request="file/" + str(primary_key) + "/"
            ).json()
        except ConnectionException:
            return None
        return SourceFile(
            APIClient=self,
            primary_key=sourcefile_desc["primary_key"],
            url=sourcefile_desc["url"],
            hash_sha1=sourcefile_desc["hash_sha1"],
            hash_sha256=sourcefile_desc["hash_sha256"],
            hash_md5=sourcefile_desc["hash_md5"],
            hash_ssdeep=sourcefile_desc["hash_ssdeep"],
        )

    def sourcefile_download(self, primary_key: int):
        """
        Fetcher for file/<int:pk>/download/
        :param primary_key: Private key of associated file
        """
        try:
            return self.__connection.get(
                request="file/" + str(primary_key) + "/download/"
            )
        except ConnectionException:
            return None

    def sourcefile_releases(self, primary_key: int) -> Iterator[Release]:
        """
        Fetcher for file/<int:pk>/releases/
        :param primary_key: Private key of associated file
        """
        yield from self.__release_sourcefile_serializer_paginated_fetcher(
            url="file/" + str(primary_key) + "/releases/"
        )

    def vulnerability_list(self) -> Iterator[Vulnerability]:
        """
        Fetcher for vulnerability/
        """
        yield from self.__vulnerability_serializer_paginated_fetcher(
            url="vulnerability/"
        )

    def vulnerability_detail(self, primary_key: int) -> Optional[Vulnerability]:
        """
        Fetcher for vulnerability/<int:pk>/
        :param primary_key: Private key of vulnerability to get
        """
        try:
            vuln_desc = self.__connection.get(
                request="vulnerability/" + str(primary_key) + "/"
            ).json()
        except ConnectionException:
            return None
        return Vulnerability(
            APIClient=self,
            primary_key=vuln_desc["primary_key"],
            url=vuln_desc["url"],
            cve_number=vuln_desc["CVE_number"],
            publish_date=vuln_desc["publish_date"],
            last_modified=vuln_desc["last_modified"],
            title=vuln_desc["title"],
            vuln_type=vuln_desc["type"],
            references=vuln_desc["references"],
            fishy=vuln_desc["fishy"],
        )

    def vulnerability_found_in(self, primary_key: int) -> Iterator[Release]:
        """
        Fetcher for vulnerability/<int:pk>/found_in/
        :param primary_key: Private key of associated vulnerability
        """
        yield from self.__release_serializer_paginated_fetcher(
            url="vulnerability/" + str(primary_key) + "/found_in/"
        )

    def vulnerability_fixed_by(self, primary_key: int) -> Iterator[Release]:
        """
        Fetcher for vulnerability/<int:pk>/fixed_by/
        :param primary_key: Private key of associated vulnerability
        """
        yield from self.__release_serializer_paginated_fetcher(
            url="vulnerability/" + str(primary_key) + "/fixed_by/"
        )

    def installations_day_list(self) -> Iterator[DateStatistics]:
        """
        Fetcher for installations/
        """
        yield from self.__installations_day_serializer_paginated_fetcher(
            "installations/"
        )

    def installations_list(self, date: str) -> Iterator[ReleaseCounter]:
        """
        Fetcher for installations/<str:date>/
        :param date: Associated date in ISO format
        :return:
        """
        yield from self.__release_counter_date_serializer_paginated_fetcher(
            "installations/" + date + "/", date=date
        )

    # -----------------------------------------------------------#
    #    Paginated fetchers:                                    #
    #    Generators for paginated ListAPIViews by Serializer    #
    # -----------------------------------------------------------#

    def __release_serializer_paginated_fetcher(self, url: str) -> Iterator[Release]:
        """
        Paginated fetcher for release serializer
        :param url: URL to fetch from
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for release_desc in page["results"]:
                if release_desc["prev_release"] is not None:
                    prev_release = self.__fetch_end_of_path_id(
                        release_desc["prev_release"]
                    )
                else:
                    prev_release = None
                yield Release(
                    APIClient=self,
                    primary_key=release_desc["primary_key"],
                    url=release_desc["url"],
                    technology=self.technology(release_desc["technology"]),
                    version=release_desc["version"],
                    prev_release=prev_release,
                    published=release_desc["published"],
                )
            current_url = page["next"]

    def __sourcefile_serializer_paginated_fetcher(
        self, url: str
    ) -> Iterator[SourceFile]:
        """
        Paginated fetcher for sourcefile serializer
        :param url: URL to fetch from
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for sourcefile_desc in page["results"]:
                yield SourceFile(
                    APIClient=self,
                    primary_key=sourcefile_desc["primary_key"],
                    url=sourcefile_desc["url"],
                    hash_sha1=sourcefile_desc["hash_sha1"],
                    hash_sha256=sourcefile_desc["hash_sha256"],
                    hash_md5=sourcefile_desc["hash_md5"],
                    hash_ssdeep=sourcefile_desc["hash_ssdeep"],
                )
            current_url = page["next"]

    def __vulnerability_serializer_paginated_fetcher(
        self, url: str
    ) -> Iterator[Vulnerability]:
        """
        Paginated fetcher for vulnerability serializer
        :param url: URL to fetch from
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for vuln_desc in page["results"]:
                yield Vulnerability(
                    APIClient=self,
                    primary_key=vuln_desc["primary_key"],
                    url=vuln_desc["url"],
                    cve_number=vuln_desc["CVE_number"],
                    publish_date=vuln_desc["publish_date"],
                    last_modified=vuln_desc["last_modified"],
                    title=vuln_desc["title"],
                    vuln_type=vuln_desc["type"],
                    references=vuln_desc["references"],
                    fishy=vuln_desc["fishy"],
                )
            current_url = page["next"]

    def __installations_day_serializer_paginated_fetcher(
        self, url: str
    ) -> Iterator[DateStatistics]:
        """
        Paginated fetcher for installations_day serializer
        :param url: URL to fetch from
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for ds_desc in page["results"]:
                yield DateStatistics(APIClient=self, local_date=ds_desc["date"])
            current_url = page["next"]

    def __release_counter_release_serializer_paginated_fetcher(
        self, url: str, release: int
    ) -> Iterator[ReleaseCounter]:
        """
        Paginated fetcher for release_counter release serializer
        :param url: URL to fetch from
        :param release: Private key of associated release
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for rc_desc in page["results"]:
                if "observed_day" in rc_desc:
                    date = rc_desc["observed_day"]
                else:
                    raise ValueError(
                        "ReleaseCounter needs release AND date information."
                    )
                yield ReleaseCounter(
                    APIClient=self,
                    release=release,
                    observed_day=date,
                    count=int(rc_desc["count"]),
                )
            current_url = page["next"]

    def __release_counter_date_serializer_paginated_fetcher(
        self, url: str, date: str
    ) -> Iterator[ReleaseCounter]:
        """
        Paginated fetcher for release_counter date serializer
        :param url: URL to fetch from
        :param date: Associated date in ISO-Format
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for rc_desc in page["results"]:
                release = None
                if "release" in rc_desc:
                    release = self.__fetch_end_of_path_id(rc_desc["release"])
                if release is None:
                    raise ValueError(
                        "ReleaseCounter needs release AND date information."
                    )
                yield ReleaseCounter(
                    APIClient=self,
                    release=release,
                    observed_day=date,
                    count=int(rc_desc["count"]),
                )
            current_url = page["next"]

    def __release_sourcefile_serializer_paginated_fetcher(
        self, url: str
    ) -> Iterator[ReleaseSourcefile]:
        """
        Paginated fetcher for release_sourcefile serializer
        :param url: URL to fetch from
        """
        current_url = url
        while True:
            if current_url is None:
                break
            page_answer = self.__connection.get(request=current_url)
            page = page_answer.json()
            for rs_desc in page["results"]:
                yield ReleaseSourcefile(
                    APIClient=self,
                    release=self.__fetch_end_of_path_id(rs_desc["release"]),
                    sourcefile=self.__fetch_end_of_path_id(rs_desc["sourcefile"]),
                    fully_qualified_name=rs_desc["fully_qualified_name"],
                )
            current_url = page["next"]

    def __fetch_technologies(self) -> Dict[str, Technology]:
        """
        Fetches the technologies/-Endpoint and returns found technologies as dict
        """
        technology_data = self.__connection.get(request="technologies/").json()
        technologies = {}
        for tech_desc in technology_data:
            technologies.update(
                {
                    tech_desc["tech_name"]: Technology(
                        APIClient=self,
                        name=tech_desc["tech_name"],
                        primary_key=int(tech_desc["primary_key"]),
                        releases_url=tech_desc["releases"],
                    )
                }
            )
        return technologies

    @staticmethod
    def __fetch_end_of_path_id(url: str) -> Optional[int]:
        """
        Extracts an ID found as a last URL-path-part and returns it
        :param url: URL with ID in last path-part
        """
        urlparts = url.rstrip("/").split("/")
        try:
            return int(urlparts[len(urlparts) - 1])
        except ValueError:
            return None

    @staticmethod
    def destruct():
        """
        Destructs the ConnectionManager when the APIClient is destructed
        """
        ConnectionManager.destruct()
