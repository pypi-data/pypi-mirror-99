"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pyoppversion",
    version="3.4.1",
    author="Paul Caston",
    author_email="paul@caston.id.au",
    description="",
    long_description=LONG,
    install_requires=[
        "aiohttp",
        "async_timeout<=3.0.1",
        "pytest-runner",
        "semantic_version",
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pyoppversion",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
