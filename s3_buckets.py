#!/bin/python
import sys
import logging
import boto3
import botocore
from switch import switch


def create_bucket(bucket_name):
    try:
        logging.info("Creating bucket " + bucket_name)
        bucket = s3.Bucket(bucket_name)
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration={'LocationConstraint':'eu-west-1'})
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])


def delete_bucket(bucket_name):
    try:
        logging.info("Attempting to delete bucket " + bucket_name)
        bucket = s3.Bucket(bucket_name)
        print ("Deleting Bucket " + bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def query_bucket(bucket_name):
    try:
        logging.info("Printing objects in bucket "  + bucket_name)
        bucket = s3.Bucket(bucket_name)
        logging.info("The items in the bucket are:")
        print("The items in the bucket are:")
        for key in bucket.objects.all():
            print(key.key)
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def query_bucket_acl(bucket_name):
    try:
        logging.info("Attempting to change permission on bucket " + bucket_name)
        bucket = s3.Bucket(bucket_name)
        acl = bucket.Acl()
        for grant in acl.grants:
            print(grant['Grantee'],grant['Permission'])
    except botocore.exceptions.ClientError as e:
            logging.error(e.response['Error']['Code'])


def change_bucket_acl(bucket_name):
    try:
        logging.info("Attempting to change ACL on bucket" + bucket_name)
        bucket = s3.Bucket(bucket_name)
        bucket.Acl.put(GrantRead='vagrant')
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])


def upload_object(bucket_name):
    try:
        file = sys.argv[3]
        logging.info("Attempting to upload " + file + "to bucket" + bucket_name)
        response = s3.Object(bucket_name, file).put(Body=open(file, 'rb'))
        print response
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def list_buckets():
    try:
	logging.info("Listing all buckets........please wait")
        buckets = s3.buckets.all()
	for key in buckets:
    	    print key.name
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        
         


if __name__ == '__main__':
    # Takes bucket name as argument
    action = sys.argv[1]
    if action != 'list-buckets':
    	bucket_name = sys.argv[2]
    

    # Sets up logging
    logging.basicConfig(filename='aws_s3.log',
                    format = '%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

    # Sets resource s3 for use
    s3 = boto3.resource('s3')

    # Dispatch structure for action

    for case in switch(action):
        if case('create-bucket'):
            create_bucket(bucket_name)
            break
        if case('list-buckets'):
	    list_buckets()
            break
        if case('delete-bucket'):
            delete_bucket(bucket_name)
            print("Action Complete")
            break
        if case('query-bucket'):
            query_bucket(bucket_name)
            print("Action Complete")
            break
        if case('upload-to-bucket'):
            upload_object(bucket_name)
            break
        if case('query-acl'):
            query_bucket_acl(bucket_name)
            break
        if case('change-acl'):
            change_bucket_acl(bucket_name)
            break
        if case():
            print("No such action")

