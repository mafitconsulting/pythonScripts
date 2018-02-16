#!/bin/python
import yaml
class Credentials():
    def __init__(self, filename):
        self.filename = filename

    def getCreds(self):
        config = {}
        with open (self.filename, 'r') as f:
            config = yaml.load(f)
        for item in config.values():
            user = item['user']
            password = item['password']
            server = item['server']
            return (user, password, server)

creds = Credentials('config.yaml')
print (creds.getCreds())
