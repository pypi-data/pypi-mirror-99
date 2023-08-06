#!/usr/bin/env python3

from pathlib import Path

from setuptools import setup

script_dir = Path(__file__).parent

# Gets the long description from the README.md file
readme_filepath = script_dir / "README.md"
with readme_filepath.open("rt", encoding="utf-8") as fd:
    LONG_DESCRIPTION = fd.read()

setup(
    name="validata_ui",
    version="0.5.0a4",
    description="Validata Web UI",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://git.opendatafrance.net/validata/validata-ui",
    author="Validata team",
    author_email="admin-validata@jailbreak.paris",
    license="AGPLv3",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU Affero General Public License v3",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "commonmark",
        "ezodf",
        "flask",
        "frictionless >= 4.*",
        "lxml",
        "pydantic",
        "python-dotenv",
        "pyyaml",
        "requests",
        "requests_cache",
        "toml",
        "opendataschema",
        "validata_core >= 0.7.0a1",
    ],
    extras_require={
        "sentry": [
            "sentry-sdk[flask]",
        ]
    },
    packages=["validata_ui"],
    include_package_data=True,
    package_data={"validata_ui": ["templates/*", "static/*", "static/**/*"]},
    zip_safe=True,
)
