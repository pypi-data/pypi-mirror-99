from setuptools import setup, find_packages
import BinaryFileReader

setup(
    name = "BinaryFileReader",
 
    version = BinaryFileReader.__version__,
    packages = find_packages(),
    install_requires = [],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package read binary file to get all strings or read it like a hexareader.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/BinaryFileReader',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
 
    entry_points = {
        'console_scripts': [
            'GetStrings = BinaryFileReader:get_strings',
            'HexaReader = BinaryFileReader:hexaread',
        ],
    },
    python_requires='>=3.6',
)