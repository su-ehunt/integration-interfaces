from smb.SMBConnection import SMBConnection
import paramiko


class SFTPServer():

    def push_to_sftp(self,filename, remotepath):

        log.info('Pushing ' + filename + " to sftp directory " + remotepath)
        try:
            transport = paramiko.Transport((self.sftp_host + ':' + self.sftp_port))
            transport.connect(hostkey=None, username=self.sftp_user, password=self.sftp_password)
            log.debug("Successfully connected to sftp directory")
            sftp = paramiko.SFTPClient.from_transport(transport)
            touch_remote_directory(sftp,remotepath)
            sftp.put(filename, remotepath + filename)
            sftp.close()
            transport.close()
            log.info('Successfully pushed ' + filename + " to sftp directory " + remotepath)
        except Exception as e:
            log.error(e)
            raise e
        finally:
            transport.close()

    def pull_sftp_files(remotepath,user,password, host,server):

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the remote server
            ssh.connect(hostname=host, username=user, password=password)
            
            # Create an SFTP client using the SSH connection
            sftp = ssh.open_sftp()

            # Change to the remote directory
            sftp.chdir(remotepath)

            # Get a list of files in the remote directory
            files = sftp.listdir()

            # Pull each file from the remote directory to the local directory
            for file in files:
                remote_file = os.path.join(remotepath, file)
                sftp.get(remote_file,server + file)
            return files

        except Exception as e:
            log.debug(e)
            raise e

class SMBServer():

    def push_to_smb(self,fns,remotepath):
        log.info('Writing ' + fns + ' to ' + self.share_server_ip + '/' + self.share_name + '/' + remotepath + '...')
        conn = SMBConnection(self.ad_username, self.ad_password, self.ad_username, self.share_server_name, use_ntlm_v2=True)
        assert conn.connect(self.share_server_ip, 139)
        with open(fns, 'rb') as file:
            conn.storeFile(self.share_name, remotepath + fns, file)
        file.close()
        conn.close()