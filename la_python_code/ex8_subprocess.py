#!/bin/python

import subprocess
import os
from argparse import ArgumentParser

parser = ArgumentParser(description='kill the running process listening on a given port')
parser.add_argument('port', type=int, help='the port number to search for')

port = parser.parse_args().port

try:
    output = subprocess.check_output(['lsof', '-n', "-i4TCP:%s" % port])
except subprocess.CalledProcessError:
    print("No process listening on port %s" % port)
else:
    listening = None
    for line in output.splitlines():
        if "LISTEN" in line:
            listening = line
            break

    if listening:
        # PID is the second column in the output
        pid = int(listening.split()[1])
        os.kill(pid, 9)
        print("Killed process %s" % pid)
    else:
        print("No process listening on port %s" % port)
        exit(1)
