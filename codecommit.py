#!/bin/python
import sys
import logging
import json
import argparse
import boto3
import botocore
import random


# CLI options
parser = argparse.ArgumentParser()
parser.add_argument("--getrepository", help="Requires the repository name")
parser.add_argument("--listrepositories", help="List all repositories in codecommit", action='store_true')
parser.add_argument("--createrepository", help="Creates a codecommit repository, requires --decription field")
parser.add_argument("--deleterepository", help="Creates a codecommit repository, requires repository name")
parser.add_argument("--description", help="Decription for code repository")
parser.add_argument("--createbranch", help="Create new branch, requires description and repos name")
parser.add_argument("--getbranch", help="queries branch from repo, requires repos name")
parser.add_argument("--repositoryname", help="repositoryname to create branch in")
args = parser.parse_args()


# Sets up logging
logging.basicConfig(filename='aws_codecommit.log',
                   format='%(asctime)s - %(levelname)s: %(message)s',
                   level=logging.ERROR)

# Sets resource s3 for use
client = boto3.client('codecommit')


def list_repositories():
    try:
        logging.info("Listing code commit repositories")
        print("Listing code commit repositories")
        response = client.list_repositories(
            sortBy='repositoryName',
            order='ascending'
        )
        print(json.dumps(response, indent=4, default=str))

    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def get_repository(repository_name):
    try:
        logging.info("Getting repository info for %s" % repository_name)
        print("Getting repository info for %s" % repository_name)
        response = client.get_repository(
                   repositoryName=repository_name
        )
        print(json.dumps(response, indent=4, default=str))
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])


def delete_repository(repository_name):
    rc = raw_input("Deleting repository %s, are you sure you wish to proceed (y/n)" % repository_name).lower()
    if rc == 'y':
        try:
            #object = client.get_repository(
            #         repositoryName=repository_name
            #)
            #repository_id = object['repositoryMetadata']['repositoryId']
            response = client.delete_repository(
                       repositoryName=repository_name
            )
            print(json.dumps(response, indent=4, default=str))
            print "Repository Deleted"
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
        print(json.dumps(response, indent=4, default=str))
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        print(e.response['Error']['Code'])


def create_branch(repository_name, branch_name):
    logging.info("Creating repository branch %s" % branch_name)
    try:
        commit = ''.join(random.choice('ABCDEFabcdef012345') for i in range(10))
        response = client.create_branch(
                   repositoryName=repository_name,
                   branchName=branch_name,
                   commitId=str(commit)
        )
        branch = client.get_branch(
                 repositoryName=repository_name,
                 branchName=branch_name
        )

        print(json.dumps(branch, indent=4, default=str))
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def get_branch(repository_name):
    logging.info("Getting branch information from repos %s" % (repository_name))
    try:
         response = client.list_branches(
                    repositoryName=repository_name,
         )
         print(json.dumps(response, indent=4, default=str))
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        print (e.response['Error']['Code'])



# Dispatch structure for action

if args.getrepository:
    get_repository(args.getrepository)
elif args.listrepositories:
    list_repositories()
elif args.createrepository:
    create_repository(args.createrepository,args.description)
elif args.deleterepository:
    delete_repository(args.deleterepository)
elif args.createbranch:
    create_branch(args.createbranch,args.repositoryname)
elif args.getbranch:
    get_branch(args.getbranch)
