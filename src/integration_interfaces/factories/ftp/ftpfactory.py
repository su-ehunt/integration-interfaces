from typing import Protocol
from sftp_connections import SFTPPrivateKey,SFTPUserPassword
from smb_connections import SMBServer

class FTPServer(Protocol):
    """Base Protocol class for our FTP endpoints"""

    def push_file(self,filename,remote_path):
        '''Push File to FTP'''

    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''

    def ls_files(self,remote_path):
        '''List Files in Directory'''

    def rm_file(self,filename):
        '''Deletes Remote File'''

def read_secret_to_endpoint(secret) -> type[FTPServer]:
    """Function to take in a secret and return the endpoint object we want"""
    #aws get secret
    secret = secret.split('/')
    endpoint_type = secret[1].split('_')[0]
    match endpoint_type:
        case "sftp":
            return sftp_factory_reader(secret)
        case "smb":
            return SMBServer(secret)
        case _:
            print("Provided Secret name is not mapped to an initialization strategy")

def sftp_factory_reader(secret):
    auth = secret["auth"].lower()
    match auth:
        case "password":
            return SFTPUserPassword(secret)
        case "pkeyfile":
            return SFTPPrivateKey(secret)
        
        