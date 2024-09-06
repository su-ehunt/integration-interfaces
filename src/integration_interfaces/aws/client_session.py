import boto3
session = boto3.session.Session()
client = session.client('secretsmanager', 'us-west-2')