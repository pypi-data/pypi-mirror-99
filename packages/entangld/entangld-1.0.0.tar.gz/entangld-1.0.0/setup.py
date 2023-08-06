import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="entangld",
    version="1.0.0",
    author="Jonathan D B Van Schenck",
    author_email="jvschenck@novadynamics.com",
    description="Synchronized key-value stores with RPCs and pub/sub events. (Port of node.js version)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaxBot/python-entangld",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
