from typing import Protocol
from src.integration_interfaces.factories.ftp.sftp_connections import SFTPPrivateKey,SFTPUserPassword
from src.integration_interfaces.factories.ftp.smb_connections import SMBServer
from src.integration_interfaces.aws_secrets_manager import get_secret_json
from src.integration_interfaces.logging import log


FTP_PROTOCOLS = {
    "sftp_password": SFTPUserPassword,
    "sftp_pkey": SFTPPrivateKey,
    "smb": SMBServer
}


class FTPServer(Protocol):
    """Base Protocol class for our FTP endpoints"""
    
    def establish_connection(self,secret):
        '''Initialize connection'''

    def close_connection(self):
        '''Closes FTP connection'''

    def push_file(self,filename,remote_path):
        '''Push File to FTP'''

    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''

    def ls_files(self,remote_path):
        '''List Files in Directory'''

    def rm_file(self,filename):
        '''Deletes Remote File'''

def ftp_factory(secret_name) -> type[FTPServer]:
    """Function to take in a secret and return the endpoint object we want"""
    secret = get_secret_json(secret_name)
    auth = secret["auth"].lower()
    try:
        return FTP_PROTOCOLS[auth](secret)
    except Exception as e:
        log.exception(e)
        raise e

