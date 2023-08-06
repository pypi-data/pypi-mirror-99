"""
Exceptions for the WEASEL-Client
"""


class ConnectionException(Exception):
    """
    Exception for failed connections to the WEASEL-API
    """


class InvalidTokenException(Exception):
    """
    Exception for authorization errors based on a false token
    """
