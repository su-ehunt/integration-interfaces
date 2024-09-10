from typing import Dict
from integration_interfaces.factories.ftp.concrete import \
    SFTPPrivateKey,SFTPUserPassword,\
    ROSFTPPrivateKey,ROSFTPUserPassword,\
    SFTPSSHAuth,ROSFTPSSHAuth,\
    SMBServer,ROSMBServer,\
    S3FTP
from integration_interfaces.factories.ftp.ftp_server_protocol import FTPServer

FTP_PROTOCOLS: Dict[str,type[FTPServer]] = {
    "sftp_password": SFTPUserPassword,
    "ro_sftp_password": ROSFTPUserPassword,
    "sftp_pkey": SFTPPrivateKey,
    "ro_sftp_pkey": ROSFTPPrivateKey,
    "sftp_ssh": SFTPSSHAuth,
    "ro_sftp_ssh": ROSFTPSSHAuth,
    "smb": SMBServer,
    "ro_smb": ROSMBServer,
    "s3": S3FTP
}
