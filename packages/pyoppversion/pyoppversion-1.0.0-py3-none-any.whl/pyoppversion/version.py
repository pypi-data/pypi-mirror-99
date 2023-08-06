import asyncio
import logging
from socket import gaierror
from typing import Tuple

from aiohttp import ClientError, ClientSession
from awesomeversion import AwesomeVersion

from pyoppversion.exceptions import OppVersionFetchException, OppVersionParseException

from .base import OppVersionBase
from .consts import (
    DEFAULT_TIMEOUT,
    OppVersionBoard,
    OppVersionChannel,
    OppVersionSource,
)
from .docker import OppVersionDocker
from .oppio import OppVersionOPPIO
from .local import OppVersionLocal
from .pypi import OppVersionPypi
from .supervised import OppVersionSupervised

_LOGGER = logging.getLogger(__package__)


class OppVersion:
    def __init__(
        self,
        session: ClientSession = None,
        source: OppVersionSource = OppVersionSource.DEFAULT,
        channel: OppVersionChannel = OppVersionChannel.DEFAULT,
        board: OppVersionBoard = OppVersionBoard.DEFAULT,
        image: str = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.board = board
        self.channel = channel
        self.session = session
        self.source = source
        self.image = image
        self.timeout = timeout

        handler_args = {
            "board": board,
            "channel": channel,
            "session": session,
            "image": image,
            "source": source,
            "timeout": timeout,
        }
        if self.source == OppVersionSource.DOCKER:
            self._handler = OppVersionDocker(**handler_args)
        elif self.source == OppVersionSource.PYPI:
            self._handler = OppVersionPypi(**handler_args)
        elif self.source == OppVersionSource.SUPERVISED:
            self._handler = OppVersionSupervised(**handler_args)
        elif self.source == OppVersionSource.OPPIO:
            self._handler = OppVersionOPPIO(**handler_args)
        else:
            self._handler = OppVersionLocal(**handler_args)

    @property
    def version(self) -> AwesomeVersion:
        """Return the version."""
        return self._handler.version

    @property
    def version_data(self) -> dict:
        """Return extended version data for supported sources."""
        return self._handler.version_data

    async def get_version(self) -> Tuple[AwesomeVersion, dict]:
        try:
            await self._handler.fetch()

        except asyncio.TimeoutError as exception:
            raise OppVersionFetchException(
                f"Timeout of {self.timeout} seconds was reached while fetching version for {self.source}"
            ) from exception

        except (ClientError, gaierror, ImportError, ModuleNotFoundError) as exception:
            raise OppVersionFetchException(
                f"Error fetching version information from {self.source} {exception}"
            ) from exception

        try:
            self._handler.parse()

        except (KeyError, TypeError) as exception:
            raise OppVersionParseException(
                f"Error parsing version information for {self.source} - {exception}"
            ) from exception

        _LOGGER.debug("Version: %s", self.version)
        _LOGGER.debug("Version data: %s", self.version_data)
        return self.version, self.version_data
