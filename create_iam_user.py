#!/bin/python

import sys
import os
import click
import boto3
import botocore
import json

@click.command()
@click.option('--user', metavar='<USERNAME>', required=True,
                       help='The name of the user to create.')
@click.option('--mfa', metavar=' <TOKENID>', prompt='Enter the mfa authcode for ec2-dev ',
                       help='MFA code to authenticate.')

def create_user(user, mfa):
    from boto.s3.connection import S3Connection
    from boto.sts import STSConnection
    import yaml
    sts_connection = STSConnection()

    # Use the appropriate device ID (serial number for hardware device or ARN for virtual device).
    # Replace ACCOUNT-NUMBER-WITHOUT-HYPHENS and MFA-DEVICE-ID with appropriate values.

    tempCredentials = sts_connection.get_session_token(
        duration=3600,
        mfa_serial_number="arn:aws:iam::231871078230:mfa/ec2-dev",
        mfa_token=mfa
    )

    # Use the temporary credentials to list the contents of an S3 bucket
    s3_connection = S3Connection(
        aws_access_key_id=tempCredentials.access_key,
        aws_secret_access_key=tempCredentials.secret_key,
        security_token=tempCredentials.session_token
    )

    try:
        f = open('users.yaml')
    except IOError as err:
        click.echo("Error: %s" % err)
    else:
        with f:
            config = yaml.load(f)
            if config[user]:
                policy = config[user]['policies']
                access = config[user]['programmatic']
                console = config[user]['console']
                mfa = config[user]['mfa']
                try:
                    response = iam.create_user(
                        UserName=user
                    )
                except botocore.exceptions.ClientError as e:
                    logging.error(e.response['Error']['Code'])
                    click.echo("Exception Caught: %s" % e)
                else:
                    print(json.dumps(response, indent=4, default=str))
                    attach_policy(user,policy)
                    # dispatch directionary
                    dispatch_dict = {
                       'programmatic': programmatic_access,
                       'console' :  console_access,
                       'mfa'     :  configure_mfa
                    }

                    for k, v in config[user].items():
                        if k in ('programmatic','console','mfa') and v is True:
                            handler = dispatch_dict[k]
                            handler(user)

            else:
                click.echo("User configuraton does not exist in %s" % f)
                sys.exit(1)

def console_access(user):
    click.echo("Creating console access for %s" % user)
    logging.info("Creating console access for %s" % user)

    try:
        login_profile = iam.create_login_profile(
            UserName=user,
            Password=pw_generator(),
            PasswordResetRequired=True
        )

        print(json.dumps(login_profile, indent=4, default=str))

    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        click.echo("Exception Caught: %s" % e)

def configure_mfa(user):
    pass

def attach_policy(user, policy):
    click.echo ("Attaching user policy %s to %s" % (policy, user))
    logging.info("Attaching user policy %s to %s" % (policy, user))

    try:
        response = iam.attach_user_policy(
            PolicyArn=policy,
            UserName=user
        )
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        click.echo("Exception Caught: %s" % e)


def programmatic_access(user):
    click.echo("Creating programmatic access for %s" % user)
    logging.info("Creating programmatic access for %s" % user)

    try:
        response = iam.create_access_key(
            UserName=user
        )
    except  botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])
        click.echo("Exception Caught: %s" % e)
    else:
        access_key_id = response['AccessKey']['AccessKeyId']
        secret_key = response['AccessKey']['SecretAccessKey']
        cred_file = 'credentials_' + user + '.csv'
        try:
            f = open (cred_file,'w')
        except IOError as err:
            click.echo ("Cannot write to file! Error %s" %  err)
        else:
            with f:
                f.write( 'AccessID,' + access_key_id + '\n' \
                         'SecretKey,' + secret_key)


def pw_generator():
    import random
    characters = "abcdefghijklmnopqrstuvwxyz"
    upperchars = characters.upper()
    length = 10
    pwlist = []

    for i in range(length//3):
        pwlist.append(characters[random.randrange(len(characters))])
        pwlist.append(upperchars[random.randrange(len(upperchars))])
        pwlist.append(str(random.randrange(10)))

    for i in range(length-len(pwlist)):
        pwlist.append(characters[random.randrange(len(characters))])

    random.shuffle(pwlist)
    pwstring = "".join(pwlist)
    print (pwstring)
    return pwstring


if __name__ == '__main__':

     # set up logging
     import logging
     logging.basicConfig(filename='aws_iam.log',
         format = '%(asctime)s - %(levelname)s: %(message)s',
         level=logging.DEBUG)

     # instantiate low-level client for iam
     iam = boto3.client('iam')

     # create user
     create_user()


