#!/usr/bin/python

import boto3
import botocore


# set up boto3 client
client = boto3.client('ec2',region_name='eu-west-1')



#Function enables EC2 Termination Protection
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



def main():

    import logging

    # Set up logging
    logging.basicConfig(filename='ec2-termination.log',
            format='%(asctime)s = %(levelname)s: %(message)s',
            level=logging.DEBUG)

    # List comprehension for regions
    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

    # tag values to ignore
    tag_value = ['openshift-node','JenkinsBuildServer','openshift-master']

    for region in ec2_regions:
        #sets current working region
        print("Currently process instances in %s" % region)
        region_id = boto3.resource('ec2',region_name=region)
        # Gets a list of EC2 instances which are running
        instances = region_id.instances.filter(
                    Filters=[{'Name': 'instance-state-name', 'Values': ['running','stopped']}])

        flag = True
        for instance in instances:
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    name = tag['Value']
                if name in tag_value:
                    flag = False
            try:
                logging.info("Deleting instance %s "% instance.id)
                if flag:
                #disableAPIProtection(instance.id)
                #response = instance.terminate()
                    print("Instance %s termination"  % instance.id)
                else:
                    pass
                    #print("Instance %s termination"  % name)
            except botocore.exceptions.ClientError as e:
                logging.error(e.response['Error']['Code'])


if __name__ == '__main__':
    main()

