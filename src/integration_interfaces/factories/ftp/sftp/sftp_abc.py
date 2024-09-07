from abc import ABC, abstractmethod
from dataclasses import dataclass
from integration_interfaces.factories.ftp.auth_wrap_ftp import auth_wrap_ftp
from integration_interfaces.aws.secrets_manager import get_secret_pkey
from integration_interfaces.logging import log
import paramiko


@dataclass
class SFTPServer(ABC):
    '''
    Abstract base class for SFTP servers
    
    Essentially just an interface to paramiko
    '''
    sftp: paramiko.SFTPClient | None
    apply_wrap = True
    def __init__(self,secret: dict) -> None:
        self.secret = secret
        self.sftp = None
        if 'private_key_secret' in secret.keys():
            self.private_key = get_secret_pkey(secret['private_key_secret'])

    @abstractmethod
    def establish_connection(self):
        '''Initialize self.sftp'''
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)
    def push_file(self,filename,remote_path):
        """Push SFTP File"""
        self.sftp.put(filename,remote_path)

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def pull_file(self,filename,remote_path):
        """Pull SFTP File"""
        self.sftp.get(remote_path,filename)

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def ls_files(self,remote_path):
        """List Files"""
        return self.sftp.listdir(remote_path)
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def rm_file(self,filename):
        """Delete Remote File"""
        self.sftp.remove(filename)

    def close_connection(self):
        self.sftp.close()

    def connected(self):
        return self.sftp is not None

@dataclass
class ROSFTPServer():
    '''
    Abstract base class for Read Only SFTP servers
    
    For FTP servers for which there is no test environment.
    This helps keep code consistent in test/prod.
    '''
    sftp: paramiko.SFTPClient | None
    apply_wrap = True
    def __init__(self,secret) -> None:
        self.secret = secret
        self.sftp = None
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def push_file(self,filename,remote_path):
        """Push SFTP File"""
        log.info('Skipping push_file operation as FTP is Read Only')

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def pull_file(self,filename,remote_path):
        """Pull SFTP File"""
        self.sftp.get(remote_path,filename)

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def ls_files(self,remote_path):
        """List Files"""
        return self.sftp.listdir(remote_path)
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def rm_file(self,filename):
        """Delete Remote File"""
        log.info('Skipping push_file operation as FTP is Read Only')

    def close_connection(self):
        self.sftp.close()
    
    def connected(self):
        return self.sftp is not None