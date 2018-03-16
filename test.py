#!/bin/python
import yaml
import os
import sys
import json


def programmatic_access(user):
    print ("programmatic access for %s" % user)

def console_access(user):
    print ("console access for %s" % user)

def configure_mfa(user):
    print ("mfa access for %s" % user)

user = sys.argv[1]

try:
    f = open('users.yaml')
except IOError as err:
    print("Error: %s" % err)
else:
    with f:
        config = yaml.load(f)

        if config[user]:
            policy = config[user]['policies']
            programmatic = config[user]['programmatic']
            console = config[user]['console']
            mfa = config[user]['mfa']

            #print ("programmatic: %s console: %s mfa: %s" % (programmatic,console,mfa))
            dispatch_dict = {
                    'programmatic': programmatic_access,
                    'console' :  console_access,
                    'mfa'     :  configure_mfa
            }

            for k, v in config[user].items():
                if k in ('programmatic','console','mfa') and v is True:
                    print ("Key: %s Value: %s" % (k,v))
                    handler = dispatch_dict[k]
                    handler(user)



