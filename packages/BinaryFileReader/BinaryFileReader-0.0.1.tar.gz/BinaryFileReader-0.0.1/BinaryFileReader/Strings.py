#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file found strings in binary file.
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

""" This file found strings in binary file.

>>> with open("test", 'wb') as f: f.write(b"\\x00\\x01abcde\\x00\\x01")
9
>>> strings = Strings("test")
>>> for line in strings.reader(): print(line)
abcde
>>> import os; os.remove("test")
"""

from typing import Generator
from argparse import ArgumentParser


class Strings:

    """This class implement a Strings getter from binary file.

    >>> with open("test", 'wb') as f: f.write(b"abc\\x00\\x01ab\\x00cdeF\\x00\\x01")
    14
    >>> strings = Strings("test", chars=b"abcde", minimum_chars=3, number_bad_chars=1, accepted_bad_chars=b"\\x00")
    >>> for line in strings.reader(): print(line)
    abc
    abcde
    >>> import os; os.remove("test")
    """

    def __init__(
        self,
        filename: str,
        chars: bytes = (
            b"0123456789"
            b"abcdefghijklmnopqrstuvwxyz"
            b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            b"!\"\#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        ),
        minimum_chars: int = 5,
        number_bad_chars: int = 0,
        accepted_bad_chars: bytes = b"",
        encoding: str = "latin1",
    ):
        self.chars = chars
        self.minimum_chars = minimum_chars
        self.filename = filename
        self.number_bad_chars = number_bad_chars
        self.accepted_bad_chars = accepted_bad_chars
        self.current_string: str = ""
        self.current_bad_chars: int = 0
        self.encoding = encoding

    def reader(self) -> Generator[str, None, None]:

        """This function read file 1 chars by 1 chars and yield lines.

        >>> with open("test", 'wb') as f: f.write(b"abc\\x00\\x01ab\\x00cdeF\\x00\\x01")
        14
        >>> strings = Strings("test", chars=b"abcde", minimum_chars=3, number_bad_chars=1, accepted_bad_chars=b"\\x00")
        >>> for line in strings.reader(): print(line)
        abc
        abcde
        >>> import os; os.remove("test")
        """

        char = b" "

        with open(self.filename, "rb") as file:
            while char:
                char = file.read(1)

                if char:
                    string = self.analyse_char(char)
                    if string:
                        yield string

        if len(self.current_string) >= self.minimum_chars:
            yield self.current_string

    def analyse_char(self, char: bytes) -> str:

        """This function analyse a byte and return strings found.

        >>> strings = Strings(None)
        >>> [strings.analyse_char(x) for x in (b"a", b"b", b"c", b"d", b"e", b"\\x00")]
        [None, None, None, None, None, 'abcde']
        >>> strings = Strings(None, number_bad_chars=1)
        >>> [strings.analyse_char(x) for x in (b"a", b"b", b"\\x00", b"c", b"d", b"e", b"\\x00", b"\\x00")]
        [None, None, None, None, None, None, None, 'abcde']
        >>> strings = Strings(None, number_bad_chars=1, accepted_bad_chars=b"\\x00")
        >>> [strings.analyse_char(x) for x in (b"a", b"b", b"\\x00", b"c", b"d", b"e", b"\\x00", b"\\x00")]
        [None, None, None, None, None, None, None, 'abcde']
        >>> strings = Strings(None)
        >>> [strings.analyse_char(x) for x in (b"a", b"b", b"\\x00", b"c", b"d", b"e", b"\\x00", b"\\x00")]
        [None, None, None, None, None, None, None, None]
        >>> strings = Strings(None, number_bad_chars=1, accepted_bad_chars=b"\\x01")
        >>> [strings.analyse_char(x) for x in (b"a", b"b", b"\\x00", b"c", b"d", b"e", b"\\x00", b"\\x00")]
        [None, None, None, None, None, None, None, None]
        """

        if char in self.chars:
            self.current_string += char.decode(self.encoding)
            self.current_bad_chars = 0
            return

        elif (self.accepted_bad_chars and char in self.accepted_bad_chars) or (
            not self.accepted_bad_chars
        ):
            self.current_bad_chars += 1
            string = self.current_string

            if (
                self.current_bad_chars > self.number_bad_chars
                and len(string) >= self.minimum_chars
            ):
                self.current_string = ""
                return string

            elif self.current_bad_chars > self.number_bad_chars:
                self.current_string = ""
                return

        else:
            string = self.current_string
            self.current_bad_chars = 0
            self.current_string = ""

            if len(string) >= self.minimum_chars:
                return string
            return


def main() -> None:

    """This function parse arguments and return error."""

    parser = ArgumentParser()
    parser.add_argument("filename", help="Filename of binary file.")
    parser.add_argument(
        "--min-chars",
        "-m",
        type=int,
        default=5,
        help="Minimum length to print a string.",
    )
    parser.add_argument(
        "--max-bad-chars",
        "-M",
        type=int,
        default=0,
        help="Maximum bad characters in string.",
    )
    args = parser.parse_args()

    strings = Strings(
        args.filename, minimum_chars=args.min_chars, number_bad_chars=args.max_bad_chars
    )
    for line in strings.reader():
        print(line)
    exit(0)


if __name__ == "__main__":
    main()
