#!/usr/bin/python

import boto3
import botocore
import logging

client = boto3.client('ec2')

def disableAPIProtection(instance):
    try:
        apiresp = client.modify_instance_attribute(
                      InstanceId=instance,
                      DisableApiTermination={
                           'Value': False
                      }
                      print("API termination disabled")
    except botocore.exceptions.ClientError as e:
        print (e.response['Error']['Code'])



ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
tags = ['openshift-node','openshift-master','JenkinsBuildServer']
ec2 = boto3.resource('ec2', regions_name='eu-west-1')
instances = ec2.instances.filter(
                 Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for region in ec2_regions:
    for instance in instances:
        try:
            ec2 = boto3.resource('ec2', regions_name=region)
            logging.info("Deleting instance %s " % instance.id)
            for tag in instance.tags:
                if tag['Value'] in tags:
                    pass
                else:
                                                                                                                                                                                    response = instance.terminate()
                                                                                                                                                                          except botocore.exceptions.ClientError as e:
             logging.error(e.response['Error']['Code'])
             print (e.response['Error']['Code'])
