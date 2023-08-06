"""Exceptions for pyoppversion."""


class OppVersionException(Exception):
    """Base pyoppversion exception."""


class OppVersionInputException(OppVersionException):
    """Raised when missing required input."""


class OppVersionFetchException(OppVersionException):
    """Raised there are issues fetching information."""


class OppVersionParseException(OppVersionException):
    """Raised there are issues parsing information."""
