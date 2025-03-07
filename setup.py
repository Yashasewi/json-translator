#!/usr/bin/env python3
"""Setup script for JSON Translator."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="json-translator",
    version="1.0.0",
    author="JSON Translator Team",
    author_email="example@example.com",
    description="A tool for translating JSON language files to multiple languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/json-translator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cachetools>=4.2.4",
        "certifi>=2025.1.31",
        "charset-normalizer>=3.4.1",
        "google-api-core>=1.34.1",
        "google-auth>=1.35.0",
        "google-cloud-core>=1.7.3",
        "google-cloud-translate>=2.0.1",
        "googleapis-common-protos>=1.69.1",
        "grpcio>=1.71.0rc2",
        "grpcio-status>=1.49.0rc1",
        "idna>=3.10",
        "markdown-it-py>=3.0.0",
        "mdurl>=0.1.2",
        "protobuf>=3.20.3",
        "pyasn1>=0.6.1",
        "pyasn1_modules>=0.4.1",
        "Pygments>=2.19.1",
        "requests>=2.32.3",
        "rich>=13.3.5",
        "rsa>=4.9",
        "setuptools>=75.8.2",
        "six>=1.17.0",
        "urllib3>=2.3.0",
        "python-dotenv>=1.0.0",
        "google-api-python-client>=2.97.0",
    ],
    entry_points={
        "console_scripts": [
            "json-translator=json_translator.main:main",
        ],
    },
) 