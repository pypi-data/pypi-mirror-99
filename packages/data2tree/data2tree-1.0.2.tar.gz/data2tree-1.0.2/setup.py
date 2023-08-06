# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Author:       01
# Date:         2021-03-22 13:26
# Description:  

# -------------------------------------------------------------------------------
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data2tree",
    version="1.0.2",
    author="01",
    author_email="zerone40@163.com",
    description="Python Generate the data tree recursively",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zerone40",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

)