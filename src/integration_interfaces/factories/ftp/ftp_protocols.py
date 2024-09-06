from typing import Dict
from integration_interfaces.factories.ftp.sftp import \
    SFTPPrivateKey,SFTPUserPassword,ROSFTPPrivateKey,ROSFTPUserPassword
from integration_interfaces.factories.ftp.smb import SMBServer
from integration_interfaces.factories.ftp.ftp_server_protocol import FTPServer

FTP_PROTOCOLS: Dict[str,type[FTPServer]] = {
    "sftp_password": SFTPUserPassword,
    "ro_sftp_password": ROSFTPUserPassword,
    "sftp_pkey": SFTPPrivateKey,
    "ro_sftp_pkey": ROSFTPPrivateKey,
    "smb": SMBServer
}
