#!/usr/bin/python
from __future__ import print_function 
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Movies')
table.delete()
