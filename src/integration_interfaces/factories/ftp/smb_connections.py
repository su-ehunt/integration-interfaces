
from smb.SMBConnection import SMBConnection
from dataclasses import dataclass
from integration_interfaces.factories.ftp.auth_wrap_ftp import auth_wrap_ftp
from tenacity import retry, stop_after_attempt, wait_exponential

@dataclass
class SMBServer():
    """
    Class for implimenting SMB Connections
    Fidelity
    """

    conn: SMBConnection | None
    def __init__(self,secret):
        self.ad_username = secret['ad_username']
        self.ad_password = secret['ad_password']
        self.share_server_name = secret['share_server_name']
        self.share_server_ip = secret['share_server_ip']

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
    def establish_connection(self):
        '''Establishes SMB connection'''
        conn = SMBConnection(self.ad_username, self.ad_password, self.ad_username, self.share_server_name, use_ntlm_v2=True)
        assert conn.connect(self.share_server_ip, 139)
   
    @auth_wrap_ftp   
    def push_file(self,filename,remote_path):
        '''Push File to FTP'''

    @auth_wrap_ftp
    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''

    @auth_wrap_ftp
    def ls_files(self,remote_path):
        '''List Files in Directory'''

    @auth_wrap_ftp
    def rm_file(self,filename):
        '''Deletes Remote File'''

    def close_connection(self):
        '''Close SMB Connection'''
        self.conn.close()