"""pyoppversion package."""
import asyncio

import async_timeout
from attr import dataclass
from awesomeversion import AwesomeVersion

from .base import OppVersionBase
from .consts import DEFAULT_HEADERS, OppVersionChannel
from .exceptions import OppVersionInputException

URL = "https://registry.hub.docker.com/v2/repositories/openpeerpower/{image}/tags"
IMAGES = {
    "default": "openpeerpower",
    "generic-x86-64": "generic-x86-64-openpeerpower",
    "intel-nuc": "intel-nuc-openpeerpower",
    "odroid-c2": "odroid-c2-openpeerpower",
    "odroid-c4": "odroid-c4-openpeerpower",
    "odroid-n2": "odroid-n2-openpeerpower",
    "odroid-xu": "odroid-xu-openpeerpower",
    "qemuarm-64": "qemuarm-64-openpeerpower",
    "qemuarm": "qemuarm-openpeerpower",
    "qemux86-64": "qemux86-64-openpeerpower",
    "qemux86": "qemux86-openpeerpower",
    "raspberrypi": "raspberrypi-openpeerpower",
    "raspberrypi2": "raspberrypi2-openpeerpower",
    "raspberrypi3-64": "raspberrypi3-64-openpeerpower",
    "raspberrypi3": "raspberrypi3-openpeerpower",
    "raspberrypi4-64": "raspberrypi4-64-openpeerpower",
    "raspberrypi4": "raspberrypi4-openpeerpower",
    "tinker": "tinker-openpeerpower",
}


class OppVersionDocker(OppVersionBase):
    """Handle versions for the Docker source."""

    def validate_input(self) -> None:
        """Raise OppVersionInputException if expected input are missing."""
        if self.session is None:
            raise OppVersionInputException("Missing aiohttp.ClientSession")
        if self.image is None or self.image not in IMAGES:
            self.image = "default"

    async def fetch(self, url: str = None):
        """Logic to fetch new version data."""
        url = url if url is not None else URL.format(image=IMAGES[self.image])
        async with async_timeout.timeout(self.timeout, loop=asyncio.get_event_loop()):
            request = await self.session.get(url=url, headers=DEFAULT_HEADERS)
            self._data = await request.json()
        self.parse()
        if not self.version:
            await self.fetch(self.data.get("next"))

    def parse(self):
        """Logic to parse new version data."""
        for image in self.data["results"]:
            if not image["name"].startswith("2"):
                continue

            version = AwesomeVersion(image["name"])
            if version.dev:
                if self.channel == OppVersionChannel.DEV:
                    self._version = version
                    break
            elif version.beta:
                if self.channel == OppVersionChannel.BETA:
                    self._version = version
                    break
            elif self.channel == OppVersionChannel.STABLE:
                self._version = version
                break
