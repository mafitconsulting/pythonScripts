#!/bin/python
import json
import os
import glob
import shutil

try:
    os.mkdir("./processed")
except OSError:
    print ("Directory already exists")

#Get a list of receipts
receipts = glob.glob('./new/receipt-[0-9]*.json')

subtotal = 0.0

#Iterate over the receipts
# read contrent and tally total
# mv the file to the processed directory
# print that we processed the file
for path in receipts:
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content['value'])
    name = path.split('/')[-1]
    destination = "./processed/%s" % name
    shutil.move(path, destination)
    print("Moved '%s' to '%s'" % (path,destination))

#Print the subtotal of all processed receipts
print ("Receipt subtotal: $%.2f" % subtotal)
