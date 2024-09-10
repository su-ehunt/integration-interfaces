from integration_interfaces.factories.ftp.ftp_factory \
    import FTPServer, ftp_factory
from integration_interfaces.factories.ftp.auth_wrap_ftp \
    import auth_wrap_ftp
from integration_interfaces.factories.ftp.concrete \
    import SFTPPrivateKey, ROSFTPPrivateKey,\
        SFTPUserPassword, ROSFTPUserPassword,\
        SFTPSSHAuth, ROSFTPSSHAuth,\
        SMBServer, ROSMBServer,\
        S3FTP