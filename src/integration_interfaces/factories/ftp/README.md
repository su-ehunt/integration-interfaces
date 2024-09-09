# The FTP Factory
This python module standardizes interface methods with our FTP infrastructure. 

## Secrets Configuration
For detailed information on configuring secrets for a given integration endpoint, refer to the README's in the concrete factory directories
- [SFTP Concrete Factories README.md](sftp/README.md)
- [SMB Concrete Factories Readme.md](smb/README.md)

## Modules

### [ftpfactory.py](ftpfactory.py)
This file is the main FTP factory. There are three main components to the file
- FTP_PROTOCOLS Dict:
This dictionary acts as a map between auth methods and their concrete classes. If there is a new concrete class for FTP transfer that needs to be added, that class, along with it's "auth" indicator need to be added to this dictionary for the factory to function.
- FTPServer Protocol Class:
This class provides the framework that all concrete instatiations of FTP servers must satisfy. This standardizes the way in which we interact with FTP endpoints, giving us the same method names regardless of if we connect to an SMB server or an SFTP server. 
- ftp_factory:
This is the function, which takes in the name of an AWS secret, parses out the auth method, and returns a concrete instantiation of your desired FTP server. Due to the strong typing of this function, when you use it to generate an FTP server, you should get syntax highlighting for methods of your generated object. 

### [sftp_connections.py](sftp_connections.py)
This file creates an abstract base class for SFTP servers that acts as a base wrapper around Paramiko, along with a base class for read-only SFTP ROSFTP. 
These classes are configured for cases when we do not have separated test/prod environments in our FTP, but still allow us to assert our connections, and complete read only operations to production assets. 

There are also a collection of concrete instantiations of these classes for each combination of read only boolean and authentication method. 

### [smb_connections.py](smb_connections.py)
This file contains our logic for instantiating SMB connections. 

### [auth_wrap_ftp.py](auth_wrap_ftp.py)
This file contains a wrapper method for authenticating and closing FTP connections. Thanks to the FTP protocol, we know that regardless of the concrete details of an FTP (SFTP/SMB/auth method), each FTP class will have an establish and close connection method. 
This allows us to wrap all function calls in the FTP class with an initial connection, and make sure to close out of FTP connections after operations are complete to avoid any dangling authenticated FTP sessions. 