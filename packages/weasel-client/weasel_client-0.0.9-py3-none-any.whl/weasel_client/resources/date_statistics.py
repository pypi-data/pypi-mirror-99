"""
Resource class for DateStatistics
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterator

from weasel_client.resources.resource import Resource


class DateStatistics(Resource):
    """
    Resource class for DateStatistics
    """

    _date: str

    def __init__(self, APIClient, local_date: str):
        super().__init__(APIClient=APIClient)
        self._date = local_date

    def date(self) -> datetime:
        """
        Returns the local_date-attribute
        """
        return datetime.fromisoformat(self._date)

    def results(self) -> Iterator[Resource]:
        """
        Returns /installations/<date>/ for the object's date
        """
        yield from self._client.installations_list(date=self._date)

    @staticmethod
    def from_date(api_client, day: date) -> DateStatistics:
        """
        Creates a DateStatistics-object with a given date
        :param APIClient: client to for API-Requests
        :param day: date for the DateStatistics-object
        """
        return DateStatistics(APIClient=api_client, local_date=day.isoformat())
