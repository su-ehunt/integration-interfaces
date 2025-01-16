# Sharepoint FTP Concrete Factory

| Key | Value | Default |
| ---- | ---- | ---- |
| auth | Must be "sharepoint" | |
| sharepoint_user | Service account username for connecting to relevant SharePoint site| |
| sharepoint_pass | Password for service account | |
| sharepoint_base_url | OPTIONAL, Base URL for sharepoint site  | https://redhawks.sharepoint.com |
| sharepoint_site_url | Name of Sharepoint Site you want to access (e.g. "/sites/CDLI") | |
| sharepoint_doc_library | e.g. "Shared Documents/" | |
| sharepoint_auth | OPTIONAL, Name of AWS Secret that contains SharePoint Authentication information | Microsoft_Sharepoint_Auth |
| sharepoint_cert | Name of AWS Secret that contains plaintext RSA key for SharePoint auth | Microsoft_Certificate |
| file_retention | Name of AWS Secret that contains plaintext RSA key | |