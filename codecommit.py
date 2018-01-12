#!/bin/python
import sys
import logging
import boto3
import botocore
import json
import argparse
import subprocess
from switch import switch

def list_repositories():
    try:
        logging.info("Listing code commit repositories")
        print("Listing code commit repositories")
        response = client.list_repositories(
                   sortBy='repositoryName',
                   order='ascending'
                   )
        print(json.dumps(response, indent = 4))

    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def get_repository(repository_name):
    try:
        logging.info("Getting repository info for %s" % repository_name)
        print("Getting repository info for %s" % repository_name)
        response = client.get_repository(
                   repositoryName=repository_name
        )
        print(json.dumps(response, indent = 4, default=str))
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

    return response

def delete_repository(repository_name):
    print("Deleting repository %s, are you sure you wish to proceed (y/n)" % repository_name)
    rc = raw_input().lower()
    if rc == 'y':
        try:
            object = get_repository(repository_name)
            repository_id = object['repositoryMetadata']['repositoryId']
            response = client.delete_repository(
                       repositoryName=repository_id
            )
            print object['repositoryMetadata']['repositoryId']
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Code'])
    else:
        sys.exit(1)

def create_repository(repository_name,repository_description):
    logging.info("Creating repository %s" % repository_name)
    try:
        response = client.create_repository(
        repositoryName=repository_name,
        repositoryDescription=repository_description
        )
        print(json.dumps(response, indent = 4, default=str))
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])


parser = argparse.ArgumentParser()
parser.add_argument("--getrepository", help="Requires the repository name")
parser.add_argument("--listrepositories", help="List all repositories in codecommit", action='store_true')
parser.add_argument("--createrepository", help="Creates a codecommit repository, requires --decription field")
parser.add_argument("--deleterepository", help="Creates a codecommit repository, requires repository name")
parser.add_argument("--description", help="Decription for code repository")
args = parser.parse_args()


# Sets up logging
logging.basicConfig(filename='aws_codecommit.log',
                    format = '%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# Sets resource s3 for use
client = boto3.client('codecommit')

# Dispatch structure for action

if args.getrepository:
    get_repository(args.getrepository)
elif args.listrepositories:
    list_repositories()
elif args.createrepository:
    create_repository(args.createrepository,args.description)
elif args.deleterepository:
    delete_repository(args.deleterepository)




