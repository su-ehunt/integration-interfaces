from abc import ABC, abstractmethod
from dataclasses import dataclass
import paramiko

@dataclass
class SFTPServer(ABC):
    '''
    Abstract base class for SFTP servers
    
    Essentially just an interface to paramiko
    '''
    sftp: paramiko.SFTPClient
    def __init__(self,secret) -> None:
        self.establish_connection(secret)
    @abstractmethod
    def establish_connection(self,secret):
        '''Initialize self.sftp'''

    def push_file(self,filename,remote_path):
        """Push SFTP File"""
        self.sftp.put(filename,remote_path)

    def pull_file(self,filename,remote_path):
        """Pull SFTP File"""
        self.sftp.get(remote_path,filename)

    def ls_files(self,remote_path):
        """List Files"""
        return self.sftp.listdir(remote_path)

    def rm_file(self,filename):
        """Delete Remote File"""
        self.sftp.remove(filename)


class SFTPUserPassword(SFTPServer):
    '''
    TutorTrac
    Slate
    Colleague

    '''
    def establish_connection(self, secret):
        sftp_host = secret['sftp_host']
        sftp_port = secret['sftp_port']
        sftp_user = secret['sftp_user']
        sftp_pass = secret['sftp_pass']
        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(username=sftp_user,password=sftp_pass)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

class SFTPPrivateKey(SFTPServer):
    '''
    Maxient
    Follett
    CLSS
    Fusion
    EverSpring
    Get Inclusive
    '''
    def establish_connection(self, secret):
        sftp_host = secret['sftp_host']
        sftp_port = secret['sftp_port']
        sftp_user = secret['sftp_user']
        private_key = secret['private_kay']

        with open('access_key.pem', 'w',encoding="UTF-8") as p_key:
            p_key.write(private_key)

        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(hostkey=None, username=sftp_user, pkey=private_key)
        self.sftp = paramiko.SFTPClient.from_transport(transport)