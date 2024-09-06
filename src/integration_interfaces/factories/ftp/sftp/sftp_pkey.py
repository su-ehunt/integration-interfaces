from integration_interfaces.factories.ftp.sftp.sftp_abc \
    import SFTPServer, ROSFTPServer
from tenacity import retry, stop_after_attempt, wait_exponential
import paramiko
from io import StringIO


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
    def establish_connection(self):
        sftp_host = self.secret['sftp_host']
        sftp_port = int(self.secret['sftp_port'])
        sftp_user = self.secret['sftp_user']
        rsa_key = paramiko.RSAKey.from_private_key(StringIO(self.private_key))

        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(hostkey=None, username=sftp_user, pkey=rsa_key)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

class ROSFTPPrivateKey(ROSFTPServer,SFTPPrivateKey):

    def establish_connection(self):
        return SFTPPrivateKey.establish_connection(self)
    
    def push_file(self, filename, remote_path):
        return ROSFTPServer.push_file(self,filename, remote_path)
    
    def pull_file(self, filename, remote_path):
        return ROSFTPServer.pull_file(self,filename, remote_path)
    
    def ls_files(self, remote_path):
        return ROSFTPServer.ls_files(self,remote_path)
    
    def rm_file(self, filename):
        return ROSFTPServer.rm_file(self,filename)