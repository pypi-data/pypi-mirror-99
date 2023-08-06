#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file implement a HexaReader (read binary file as hexa and ascii).
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

""" This file implement a HexaReader (read binary file as hexa and ascii).

>>> with open("test", 'wb') as f: f.write(b"\\x00abc")
4
>>> hexareader = HexaReader("test")
>>> for line in hexareader.reader(): print(line)
00 61 62 63                                  .abc
>>> import os; os.remove("test")
"""

from typing import Generator
from binascii import hexlify
from os import path
from sys import argv


class HexaReader:

    """This class implement a hexadecimal reader for binary file.

    >>> with open("test", 'wb') as f: f.write(b"\\x00abc")
    4
    >>> hexareader = HexaReader("test")
    >>> for line in hexareader.reader(): print(line)
    00 61 62 63                                  .abc
    >>> import os; os.remove("test")
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.chars = (
            "0123456789"
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "!\"\#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        ).encode()

    def reader(self) -> Generator[str, None, None]:

        """This function read file 16 chars by 16 chars and yield lines.

        >>> with open("test", 'wb') as f: f.write(b"\\x00abc")
        4
        >>> hexareader = HexaReader("test")
        >>> for line in hexareader.reader(): print(line)
        00 61 62 63                                  .abc
        >>> import os; os.remove("test")
        """

        data = b" "

        with open(self.filename, "rb") as file:
            while data:
                data = file.read(16)

                if data:
                    yield self.get_line(data)

    def get_line(self, data: bytes) -> str:

        """This function return hexareader line from bytes.

        >>> hexareader = HexaReader(None)
        >>> hexareader.get_line(b"\\x00\\x01")
        '00 01                                        ..'
        """

        hexa = "{:<55}".format(hexlify(data, " ").decode())

        ascii_ = ""
        for char in data:
            if char in self.chars:
                ascii_ += chr(char)
            else:
                ascii_ += "."

        return hexa + ascii_


def main() -> None:

    """This function parse arguments and return error."""

    if len(argv) != 2:
        print("USAGE: python3 HexaReader.py filename")
        exit(1)
    elif not path.exists(argv[1]):
        print(f"ERROR: file {argv[1]} doesn't exist.")
        exit(2)
    else:
        hexareader = HexaReader(argv[1])
        for line in hexareader.reader():
            print(line)
        exit(0)


if __name__ == "__main__":
    main()
