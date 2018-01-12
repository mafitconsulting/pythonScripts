#!/bin/python
import subprocess

# call example
code = subprocess.call(['ls', '-l'])

if code == 0:
    print ("Command finished sucessfully")
else:
    print("failed with code: %i" % code)

#Check output example
try:
    output = subprocess.check_output(
             ['ls', 'fake.txt'],
             stderr=subprocess.STDOUT)
except OSError as err:
    print ("Caught OSError")
    output = err
except subprocess.CalledProcessError as err:
    print ("Caught CAlledProcessError")
    output = err

print(output)
