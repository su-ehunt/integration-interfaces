
from smb.SMBConnection import SMBConnection
from dataclasses import dataclass
from integration_interfaces.factories.ftp.auth_wrap_ftp import auth_wrap_ftp
from integration_interfaces.logging import log
from tenacity import retry, stop_after_attempt, wait_exponential

@dataclass
class SMBServer():
    """
    Class for implimenting SMB Connections
    Fidelity
    """

    conn: SMBConnection | None
    apply_wrap = True
    def __init__(self,secret,secret_name):
        self.ad_username = secret['ad_username']
        self.ad_password = secret['ad_password']
        self.share_server_name = secret['share_server_name']
        self.share_server_ip = secret['share_server_ip']
        self.auth = secret['auth']
        self.secret_name = secret_name
        self.conn = None

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
    def establish_connection(self):
        '''Establishes SMB connection'''
        conn = SMBConnection(self.ad_username, self.ad_password, self.ad_username, self.share_server_name, use_ntlm_v2=True)
        assert conn.connect(self.share_server_ip, 139)
   
    def close_connection(self):
        '''Close SMB Connection'''
        self.conn.close()
    
    def connected(self):
        return self.conn is not None

    @auth_wrap_ftp(apply_wrap = apply_wrap)   
    def push_file(self,filename,remote_path):
        """Push File over SMB"""
        with open(filename, 'rb') as file_obj:
            self.conn.storeFile(remote_path, remote_path + filename, file_obj)

    @auth_wrap_ftp(apply_wrap = apply_wrap)
    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''
        with open(filename, 'wb') as file_obj:
            self.conn.retrieveFile(remote_path, filename, file_obj)

    @auth_wrap_ftp(apply_wrap = apply_wrap)
    def ls_files(self,remote_path):
        '''List Files in Directory'''
        return self.conn.listPath(remote_path,'/')
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)
    def rm_file(self,filename,remote_path):
        '''Deletes Remote File'''
        self.conn.deleteFiles(remote_path, filename)

    def info(self):
        info_dict = {
            "Endpoint Secret": self.secret_name,
            "Endpoint auth type": self.auth
        }
        return info_dict


class ROSMBServer(SMBServer):
    """
    Class for implimenting SMB Connections
    Fidelity
    """

    apply_wrap = True
    def __init__(self, secret):
        super().__init__(secret)
    
    def establish_connection(self):
        return super().establish_connection()
    
    def close_connection(self):
        return super().close_connection()
    
    def connected(self):
        return super().connected()
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)   
    def push_file(self,filename,remote_path):
        """Push File over SMB"""
        log.info("Skipping File Write Operation during Read Only Session")
    
    def pull_file(self, filename, remote_path):
        return super().pull_file(filename, remote_path)
    
    def ls_files(self, remote_path):
        return super().ls_files(remote_path)
    
    @auth_wrap_ftp(apply_wrap = apply_wrap)
    def rm_file(self,filename,remote_path):
        '''Deletes Remote File'''
        log.info("Skipping File Deletion Operation during Read Only Session")

    def info(self):
        info_dict = {
            "Endpoint Secret": self.secret_name,
            "Endpoint auth type": self.auth
        }
        return info_dict