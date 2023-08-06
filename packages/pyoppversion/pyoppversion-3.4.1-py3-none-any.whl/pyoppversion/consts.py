"""Constants for pyoppversion."""
from enum import Enum

BOARDS = {
    "default": "ova",
    "intel-nuc": "intel-nuc",
    "odroid-c2": "odroid-c2",
    "odroid-n2": "odroid-n2",
    "odroid-xu": "odroid-c2",
    "raspberrypi": "rpi",
    "raspberrypi2": "rpi2",
    "raspberrypi3-64": "rpi3-64",
    "raspberrypi3": "rpi3",
    "tinker": "tinker",
}

IMAGES = {
    "default": {"docker": "open-peer-power", "oppio": "default"},
    "intel-nuc": {"docker": "intel-nuc-openpeerpower", "oppio": "intel-nuc"},
    "odroid-c2": {"docker": "odroid-c2-openpeerpower", "oppio": "odroid-c2"},
    "odroid-n2": {"docker": "odroid-n2-openpeerpower", "oppio": "odroid-n2"},
    "odroid-xu": {"docker": "odroid-xu-openpeerpower", "oppio": "odroid-xu"},
    "qemuarm-64": {"docker": "qemuarm-64-openpeerpower", "oppio": "qemuarm-64"},
    "qemuarm": {"docker": "qemuarm-openpeerpower", "oppio": "qemuarm"},
    "qemux86-64": {"docker": "qemux86-64-openpeerpower", "oppio": "qemux86-64"},
    "qemux86": {"docker": "qemux86-openpeerpower", "oppio": "qemux86"},
    "raspberrypi": {"docker": "raspberrypi-openpeerpower", "oppio": "raspberrypi"},
    "raspberrypi2": {"docker": "raspberrypi2-openpeerpower", "oppio": "raspberrypi2"},
    "raspberrypi3-64": {
        "docker": "raspberrypi3-64-openpeerpower",
        "oppio": "raspberrypi3-64",
    },
    "raspberrypi3": {"docker": "raspberrypi3-openpeerpower", "oppio": "raspberrypi3"},
    "raspberrypi4-64": {
        "docker": "raspberrypi4-64-openpeerpower",
        "oppio": "raspberrypi4-64",
    },
    "raspberrypi4": {"docker": "raspberrypi4-openpeerpower", "oppio": "raspberrypi4"},
    "tinker": {"docker": "tinker-openpeerpower", "oppio": "tinker"},
}

URL = {
    "docker": "https://registry.hub.docker.com/v2/repositories/openpeerpower/{}/tags",
    "oppio": {
        "stable": "https://version.openpeerpower.io//stable.json",
        "beta": "https://version.openpeerpower.io//beta.json",
    },
    "pypi": "https://pypi.org/pypi/openpeerpower/json",
    "oppio": "https://www.openpeerpower.io//version.json",
}
