# Factories Module
This module gives a set of factory functions which take in the name of an AWS secret, and return an object with standard interface methods. 
This allows us to generate programmable objects just from populating an AWS secret, and removes the need to specify how to interact with the same type of endpoint from project to project.

Factories are split by interface type (e.g. FTP Servers, SQL Servers, etc), and the specific concrete instantiation method of an interface object is controlled by the "auth" parameter in the endpoint's corresponding JSON secret. 

Individual concrete instantiations are differentiated by any difference in the implimentation of interacting with the endpoint (e.g. difference of authentication method, etc), however, all of these concrete classes satisfy a shared protocol (e.g. FTP Server) which allows us to interact with these differing types of endpoints the same way regardless of individual differences.

For more detailed information on how to configure secrets such that they are compatable with the factory, refer to the readme corresponding to the interface you are trying to implemment:
- [FTP Factory](ftp/README.md)
- [SQL Factory](sql/README.md)

## Factory Structure
Each factory module has the following types of submodule:
- Concrete Factory Registry (see [ftp_protocols.py](ftp/ftp_protocols.py) or [sql_protocols.py](sql/sql_protocols.py)).
These files sit at the root of each factory and serve as the record of concrete classes that impliment the protocol the factory produces, along with a corresponding "auth" value for each.
This "auth" value allows us to tell the factory which concrete class we need to handle the given information from secrets manager.
- Factory Protocol file (see [ftp_server_protocols.py](ftp/ftp_server_protocol.py) or [sql_server_protocol.py](sql/sql_server_protocol.py)).
This file also sits at the root directory of each factory, and serves as the standard interface that all objects produced by the factory must impliment.
The functionality of the protocol class comes into play when we invoke the specific factory. 
A class in python is considered to "satisfy a protocol" (i.e. returns true when doing a type comparison between a reference class and the protocol class) if the reference class contains each method defined in the protocol, and those methods contain the same or compatable return types.
- Factory Module (see [ftp_factory.py](ftp/ftp_factory.py) or [sql_factory.py](sql/sql_factory.py)).
Each factory has a specified return type of the protocol class defined by this module. 
When the type checking occurs, the python kernel checks that the object returned by the factory function satisfies the specified protocol return type.
The factory works by returning a concrete class with a standard interface when you supply it with the name of an AWS secret of the correct format.

# Contribution Guide
To best understand how to extend this libray, it is best to make sure to understand the structuring of each factory module. 