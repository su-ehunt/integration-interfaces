from abc import ABC, abstractmethod
from dataclasses import dataclass
import paramiko
from integration_interfaces.factories.ftp.auth_wrap_ftp import auth_wrap_ftp
from integration_interfaces.logging import log
from integration_interfaces.aws_secrets_manager import get_secret_pkey
from tenacity import retry, stop_after_attempt, wait_exponential

@dataclass
class SFTPServer(ABC):
    '''
    Abstract base class for SFTP servers
    
    Essentially just an interface to paramiko
    '''
    sftp: paramiko.SFTPClient | None
    def __init__(self,secret) -> None:
        self.secret = secret
        self.sftp = None

    @abstractmethod
    def establish_connection(self,secret):
        '''Initialize self.sftp'''
    
    @auth_wrap_ftp
    def push_file(self,filename,remote_path):
        """Push SFTP File"""
        self.sftp.put(filename,remote_path)

    @auth_wrap_ftp
    def pull_file(self,filename,remote_path):
        """Pull SFTP File"""
        self.sftp.get(remote_path,filename)

    @auth_wrap_ftp
    def ls_files(self,remote_path):
        """List Files"""
        return self.sftp.listdir(remote_path)
    
    @auth_wrap_ftp
    def rm_file(self,filename):
        """Delete Remote File"""
        self.sftp.remove(filename)

    def close_connection(self):
        self.sftp.close()



class SFTPUserPassword(SFTPServer):
    '''
    TutorTrac
    Slate
    Colleague

    '''
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
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
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
    def establish_connection(self, secret):
        sftp_host = secret['sftp_host']
        sftp_port = secret['sftp_port']
        sftp_user = secret['sftp_user']
        private_key_secret = secret['private_key_secret'] #Location of pkey secret. Standards dictate it will be Vendor/ftp_secret/pkey
        private_key = get_secret_pkey(private_key_secret) #Alma_RSA as reference secret

        with open('access_key.pem', 'w',encoding="UTF-8") as p_key:
            p_key.write(private_key)
            log.info('Writing Private Key File to access_key.pem')

        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(hostkey=None, username=sftp_user, pkey='access_key.pem')
        self.sftp = paramiko.SFTPClient.from_transport(transport)


