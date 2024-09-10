# SFTP Concrete Factories
This directory contains the concrete implimenations of SFTP classes. They all inherit a light paramiko wrapper as defined in the SFTP Abstract Base Class (ABC), and each overwrites the base class's authentication method in such a way that each SFTP server is the same to deal with no matter what. 

# How to Format SFTP Secrets

The main functionality of the factory is around standardizing how we go from secrets to interactable code objects. In order for this to work, the secrets stored in AWS must follow certain standards

## SFTP Private Key Authentication

For Private Key SFTP authentication, make sure you have the following key/value pairs in Secrets Manager: 
| Key | Value|
| ---- | ---- |
| auth | Value MUST be "sftp_pkey" OR "ro_sftp_pkey" |
| sftp_host | Hostname for SFTP Server|
| sftp_port | Port which accepts SFTP connections |
| sftp_user | Username for SFTP authentication |
| private_key_secret | Name of AWS Secret that contains plaintext RSA key |

This secret is required along with the secret named in "private_key_secret" for authenticating private key connections. The secret stored in "private_key_secret" MUST be a plaintext secret containing the RSA private key for connection (see Alma/sftp/rsa_key)

## SFTP Username/Password Authentication

For SFTP servers that authenticate with username and password, make sure you have the following key/value pairs in Secrets Manager: 
| Key | Value|
| ---- | ---- |
| auth | Value MUST be "sftp_password" OR "ro_sftp_password" |
| sftp_host | Hostname for SFTP Server|
| sftp_port | Port which accepts SFTP connections |
| sftp_user | Username for SFTP authentication |
| sftp_pass | Password for SFTP authentication |

## SFTP Authentication over SSH

For SFTP servers that authenticate with username and password over SSH, make sure you have the following key/value pairs in Secrets Manager: 
| Key | Value|
| ---- | ---- |
| auth | Value MUST be "sftp_ssh" OR "ro_sftp_ssh" |
| sftp_host | Hostname for SFTP Server|
| sftp_port | Port which accepts SFTP connections |
| sftp_user | Username for SFTP authentication |
| sftp_pass | Password for SFTP authentication |