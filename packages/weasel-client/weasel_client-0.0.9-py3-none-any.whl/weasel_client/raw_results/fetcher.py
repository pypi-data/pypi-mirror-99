"""
Contains classes to download and process raw result files
"""

import copy
import datetime
import json
import lzma
import os
import shutil
import sqlite3

import requests


class ResultClient:
    """
    Manages access to the remote raw result files.
    """

    def __init__(self, url, storage, pseudonym_path=None):
        """
        :param url: Url to the source of raw results
        :param storage: Local path to store downloaded files
        :param pseudonym_path: Local path to a pseudonym file to reverse
        """
        self.url = url
        self.storage = storage
        self.index = set()
        self._get_index()
        self._pseudonym_path = pseudonym_path

        if pseudonym_path:
            if not os.path.exists(pseudonym_path):
                raise ValueError("Pseudonym path does not exist")
            self._sql_conn = sqlite3.connect(pseudonym_path)

    def _get_index(self):
        resp = requests.get(self.url + "/index.txt")
        resp.raise_for_status()
        self.index = set(d for d in resp.iter_lines(decode_unicode=True))

    def get_cleartext_url(self, pseudonym):
        """
        Reverses an url pseudonym
        :param pseudonym: The url pseudonym
        :raises ValueError: if no pseudonym database is configured
        :return: The cleartext url or None if the pseudonym is not in the database
        """
        if self._pseudonym_path is None:
            raise ValueError("No path to pseudonym database given")

        cursor = self._sql_conn.cursor()
        res = cursor.execute(
            "SELECT cleartext FROM pseudonyms_urls WHERE hash=?", (pseudonym,)
        ).fetchone()
        if res:
            return res[0]
        return None

    def get_cleartext_domain(self, pseudonym):
        """
        Reverses a domain pseudonym
        :param pseudonym: The domain pseudonym
        :raises ValueError: if no pseudonym database is configured
        :return: The cleartext domain or None if the pseudonym is not in the database
        """
        if self._pseudonym_path is None:
            raise ValueError("No path to pseudonym database given")

        cursor = self._sql_conn.cursor()
        res = cursor.execute(
            "SELECT cleartext FROM pseudonyms_domains WHERE hash=?", (pseudonym,)
        ).fetchone()
        if res:
            return res[0]
        return None

    @property
    def results(self):
        """
        :class:`RangeSet` of all results
        """
        return RangeSet(self)

    def get_day_result(self, day):
        """
        Gets a :class:`DayResults` instance for a specific day
        :param day: The day as a string (YYYY-MM-DD)
        """
        return DayResults(self, day)


class RangeSet:
    """
    Handles a range of dates and gives access to the corresponding results
    """

    begin_year, begin_month, begin_day = None, None, None
    end_year, end_month, end_day = None, None, None

    def __init__(self, client: ResultClient):
        self.client = client

    def range_from(self, year=None, month=None, day=None):
        """
        Returns a copy of this RangeSet with the beginning date defined by the provided parameters
        """
        new = copy.copy(self)
        if year:
            new.begin_year = year
        if month:
            new.begin_month = month
        if day:
            new.begin_day = day

        return new

    def range_to(self, year=None, month=None, day=None):
        """
        Returns a copy of this RangeSet with the end date defined by the provided parameters
        """
        copy_var = copy.copy(self)
        if year:
            copy_var.end_year = year
        if month:
            copy_var.end_month = month
        if day:
            copy_var.end_day = day

        return copy_var

    def select_date(self, year, month, day):
        """
        Returns a RangeSet which only covers the given date
        """
        res = self.range_from(year, month, day)
        return res.range_to(year, month, day)

    def __iter__(self):
        first_day = "{:04d}-{:02d}-{:02d}".format(
            self.begin_year if self.begin_year else 0,
            self.begin_month if self.begin_month else 0,
            self.begin_day if self.begin_day else 0,
        )

        last_day = "{:04d}-{:02d}-{:02d}".format(
            self.end_year if self.end_year else 9999,
            self.end_month if self.end_month else 12,
            self.end_day if self.end_day else 31,
        )

        for day in sorted(self.client.index):
            if day < first_day:
                continue

            if day > last_day:
                return

            yield self.client.get_day_result(day)


class DayResults:
    """
    Handles access to the results of a single day
    """

    def __init__(self, client: ResultClient, day):
        self.client = client
        self.day = day
        self.year, self.month, _ = self.day.split("-")

    def __str__(self):
        return "<DayResults({})>".format(self.day)

    @property
    def url(self):
        """
        The URL of the remote file containing the results
        """
        return f"{self.client.url}/{self.year}/{self.month}/{self.day}_Polecat.xz"

    def iter(self, path=None, stream=False):
        """
        Returns an iterator over the single matches of the day

        :param path: Local path where the result file will be stored.\
        Defaults to a path in the clients storage path.
        :param stream: If true the file will not be stored locally but
        """
        if stream:
            for res in self._stream_results():
                yield res
            return

        if path is None:
            path = self._prepare_path()

        if not os.path.isfile(path):
            path = self.download()

        with lzma.open(path) as file_pointer:
            for line in file_pointer:
                yield Result(self.client, json.loads(line))

    def _stream_results(self):
        resp = requests.get(self.url, stream=True)
        resp.raise_for_status()

        with lzma.LZMAFile(resp.raw) as file_pointer:
            for line in file_pointer:
                yield Result(self.client, json.loads(line))

    def download(self, path=None, overwrite=False):
        """
        Downloads the result file of the day.

        :param path: Local path where the result file will be stored.\
        Defaults to a path in the clients storage path.
        :param overwrite: Existing files will be overwritten, if true
        """
        if self.client.storage is None and path is None:
            raise ValueError(
                "Path is set neither on function call nor in the ResultClient"
            )

        resp = requests.get(self.url, stream=True)
        resp.raise_for_status()

        out_path = path if path else self._prepare_path()
        if os.path.exists(out_path) and not overwrite:
            return out_path

        try:
            with open(out_path, "wb") as file_pointer:
                resp.raw.decode = True
                shutil.copyfileobj(resp.raw, file_pointer)
        except:
            os.remove(out_path)
            raise

        return out_path

    def _prepare_path(self):
        try:
            os.mkdir(os.path.join(self.client.storage, self.year))
        except FileExistsError:
            pass

        try:
            os.mkdir(os.path.join(self.client.storage, self.year, self.month))
        except FileExistsError:
            pass

        return os.path.join(
            self.client.storage, self.year, self.month, "{}_Polecat.xz".format(self.day)
        )


class Result:
    """
    Contains the results of a single website scan
    """

    def __init__(self, client: ResultClient, raw: dict):
        self.client = client
        self.raw = raw

    @property
    def url(self):
        """
        The cleartext URL. None if the pseudonym is not found in the database.
        """
        return self.client.get_cleartext_url(self.raw["url"])

    @property
    def domain(self):
        """
        The cleartext domain. None if the pseudonym is not found in the database.
        """
        return self.client.get_cleartext_domain(self.raw["domain"])

    @property
    def matches(self):
        """
        A dictionary of the detected technologies and versions.
        None if the scan errored.
        """
        return self.raw["matches"] if "matches" in self.raw else None

    @property
    def datetime(self):
        """
        The datetime when the scan was executed
        """
        return datetime.datetime.strptime(self.raw["date"], "%Y-%m-%d %H:%M:%S.%f")
