#!/bin/python
import json
import os
import glob
import shutil
import re
import math

try:
    os.mkdir("./processed")
except OSError:
    print ("Directory already exists")

#Get a list of receipts
#receipts = glob.glob('./new/receipt-[0-9]*.json')
receipts = [f for f in  glob.iglob('./new/receipt-[0-9]*.json') if re.match('./new/receipt-[0-9]*[02469].json', f)]
subtotal = 0.0

#Iterate over the receipts
# read contrent and tally total
# mv the file to the processed directory
# print that we processed the file
for path in receipts:
    with open(path) as f:
        content = json.load(f)
        subtotal += math.ceil(float(content['value']))
    name = path.split('/')[-1]
    destination = "./processed/%s" % name
    destination = path.replace('new', 'processed')
    shutil.move(path, destination)
    print("Moved '%s' to '%s'" % (path,destination))

#Print the subtotal of all processed receipts
print ("Receipt subtotal: $%.2f" % subtotal)
