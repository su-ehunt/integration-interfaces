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
    apply_wrap = True #Data Class plus inheritance from Abstract Base class ensures
    # there is no way to update parent data value directly, thus child classes created
    # at the factory will never overwrite each-other's specific dataclass values for
    # either of these. 
    def __init__(self,secret: dict,secret_name) -> None:
        self.secret = secret
        self.sftp = None
        self.auth = secret['auth']
        self.secret_name = secret_name
        if 'private_key_secret' in secret.keys():
            self.private_key = get_secret_pkey(secret['private_key_secret'])

    @abstractmethod
    def establish_connection(self):
        '''Initialize self.sftp'''
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)
    def push_file(self,filename,remote_path):
        """Push SFTP File"""
        log.info(f"Pushing {filename} to {remote_path}")
        self.sftp.put(filename,remote_path)

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def pull_file(self,filename,remote_path):
        """Pull SFTP File"""
        log.info(f'Pulling {filename} from {remote_path}')
        return self.sftp.get(remote_path,filename)

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def ls_files(self,remote_path):
        """List Files"""
        log.info(f'Running ls operation on {remote_path}')
        return self.sftp.listdir(remote_path)
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def rm_file(self,filename):
        """Delete Remote File"""
        log.info(f"Deleting file {filename}")
        return self.sftp.remove(filename)

    def close_connection(self):
        log.info(f"Closing Connection to {self.secret_name}")
        return self.sftp.close()

    def connected(self):
        log.info(f"Checking if we are connected to {self.secret_name}")
        return self.sftp is not None
    
    def info(self):
        info_dict = {
            "Endpoint Secret": self.secret_name,
            "Endpoint auth type": self.auth
        }
        return info_dict

@dataclass
class ROSFTPServer():
    '''
    Abstract base class for Read Only SFTP servers
    
    For FTP servers for which there is no test environment.
    This helps keep code consistent in test/prod.
    '''
    sftp: paramiko.SFTPClient | None
    apply_wrap = True
    def __init__(self,secret,secret_name) -> None:
        self.secret = secret
        self.sftp = None
        self.auth = secret['auth']
        self.secret_name = secret_name
        if 'private_key_secret' in secret.keys():
            self.private_key = get_secret_pkey(secret['private_key_secret'])
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def push_file(self,filename,remote_path):
        """Push SFTP File"""
        log.info('Skipping push_file operation as FTP is Read Only')

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def pull_file(self,filename,remote_path):
        """Pull SFTP File"""
        log.info(f'Pulling {filename} from {remote_path}')
        self.sftp.get(remote_path,filename)

    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def ls_files(self,remote_path):
        """List Files"""
        log.info(f'Running ls operation on {remote_path}')
        return self.sftp.listdir(remote_path)
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)  
    def rm_file(self,filename):
        """Delete Remote File"""
        log.info('Skipping push_file operation as FTP is Read Only')

    def close_connection(self):
        log.info(f"Closing Connection to {self.secret_name}")
        self.sftp.close()
    
    def connected(self):
        log.info(f"Checking if we are connected to {self.secret_name}")
        return self.sftp is not None
    
    def info(self):
        info_dict = {
            "Endpoint Secret": self.secret_name,
            "Endpoint auth type": self.auth
        }
        return info_dict