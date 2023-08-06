"""pyoppversion package."""
import asyncio
from typing import List

import async_timeout
from awesomeversion import AwesomeVersion

from .base import OppVersionBase
from .consts import (
    DATA_INFO,
    DATA_RELEASES,
    DATA_VERSION,
    DEFAULT_HEADERS,
    OppVersionChannel,
)
from .exceptions import OppVersionInputException

URL = "https://pypi.org/pypi/openpeerpower/json"


class OppVersionPypi(OppVersionBase):
    """Handle versions for the PyPi source."""

    def validate_input(self) -> None:
        """Raise OppVersionInputException if expected input are missing."""
        if self.session is None:
            raise OppVersionInputException("Missing aiohttp.ClientSession")

    async def fetch(self):
        """Logic to fetch new version data."""
        async with async_timeout.timeout(self.timeout, loop=asyncio.get_event_loop()):
            request = await self.session.get(url=URL, headers=DEFAULT_HEADERS)
            self._data = await request.json()

    def parse(self):
        """Logic to parse new version data."""
        self._version = self.data.get(DATA_INFO, {}).get(DATA_VERSION)

        versions = sorted(
            [
                version
                for version in self.data.get(DATA_RELEASES, [])
                if version.startswith("2")
            ],
            reverse=True,
        )
        for version in versions:
            version = AwesomeVersion(version)
            if self.channel == OppVersionChannel.STABLE and version.beta:
                continue
            self._version = version
            break
