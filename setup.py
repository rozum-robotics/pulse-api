import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

def read_version() -> str:
    file_path = here / "version"
    with open(file_path) as version_file:
        return version_file.read().strip()

def development_status(version: str) -> str:
    if "a" in version:
        dev_status = "Development Status :: 3 - Alpha"
    elif "dev" in version or "rc" in version:
        dev_status = "Development Status :: 4 - Beta"
    else:
        dev_status = "Development Status :: 5 - Production/Stable"
    return dev_status

def long_description(short_description: str) -> str:
    readme_path = here / "README.md"
    try:
        with open(readme_path,  encoding="utf-8") as readme:
            long_description = "\n" + readme.read()
            return long_description
    except FileNotFoundError:
        return short_description

NAME = "pulse-api"
DESCRIPTION = "Python API for Pulse Robotic Arm with useful utilities"
URL = "https://rozum.com"
EMAIL = "dev@rozum.com"
AUTHOR = "Rozum Robotics"
VERSION = read_version()
DEVELOPMENT_STATUS = development_status(VERSION)
LONG_DESCRIPTION = long_description(DESCRIPTION)

REQUIRED = [
    "certifi >= 2019.3.9",
    "six >= 1.10",
    "python_dateutil == 2.8.0",
    "urllib3 >= 1.24.2",
    "pdhttp >= 1.8.1.dev20200804140542,<1.9.0",
    "Deprecated == 1.2.6",
]


setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=REQUIRED,
    url=URL,
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        DEVELOPMENT_STATUS,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    zip_safe=False,
)
