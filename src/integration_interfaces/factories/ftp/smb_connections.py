
from smb.SMBConnection import SMBConnection
from dataclasses import dataclass


@dataclass
class SMBServer():
    """
    Class for implimenting SMB Connections
    Fidelity
    """
    conn: SMBConnection
    def establish_connection(self):
        '''Establishes SMB connection'''
        conn = SMBConnection(self.ad_username, self.ad_password, self.ad_username, self.share_server_name, use_ntlm_v2=True)
        assert conn.connect(share_server_ip, 139)
        
    def push_file(self,filename,remote_path):
        '''Push File to FTP'''

    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''

    def ls_files(self,remote_path):
        '''List Files in Directory'''

    def rm_file(self,filename):
        '''Deletes Remote File'''