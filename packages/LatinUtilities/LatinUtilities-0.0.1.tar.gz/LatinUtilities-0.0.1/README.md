# LatinUtilities

## Description
This package show int, hexa, binary and latin1 from int, hexa, binary or latin1.

## Requirements
This package require :
 - python3
 - python3 Standard Library

## Installation
```bash
pip install LatinUtilities
```

## Launcher

## Command line:
```bash
LatinUtilities abc # get int, hexa, binary and latin1 from latin1
LatinUtilities string abc # get int, hexa, binary and latin1 from latin1
LatinUtilities integers 97,98,99 # get int, hexa, binary and latin1 from int
LatinUtilities binary "1100001 1100010 1100011" # get int, hexa, binary and latin1 from binary
LatinUtilities hexa "61 62 63" # get int, hexa, binary and latin1 from hexa
LatinUtilities hexa "61:62:63" # get int, hexa, binary and latin1 from hexa
LatinUtilities hexa "61-62-63" # get int, hexa, binary and latin1 from hexa
```

### Python script
```python
from LatinUtilities import LatinUtilities
latin = LatinUtilities()
latin1, int_list, hexa, binary_list = latin.from_bin('1100001 1100010 1100011')
latin1, int_list, hexa, binary_list = latin.from_hexa('61 62 63')
latin1, int_list, hexa, binary_list = latin.from_string('abc')
latin1, int_list, hexa, binary_list = latin.from_bytes(b'abc')
latin1, int_list, hexa, binary_list = latin.from_int([97, 98, 99])
print(latin)
```

### Python executable:
```bash
python3 LatinUtilities.pyz abc

# OR
chmod u+x LatinUtilities.pyz # add execute rights
./LatinUtilities.pyz hexa "61-62-63" # execute file
```

### Python module (command line):

```bash
python3 -m LatinUtilities integers 97,98,99
python3 -m LatinUtilities.LatinUtilities binary "1100001 1100010 1100011"
```

## Links
 - [Github Page](https://github.com/mauricelambert/LatinUtilities/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/LatinUtilities.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/security/LatinUtilities.pyz)
 - [Pypi package](https://pypi.org/project/LatinUtilities/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
