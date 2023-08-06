# IBM Confidential - OCO Source Materials
# (C) Copyright IBM Corp. 2020
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.

__author__ = "IBM"

import setuptools


def main():
    setuptools.setup(
        name="nba2liteserver",
        author="IBM",
        author_email="<lalala@gmail.com>",
        version="1.0.1",
        description="NBA2 lite server",
        long_description="Lite server to generate and handle models",
        long_description_content_type="text/markdown",
        url="",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    )


main()
