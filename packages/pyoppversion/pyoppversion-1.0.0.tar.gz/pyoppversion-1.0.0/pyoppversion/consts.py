"""Constants for pyoppversion."""
from enum import Enum

DEFAULT_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent": "python/pyoppversion",
    "Content-Type": "application/json",
}

DATA_AUDIO = "audio"
DATA_BOARD = "board"
DATA_CHANNEL = "channel"
DATA_CLI = "cli"
DATA_OPENPEERPOWER = "openpeerpower"
DATA_DNS = "dns"
DATA_OPPOS = "oppos"
DATA_OS = "os"
DATA_IMAGE = "image"
DATA_MULTICAST = "multicast"
DATA_RELEASES = "releases"
DATA_OBSERVER = "observer"
DATA_RAW = "raw"
DATA_INFO = "info"
DATA_VERSION = "version"
DATA_SOURCE = "source"
DATA_SUPERVISOR = "supervisor"
DATA_CURRENT_VERSION = "current_version"
DATA_RELEASE_DATE = "release_date"
DATA_RELEASE_NOTES = "release_notes"
DATA_RELEASE_TITLE = "release_title"
DATA_RELEASE_DESCRIPTION = "release_description"


class OppVersionSource(str, Enum):
    """Valid sources for pyoppversion."""

    DOCKER = "docker"
    OPPIO = "oppio"
    LOCAL = "local"
    PYPI = "pypi"
    SUPERVISED = "supervised"

    DEFAULT = LOCAL


class OppVersionChannel(str, Enum):
    """Valid version channels."""

    BETA = "beta"
    DEV = "dev"
    STABLE = "stable"

    DEFAULT = STABLE


class OppVersionBoard(str, Enum):
    """Boards for OppVersion."""

    GENERIC_X86_64 = "generic-x86-64"
    INTEL_NUC = "intel-nuc"
    ODROID_C2 = "odroid-c2"
    ODROID_C4 = "odroid-c4"
    ODROID_N2 = "odroid-n2"
    ODROID_XU = "odroid-xu"
    OVA = "ova"
    RASPBERRYPI = "rpi"
    RASPBERRYPI2 = "rpi2"
    RASPBERRYPI3 = "rpi3"
    RASPBERRYPI364 = "rpi3-64"
    RASPBERRYPI4 = "rpi4"
    RASPBERRYPI464 = "rpi4-64"
    TINKER = "tinker"

    DEFAULT = OVA
