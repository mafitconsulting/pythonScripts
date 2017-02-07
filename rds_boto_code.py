#!/usr/bin/python
""" Utility script for manipulating AWS RDS """
import sys
import logging
import boto3
from switch import switch
import botocore
import configparser

def usage(option):
    """ Usage function """
    print "\nUSAGE: " + option + "\n"
    for case in switch(option):
        if case('default'):
            print """
                ./rds_boto_code.py create-db-instance
                ./rds_boto_code.py delete-db-instance <dbname>
                ./rds_boto_code.py list-db-instances
            """
        break

def create_db_instance():
    """ Creates mysql Instance """
    try:
        if len(sys.argv) < 1:
            usage('default')
        else:
            logging.info("Creating RDS Instance ")
            try:
                file = '/root/dbinstance.cfg'
                config = configparser.ConfigParser()
                config.read(file)
                response = rds.create_db_instance(
                    DBInstanceIdentifier=config['DBPARAMS']['DBInstanceIdentifier'],
                    MasterUsername=config['DBPARAMS']['MasterUsername'],
                    MasterUserPassword=config['DBPARAMS']['MasterUserPassword'],
                    DBInstanceClass=config['DBPARAMS']['DBInstanceClass'],
                    Engine=config['DBPARAMS']['Engine'],
                    AllocatedStorage=int(config['DBPARAMS']['AllocatedStorage']))
                print response
            except botocore.exceptions.ClientError as e:
                logging.error(e.response['Error']['Code'])
    except IndexError:
        usage('default')

def list_db_instances():
    """ Get all DB Instances """
    try:
        dbs = rds.describe_db_instances()
        for db in dbs['DBInstances']:
            print ("%s@%s:%s %s") % (
                db['MasterUsername'],
                db['Endpoint']['Address'],
                db['Endpoint']['Port'],
                db['DBInstanceStatus'])
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

def delete_db_instance():
    """Detete a db instance"""
    db = sys.argv[2]
    try:
        response = rds.delete_db_instance(
            DBInstanceIdentifier=db,
            SkipFinalSnapshot=True)
        print response
    except botocore.exceptions.ClientError as e:
        logging.error(e.response['Error']['Code'])

if __name__ == '__main__':
    rds = boto3.client('rds')
    """Sets up logging"""
    logging.basicConfig(filename='aws_s3.log',
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)

    try:
        ACTION = sys.argv[1]
        for case in switch(ACTION):
            if case('create-db-instance'):
                if len(sys.argv) > 1:
                    logging.info("Creating Instance")
                    create_db_instance()
                else:
                    usage('default')
                break
            if case('list-db-instances'):
                if len(sys.argv) == 2: 
                    logging.info("querying instance")
                    list_db_instances()
                else:
                    usage('default')
                break
            if case('delete-db-instance'):
                if len(sys.argv) == 3:
                    delete_db_instance()
                else:
                    usage('default')
                break
            if case():
                print "No Database instance action"
                break
    except:
        usage('default')

