# Factories Module
This module gives a set of factory functions which take in the name of an AWS secret, and return an object with standard interface methods. 
This allows us to generate programmable objects just from populating an AWS secret, and removes the need to specify how to interact with the same type of endpoint from project to project.

Factories are split by interface type (e.g. FTP Servers, SQL Servers, etc), and the specific concrete instantiation method of an interface object is controlled by the "auth" parameter in the endpoint's corresponding JSON secret. 

Individual concrete instantiations are differentiated by any difference in the implimentation of interacting with the endpoint (e.g. difference of authentication method, etc), however, all of these concrete classes satisfy a shared protocol (e.g. FTP Server) which allows us to interact with these differing types of endpoints the same way regardless of individual differences.

For more detailed information on how to configure secrets such that they are compatable with the factory, refer to the readme corresponding to the interface you are trying to implemment:
- [FTP Factory](ftp/README.md)
- [SQL Factory](sql/README.md)