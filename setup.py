# Make pip installable

from setuptools import setup, find_packages 

setup(
    name="datastack",
    version="0.1.0",
    packages=find_packages(),
)