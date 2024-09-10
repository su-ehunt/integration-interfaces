# SMB Concrete factories
This directory contains the concrete implementations of SMB connections. The concrete class provides a light wrapper around pysmb in a way to hopefully make if more understandbale in our logs when something goes amis, and to improve integration reliability by standardizing retry logic when establishing a connection with remote SMB servers. 

# How to Format SMB Secrets
The format of these secrets are the only ones where I am uncertain of the standard layed out, and thus am open to discussion in regards to keeping the hostname/server IP in the same secret as the authentication credentials, as the majority of our SMB connections go to the DropShare, just with different service accounts. 
This shouldn't be an issue in so far as this IP/hostname is already duplicated across multiple secrets, and thus this initial refactoring simply does not address that issue. 

With that being said, here is the standard format for what can be our first pass in the standardization of our secrets 

| Key | Value|
| ---- | ---- |
| auth | Value MUST be "smb" OR "ro_smb" |
| share_server_ip | SMB Server IP Address |
| share_server_name | Name of SMB Share |
| ad_username | Username for SMB authentication |
| ad_password | Password for SMB authentication |