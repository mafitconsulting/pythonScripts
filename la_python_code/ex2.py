#!/bin/python
user = {'admin': True, 'active': True, 'name': 'Kevin'}
if user['admin']:
    print("ADMIN %s" % user['name'])
elif user['active']:
    print("ACTIVE %s" % user['name'])
elif user['active'] and user['admin']:
    print("ACTIVE - (ADMIN) %s" % user['name'])
else:
    print("Users name " % user['name'])

