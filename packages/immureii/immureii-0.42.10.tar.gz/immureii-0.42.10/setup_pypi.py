#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="immureii",
    version="0.42.10",
    author="Scott McCallum (sr.ht/~scott91e1)",
    author_email="cto@immureii.com",
    description="Immure Iniquitous Intent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/immureii/immureii",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: SQL",
        "Programming Language :: Forth",
        "Programming Language :: JavaScript",
        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Internet",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Version Control",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: System :: Software Distribution",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.7",
)
