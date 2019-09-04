#!/usr/bin/env python
from setuptools import find_packages, setup

project = "openapi"
version = "1.1.1"

setup(
    name=project,
    version=version,
    description="Python OpenAPI 2.0 (Swagger) object model",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/openapi",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    keywords="openapi swagger",
    install_requires=[
        "inflection>=0.3.1",
        "jsonschema[format]>=2.6.0",
    ],
    extras_require={
        "yaml": [
            "PyYAML>=3.12",
        ],
    },
    setup_requires=[
        "nose>=1.3.6",
    ],
    dependency_links=[
    ],
    entry_points={
    },
    tests_require=[
        "coverage>=3.7.1",
        "mock>=1.0.1",
        "PyHamcrest>=1.8.5",
    ],
)
