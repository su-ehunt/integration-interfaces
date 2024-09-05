# Integration Connectors Library

This is a python library we can use to distribute our standard methods for connecting to standard interface types. 

## Guide to hosting a Azure Repository
The goal of this is to host a python distribution privately in Azure Dev-Ops that we can pull into other projects. 
This project hosts the source code for the package under the src/ directory, upon commits an Azure Build agent runs that builds the source code into a wheel for publishing, and commits the update to Azure Artifacts with twine.

### Project Permisions
There is one particularly obscure set of service accounts you need to configure so the pipeline can publish the packages.
- Under Artifacts, find the gear icon (settings), called Feed Settings if you hover over it.
- Under Feed Settings, navigate to the permissions tab
- Add two users with "Feed Publisher" roles
-- \[Project Name] Build Service (seattleu-its) e.g. Standard_Integration_Connectors Build Service (seattleu-its)
-- Project Collection Build Service (seattleu-its)

# Project To Do
- Add concrete Mock FTP classes that instantiate read only sessions for the case of not having a test environment FTP. 
- Add tests: I want to make sure that in the pipeline, before we try uploading to twine, I want our code to pass a set of tests to make sure we didn't break anything with an update. 