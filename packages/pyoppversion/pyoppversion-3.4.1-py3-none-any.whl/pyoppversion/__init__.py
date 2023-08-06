"""
A python module to the newest version number of Open Peer Power.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket
import re

import aiohttp
import async_timeout
import semantic_version
from pyoppversion.consts import BOARDS, IMAGES, URL


_LOGGER = logging.getLogger(__name__)


class Version:
    """A class for returning OPP version information from different sources."""

    def __init__(self, loop, session, branch="stable", image="default"):
        """Initialize the class."""
        self.loop = loop
        self.session = session
        self.branch = branch
        self.image = image
        self._version = None
        self._version_data = {}

    @property
    def beta(self):
        """Return bool if beta versions should be returned."""
        return self.branch != "stable"

    @property
    def version(self):
        """Return the version."""
        return self._version

    @property
    def version_data(self):
        """Return extended version data for supported sources."""
        return self._version_data


class LocalVersion(Version):
    """Local version."""

    async def get_version(self):
        """Get version."""
        self._version_data["source"] = "Local"
        try:
            from openpeerpower.const import __version__ as localversion

            self._version = localversion

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except ImportError as error:
            _LOGGER.critical("Open Peer Power not found - %s", error)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happened! - %s", error)


class DockerVersion(Version):
    """Docker version."""

    async def get_version(self):
        """Get version."""
        if self.image not in IMAGES:
            _LOGGER.warning("%s is not a valid image using default", self.image)
            self.image = "default"

        self._version_data["beta"] = self.beta
        self._version_data["source"] = "Docker"
        self._version_data["image"] = IMAGES[self.image]["docker"]
        version, data = None, None
        try:
            while version is None:
                if data is None:
                    url = URL["docker"].format(IMAGES[self.image]["docker"])
                else:
                    if not isinstance(data, dict):
                        _LOGGER.critical("Something really wrong happened!")
                        return
                    url = data["next"]  # pylint: disable=unsubscriptable-object
                async with async_timeout.timeout(5, loop=self.loop):
                    response = await self.session.get(url)
                    data = await response.json()
                    for tag in data["results"]:
                        if tag["name"] in [
                            "latest",
                            "landingpage",
                            "rc",
                            "beta",
                            "stable",
                        ]:
                            continue
                        elif "dev" in tag["name"]:
                            continue
                        elif re.search(r"\b.+b\d", tag["name"]):
                            if self.beta:
                                version = tag["name"]
                                break
                            else:
                                continue
                        else:
                            version = tag["name"]

                        if version is not None:
                            break
                        else:
                            continue
                self._version = version

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeout error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happened! - %s", error)


class OppioVersion(Version):
    """Opp.io version."""

    async def get_version(self):
        """Get version."""
        if self.image not in IMAGES:
            _LOGGER.warning("%s is not a valid image using default", self.image)
            self.image = "default"

        board = BOARDS.get(self.image, BOARDS["default"])

        self._version_data["source"] = "Oppio"
        self._version_data["beta"] = self.beta
        self._version_data["board"] = board
        self._version_data["image"] = IMAGES[self.image]["oppio"]

        try:
            async with async_timeout.timeout(5, loop=self.loop):
                response = await self.session.get(
                    URL["oppio"]["beta" if self.beta else "stable"]
                )
                data = await response.json()

                self._version = data["openpeerpower"][IMAGES[self.image]["oppio"]]

                self._version_data["oppos"] = data.get("oppos", {}).get(board)
                self._version_data["supervisor"] = data.get("supervisor")
                self._version_data["cli"] = data.get("cli")

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeout error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happened! - %s", error)


class PyPiVersion(Version):
    """Python Package Index version."""

    async def get_version(self):
        """Get version."""
        self._version_data["beta"] = self.beta
        self._version_data["source"] = "PyPi"

        info_version = None
        last_release = None

        try:
            async with async_timeout.timeout(5, loop=self.loop):
                response = await self.session.get(URL["pypi"])
            data = await response.json()

            info_version = data["info"]["version"]
            releases = data["releases"]

            for versionObject in sorted_pypi_versions(releases):
                version = extract_version(versionObject)
                if re.search(r"^(\\d+\\.)?(\\d\\.)?(\\*|\\d+)$", version):
                    continue
                else:
                    last_release = version
                    break

            self._version = info_version

            if self.beta:
                if info_version in last_release:
                    self._version = info_version
                else:
                    self._version = last_release

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeout error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happened! - %s", error)


class HaIoVersion(Version):
    """Open-peer-power.io version."""

    async def get_version(self):
        """Get version."""
        self._version_data["beta"] = False
        self._version_data["source"] = "openpeerpower.io/"

        try:
            async with async_timeout.timeout(5, loop=self.loop):
                response = await self.session.get(URL["oppio"])
            data = await response.json()

            self._version = data["current_version"]
            del data["current_version"]
            self._version_data.update(data)

            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeout error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["source"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happened! - %s", error)


def sorted_pypi_versions(response):
    """Sort list of pypi versions."""
    versions = [semantic_version.Version.coerce(version) for version in response]
    return sorted(
        versions,
        reverse=True,
        key=lambda k: (
            k.major,
            k.minor,
            k.patch,
            int(0 if not k.prerelease else re.sub(r"[a-z]", "", k.prerelease[0])),
        ),
    )


def extract_version(versionObject):
    """Extract version number from version object."""
    version = [versionObject.major, versionObject.minor, versionObject.patch]
    if versionObject.prerelease:
        return ".".join([str(v) for v in version]) + str(versionObject.prerelease[0])
    return ".".join([str(v) for v in version])
