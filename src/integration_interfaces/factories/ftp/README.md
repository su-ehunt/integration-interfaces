# The FTP Factory
This python module standardizes interface methods with our FTP infrastructure. 

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