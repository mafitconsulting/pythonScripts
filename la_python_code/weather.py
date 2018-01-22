#!/usr/bin/env python
import os
import requests
import sys
from argparse import ArgumentParser

parser = ArgumentParser(description='Get the current weather information')
parser.add_argument('zip', help='post code')
parser.add_argument('country', help='county')
args = parser.parse_args()

url = "http://api.openweathermap.org/data/2.5/weather?zip=%s,%s" % (
       args.zip,
       args.country,
       os.getenv("OWM_API_KEY"))
res = requests.get(url)

if res.status_code != 200:
   print("Error talking to weather api %s" % res.status_code)
   sys.exit(1)

print(res.json())

