#!/bin/python
import sys
import os
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

def get_all_versions(bucket, filename):
    s3 = boto3.client('s3')
    keys = ["Versions", "DeleteMarkers"]
    results = []
    for k in keys:
        response = s3.list_object_versions(Bucket=bucket)[k]
        to_delete = [r["VersionId"] for r in response if r["Key"] == filename]
    results.extend(to_delete)
    return results

def delete_bucket(bucket_name):
    try:
        logging.info("Attempting to delete bucket " + bucket_name)
        bucket = s3.Bucket(bucket_name)
        print ("Deleting Bucket " + bucket_name)
        for key in bucket.objects.all():
            key.delete()
            for version in get_all_versions(bucket_name, key):
               s3.delete_object(Bucket=bucket_name, Key=key, VersionId=version)
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
    size = 100
    try:
        file = sys.argv[3]
        filesz = os.stat(file).st_size >> 20
        if int(filesz) > int(size):
            print("Using multipart upload...")
            mpupload(bucket_name,file)
        else:
            logging.info("Attempting to upload " + file + "to bucket" + bucket_name)
            response = s3.Object(bucket_name, file).put(Body=open(file, 'rb'))
            print response
    except IOError:
        print("File not found")
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def mpupload(bucket_name,file):
    # Initiate the multipart upload and send the part(s)
    s3 = boto3.client('s3')
    mpu = s3.create_multipart_upload(Bucket=bucket_name,Key=file)
    part1 = s3.upload_part(Bucket=bucket_name, Key=file, PartNumber=1,
                           UploadId=mpu['UploadId'], Body='Testfile')
    # Next, we need to gather information about each part to complete
    # the upload. Needed are the part number and ETag.
    part_info = {
                'Parts': [
                            {
                              'PartNumber': 1,
                              'ETag': part1['ETag']
                            }
                         ]
                }
    # Now the upload works!
    s3.complete_multipart_upload(Bucket=bucket_name, Key=file, UploadId=mpu['UploadId'],
                                 MultipartUpload=part_info)


def list_buckets():
    try:
        logging.info("Listing all buckets........please wait")
        buckets = s3.buckets.all()
        for key in buckets:
            print key.name
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def download_object(bucket_name):
    try:
        KEY = sys.argv[3]
        logging.info("Downloading file from bucket........please wait")
        print ("Downloading File %s" % KEY)
        s3.Bucket(bucket_name).download_file(KEY, KEY)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


if __name__ == '__main__':
    # Takes bucket name as argument
    action = sys.argv[1]
    if action != 'list-buckets':
        bucket_name = sys.argv[2]


    # Sets up logging
    logging.basicConfig(filename='aws_s3.log',
                        format = '%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.ERROR)

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
        if case('download-file'):
            download_object(bucket_name)
            break
        if case('query-acl'):
            query_bucket_acl(bucket_name)
            break
        if case('change-acl'):
            change_bucket_acl(bucket_name)
            break
        if case():
            print("No such action")

