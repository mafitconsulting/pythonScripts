#!/bin/python
import argparse

#Define argument parser
parser = argparse.ArgumentParser(description='Search for words including partial word')

# Add argument
parser.add_argument('snippet',help='Partial or complete string to search for')
args = parser.parse_args()
#Convert text to lower case
snippet = args.snippet.lower()
# Read dict file
words = open('/usr/share/dict/words').readlines()
matches = []
for word in words:
    if snippet in word.lower():
        matches.append(word)
print(matches)

# Now with a list comprehension
print [word.strip() for word in words if snippet in word.lower()]

#replaces
#matches = []
#for word in words:
#  if snippet in word.lower():
#     matches.append(word)
#print(matches)
