# BinaryFileReader

## Description
This package read binary file to get all strings or read it like a hexareader.

## Requirements
This package require :
 - python3
 - python3 Standard Library

## Installation
```bash
pip install BinaryFileReader
```

## Launcher

## Command line:
```bash
GetStrings -h # get help message
GetStrings test.bin # get strings in test.bin
GetStrings -m 7 -M 1 test.dump # get strings with minimum length of 7 characters and with one non printable character between characters
HexaReader test.bin # Read test.bin as hexadecimal and ascii printable
```

### Python script
```python
from BinaryFileReader import Strings, HexaReader

hexareader = HexaReader("test.bin")
for line in hexareader.reader():
    print(line)

strings = Strings("test.bin")
for line in strings.reader():
    print(line)

strings = Strings("test.dmp", chars=b"abcdeABCDE0123./$", minimum_chars=7, number_bad_chars=1, accepted_bad_chars=b'\x00', encoding="latin1")
for line in strings.reader():
    print(line)
```

### Python executable:
```bash
python3 BinaryFileReader.pyz strings -m 7 -M 1 test.dump
python3 BinaryFileReader.pyz strings test.bin

# OR
chmod u+x BinaryFileReader.pyz # add execute rights
./BinaryFileReader.pyz hexareader test.bin # execute file
```

### Python module (command line):

```bash
python3 -m BinaryFileReader hexareader test.bin
python3 -m BinaryFileReader.Strings -m 7 -M 1 test.dump
```

## Links
 - [Github Page](https://github.com/mauricelambert/BinaryFileReader/)
 - [Documentation](https://mauricelambert.github.io/info/python/code/BinaryFileReader.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/code/BinaryFileReader.pyz)
 - [Pypi package](https://pypi.org/project/BinaryFileReader/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
