#!/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='the file to read')
parser.add_argument('linenumber',type=int, help='The line number')
args = parser.parse_args()

try:
    lines = open(args.filename, 'r').readlines()
    line = lines[args.linenumber - 1]
except IndexError:
    print("Error file '%s' doesnt have %i lines" % (args.filename, args.linenumber))
except IOError as err:
    print("Error: File not found")
else:
    print(line)


