#!/usr/bin/python
"""
EC2 Boto intrumentation script
"""


import sys
import logging
import boto3
from switch import switch
import botocore

def usage(option):
    """ Usage function """
    print "\nUSAGE: " + option + "\n"
    for case in switch(option):
        if case('default'):
            print """
                Options are: ./ec2_instance <option>
                create_instance
                delete_instance
                query_instances
                control_instances
            """
        break

def create_instance():
    """ Creates EC2 Instance """
    try:
        if len(sys.argv) < 1:
            usage('create-instance')
        else:
            logging.info("Creating EC2 Instance ")
            instance = ec2.create_instances(
                ImageId='ami-6f587e1c',
                MinCount=1,
                MaxCount=1,
                InstanceType='t2.micro')
            print instance[0].id
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def delete_instance():
    """ Deletes EC2 Instance """
    try:
        logging.info("Deleting instance " + sys.argv[2:])
        for instance_id in sys.argv[2:]:
            instance = ec2.Instance(instance_id)
            response = instance.terminate()
            print response
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def query_instances():
    """ Queries EC2 Instance ID for current state """
    try:
        logging.info("Checking for instances.....")
        for instance in ec2.instances.all():
            print instance.tags, instance.id, instance.public_ip_address, instance.state 
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def control_instances():
    """ Controls the state of instances """
    try:
        logging.info("Attempting to " + sys.argv[3] + " the instance " +  sys.argv[2])
        if sys.argv[3] == 'stop':
            print "Stopping Instance ID " + sys.argv[2]
            ec2.Instance(id=sys.argv[2]).stop()
        elif sys.argv[3] == 'start':
            print "Starting Instance ID " + sys.argv[2]
            ec2.Instance(id=sys.argv[2]).start()
        elif sys.argv[3] == 'terminate':
            print "Terminating Instance ID " + sys.argv[2]
            ec2.instance(id=sys.argv[2]).terminate()
        else:
            print "Not a valid argument. Supports (stop|start|terminate)"
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

if __name__ == '__main__':

    """Takes ACTION argument from cmd line"""
    try:
        ACTION = sys.argv[1]
    except IndexError:
        usage('default')
    """Set boto resource to ec2"""
    ec2 = boto3.resource('ec2')

    """Sets up logging"""
    logging.basicConfig(filename='aws_s3.log',
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    """ Dispatch structure for ACTION """
    for case in switch(ACTION):
        if case('create-instance'):
            create_instance()
            break
        if case('delete-instance'):
            delete_instance()
            break
        if case('query-instances'):
            query_instances()
            break
        if case('control-instances'):
            control_instances()
            break
        if case():
            print "No instance option initiated"
            break
