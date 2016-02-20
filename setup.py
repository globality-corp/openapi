#!/usr/bin/env python
from setuptools import find_packages, setup

project = "openapi"
version = "0.2.0"

setup(
    name=project,
    version=version,
    description="Python OpenAPI 2.0 (Swagger) object model",
    long_description=open("README.md").read(),
    author="Jesse Myers",
    author_email="jesse.myers@gmail.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    keywords="openapi swagger",
    install_requires=[
        "inflection>=0.3.1",
        "jsonschema>=2.5.1",
    ],
    extras_require={
        "yaml": [
            "PyYAML>=3.11",
        ],
    },
    setup_requires=[
        "nose>=1.3.7",
    ],
    tests_require=[
        "coverage>=4.0.3",
        "mock>=1.3.0",
        "PyHamcrest>=1.8.5",
    ],
)
