#!/bin/python
import jenkins
from credentials import

creds = Credentials('config.yaml')
print (creds.getCreds())

