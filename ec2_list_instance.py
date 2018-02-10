#!/usr/bin/python

import boto3
import botocore
import logging

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def disableAPIProtection(instance):
    try:
        response = client.modify_instance_attribute(
                InstanceId=instance,
                DisableApiTermination={
                    'Value': False
                    }
                )
        print("API termination disabled")
    except botocore.exceptions.ClientError as e:
         print (e.response['Error']['Code'])


instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for instance in instances:
    try:
        logging.info("Deleting instance %s " % instance.id)
        disableAPIProtection(instance.id)
        response = instance.terminate()
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        print (e.response['Error']['Code'])
