#!/bin/python
users = [ {'admin': True, 'active': True, 'name': 'Kevin'},
         {'admin': False, 'active': False, 'name': 'Mark'},
         {'admin': True, 'active': False, 'name' : 'Catherine'},
       ]

line = 1

for user in users:
    if user['admin'] and user['active']:
        print ("ACTIVE - ADMIN %s %s" % (line, user['name']))
    elif user['active']:
        print ("ACTIVE - %s %s" % (line, user['name']))
    elif user['admin']:
        print ("ACTIVE - %s %s" % (line, user['name']))
    else:
        print ("%s %s is neither admin of active " % (line, user['name']))
    line += 1



