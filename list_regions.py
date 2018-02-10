#!/bin/python
import boto3

client = boto3.client('ec2')

ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

for region in ec2_regions:
    print region
