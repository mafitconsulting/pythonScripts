#!/usr/bin/env python

import sys
import requests
import argparse

parser = argparse.ArgumentParser(description='URL request')
parser.add_argument('url', help='URL for request')
parser.add_argument('filename', help='Enter destination filename')
parser.add_argument('--content-type', '-c',
                     default='html',
                     choices=['html', 'json'],
                     help='the content-type of the URL being requested')
args = parser.parse_args()

res = requests.get(args.url)

if res > '400':
    print ("Error returning request")
else:
    if args.content_type == 'json':
        try:
             content = res.json()
        except ValueError:
             print("Error: Content is not JSON")
             sys.exit(1)
    else:
        content = res.text

    with open(args.filename, 'w') as f:
        f.write(content.encode("UTF-8"))
        print("Content written to '%s'" % args.filename)

