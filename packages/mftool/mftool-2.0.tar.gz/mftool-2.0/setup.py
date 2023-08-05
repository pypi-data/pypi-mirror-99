from setuptools import setup, Extension ,find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
	
setup(
    name="mftool",
    version="2.0",
    author="Sujit Nayakwadi",
    author_email="nayakwadi.sujit@gmail.com",
    description="Library for getting real time Mutual funds data in India",
    license="MIT",
    keywords="amfi, quote, mutual-funds, funds, bse, nse, stock, stocks",
    install_requires=['requests','bs4'],
    url="https://github.com/NayakwadiS/mftool",
    packages=find_packages(),
	long_description = long_description,
	long_description_content_type='text/markdown',
	package_data = {'': ['*.json']}
)
