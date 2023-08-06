from setuptools import setup
from setuptools import find_packages


setup(
    name="subsparser",
    version="0.0.6",
    description="subtitle parser for srt and text",
    author="Dharmveer Baloda",
    packages=find_packages(),
    install_requires=['chardet'],
    url="https://github.com/baloda/subparser"
)