from integration_interfaces.factories.ftp.concrete.sftp.sftp_abc \
    import SFTPServer, ROSFTPServer
from integration_interfaces.logging import log
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
        log.info(f"Establishing connection to {self.secret_name}")
        sftp_host = self.secret['sftp_host']
        sftp_port = int(self.secret['sftp_port'])
        sftp_user = self.secret['sftp_user']
        rsa_key = paramiko.RSAKey.from_private_key(StringIO(self.private_key))

        transport = paramiko.Transport((sftp_host, sftp_port))
        log.info("Transport Object Established, moving onto authentication...")
        transport.connect(hostkey=None, username=sftp_user, pkey=rsa_key)
        log.info("Authenticated!")
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        if self.base_dir is not None:
            log.info(f"Moving SFTP Cursor to Base Directory {self.base_dir}")
            self.sftp.chdir(self.base_dir)

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