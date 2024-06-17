#!/usr/bin/env python
from setuptools import find_packages, setup


project = "openapi"
version = "2.0.0"

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
        "inflection>=0.5.1",
        "jsonschema>=3.2.0",
    ],
    extras_require={
        "yaml": [
            "PyYAML>=3.12",
        ],
        "test": [
            "coverage>=7.5.3",
            "PyHamcrest>=2.1.0",
            "pytest-cov>=5.0.0",
            "pytest>=8.2.0",
            "pytest-cov>=5.0.0",
            "PyYAML>=6.0.1",
        ],
        "lint": [
            "flake8",
            "flake8-print",
            "flake8-isort",
        ],
        "typehinting": [
            "mypy",
            "types-psycopg2",
            "types-python-dateutil",
            "types-pytz",
            "types-setuptools",
            "types-PyYAML",
        ],
    },
    setup_requires=[
    ],
    dependency_links=[
    ],
    entry_points={
    },
    tests_require=[
        "coverage>=7.5.3",
        "PyHamcrest>=2.1.0",
        "pytest-cov>=5.0.0",
        "pytest>=8.2.0",
        "pytest-cov>=5.0.0",
        "PyYAML>=6.0.1",
    ],
)
