#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file show int, hexa, binary and latin1 from int, hexa, binary or latin1.
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

""" This file show int, hexa, binary and latin1 from int, hexa, binary or latin1.
>>> a = LatinUtilities()
>>> a.from_string("abc")
('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
>>> str(a)
'TEXT: abc\\nINT: 97 98 99\\nHEXA: 61 62 63\\nBINARY: 1100001 1100010 1100011'
>>> print(a)
TEXT: abc
INT: 97 98 99
HEXA: 61 62 63
BINARY: 1100001 1100010 1100011
"""

# To test this file/class launch this command:
# python3 -m doctest -v LatinUtilities.py

from binascii import hexlify
from base64 import b16decode
from typing import List, Tuple
from sys import argv


class LatinUtilities:

    """ This class show int, hexa, binary and latin1 from int, hexa, binary or latin1.

    >>> a = LatinUtilities()
    >>> a.from_string("abc")
    ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
    >>> str(a)
    'TEXT: abc\\nINT: 97 98 99\\nHEXA: 61 62 63\\nBINARY: 1100001 1100010 1100011'
    >>> print(a)
    TEXT: abc
    INT: 97 98 99
    HEXA: 61 62 63
    BINARY: 1100001 1100010 1100011
    """

    def __init__(self):
        self.string: str = None
        self.bin: List[str] = None
        self.hexa: str = None
        self.int: List[int] = None

    def __str__(self) -> str:
        return f"TEXT: {self.text}\nINT: {' '.join([str(x) for x in self.int])}\nHEXA: {self.hexa}\nBINARY: {' '.join(self.bin)}"

    def from_string(self, text: str) -> Tuple[str, List[int], str, List[str]]:

        """Get int, hexa and binary from string.

        >>> a = LatinUtilities()
        >>> a.from_string("abc")
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        """

        self.text = text
        self.int = [ord(car) for car in text]
        self.hexa = hexlify(text.encode("latin"), " ").decode()
        self.bin = [bin(number)[2:] for number in self.int]

        return (self.text, self.int, self.hexa, self.bin)

    def from_int(self, numbers: list) -> Tuple[str, List[int], str, List[str]]:

        """Get string, hexa and binary from list of int.

        >>> a = LatinUtilities()
        >>> a.from_int([97, 98, 99])
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        """

        self.int = numbers
        self.text = bytes(numbers).decode("latin1")
        self.hexa = hexlify(self.text.encode("latin"), " ").decode()
        self.bin = [bin(number)[2:] for number in self.int]

        return (self.text, self.int, self.hexa, self.bin)

    def from_bytes(self, encoded: bytes) -> Tuple[str, List[int], str, List[str]]:

        """Get string, hexa, int and binary from bytes.

        >>> a = LatinUtilities()
        >>> a.from_bytes(b'abc')
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        """

        return self.from_int([x for x in encoded])

    def from_hexa(self, hexa: str) -> Tuple[str, List[int], str, List[str]]:

        """Get string, int and binary from hexa.
         - formats accepted: "a1 b4 ff", "A1B4FF" and "A1-b4-Ff"

        >>> a = LatinUtilities()
        >>> a.from_hexa('61 62 63')
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        >>> a.from_hexa('61:62:63')
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        >>> a.from_hexa('61-62-63')
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        >>> a.from_hexa('616263')
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        >>> a.from_hexa("5e 6F4f")
        ('^oO', [94, 111, 79], '5e 6f 4f', ['1011110', '1101111', '1001111'])
        """

        hexa = hexa.replace(" ", "").replace(":", "").replace("-", "").upper()
        return self.from_bytes(b16decode(hexa.encode()))

    def from_bin(self, binary: str) -> Tuple[str, List[int], str, List[str]]:

        """Get string, hexa, and int from binary.
         - format accepted: "1100001 1100010 1100011"

        >>> a = LatinUtilities()
        >>> a.from_bin('1100001 1100010 1100011')
        ('abc', [97, 98, 99], '61 62 63', ['1100001', '1100010', '1100011'])
        """

        return self.from_int([int(x, 2) for x in binary.split()])


def main() -> None:
    help_message = """USAGE: python3 LatinUtilities.py [OPTION] ascii
    OPTION:
        type {integers, string, binary, hexa} (default: string)

    ascii - formats:
        if type is integers: "97,98,99"
        if type is string: "abc"
        if type is binary: "1100001 1100010 1100011"
        if type is hexa:
            "61 62 63", "61-62-63", "61:62:63", "616263", "fF aB:6D-6d"
    """

    if len(argv) == 2:
        string = argv[1]
        type_ = "string"
    elif len(argv) == 3:
        _, type_, string = argv
    else:
        type_ = ""

    ascii_ = LatinUtilities()
    show_help = True

    if type_ == "integers":
        show_help = False
        ascii_.from_int([int(x) for x in string.split(",")])
    elif type_ == "string":
        show_help = False
        ascii_.from_string(string)
    elif type_ == "binary":
        show_help = False
        ascii_.from_bin(string)
    elif type_ == "hexa":
        show_help = False
        ascii_.from_hexa(string)

    if show_help:
        print(help_message)
        exit(1)
    else:
        print(ascii_)
        exit(0)


if __name__ == "__main__":
    main()
