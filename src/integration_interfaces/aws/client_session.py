import boto3
import boto3.session
session = boto3.session.Session()
client = session.client('secretsmanager', 'us-west-2')

def external_session_factory(access_key,access_key_id) -> boto3.Session:
    session = boto3.Session(aws_access_key_id=access_key_id,aws_secret_access_key=access_key)
    return session
