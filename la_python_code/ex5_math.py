#!/bin/python

from os import getenv
from math import pi

digits = getenv("DIGITS") or 10
print("%.*f" % (int(digits), pi))
