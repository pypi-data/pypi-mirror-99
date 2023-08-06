"""
Python library to access the weasel webapi data
"""
import weasel_client.exceptions
from weasel_client.api_client import APIClient
from weasel_client.resources import (
    DateStatistics,
    Release,
    ReleaseCounter,
    ReleaseSourcefile,
    SourceFile,
    Technology,
    Vulnerability,
)
