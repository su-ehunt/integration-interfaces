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

# How to Utilize factories

## Steps to install locally

You will need to install the intended version factory you wish to use. You may view the currently used version within Azure DevOps Repo's pyproject.toml file. This will, most likely, be the version you want to use.

1. open git bash or cmd prompt
2. Navigate to (or clone) the Standard_Integration_Connectors project to pull down the latest version
3. Once you are in the project, you will need to build the project locally by typing:
> python -m build

4. Next, you will need to install the package. Change into /dist/ directory and type:
> python -m pip install integration_interfaces-0.0.32-py3-none-any.whl

**NOTE:** The version number may be different. Use the version number found in the pyproject.toml file

## Steps to utilize it locally

1. Add to your project's requirements document
> Example: integration_interfaces==0.0.32  or whichever version you have built and installed

2. Update the azure-pipelines.yml file. This code will be added directly below 'stages\stage\job\steps:'

> #Authenticate with Private Python Repo (Populates $(PIP_EXTRA_INDEX_URL)) \
    - task: PipAuthenticate@1 \
       inputs: \
        artifactFeeds: 'integration-connectors' \
        onlyAddExtraIndex: true \
    - task: Docker@2 \
      displayName: Build an image \
      inputs: \
        command: build \
        dockerfile: '**/Dockerfile_base' \
        repository: dockerbase \
        tags: latest
        arguments: --build-arg INDEX_URL=$(PIP_EXTRA_INDEX_URL) \

3. Create a new Dockerfile called, Dockerfile_base. This file includes:
>FROM public.ecr.aws/su-batch/su-batch:latest \
ARG INDEX_URL \
ENV PIP_EXTRA_INDEX_URL=$INDEX_URL \
ADD requirements.txt /tmp \
WORKDIR /usr/local/bin/ \
RUN python3.11 -m pip install --upgrade pip &&\ \
python3.11 -m pip install keyring artifacts-keyring \
RUN python3.11 -m pip install -r /tmp/requirements.txt \
USER root

**NOTE:** Update paths as needed for your project.

4. Update Dockerfile for the project including:
>FROM --platform=linux/amd64 dockerbase \
ADD Python/your_python_process_name.py /usr/local/bin/your_python_process_name.py \
ENTRYPOINT ["/usr/bin/python3.11", "/usr/local/bin/your_python_process_name.py"]

**NOTE:** Update paths as needed for your project.

## Steps to update the ftp factory code locally
As you work with the ftp factories, you may find a piece of code that needs to be updated. It is not as simple as just making the update to the code within the ftp factory and then running your code against it. You will need to follow this next section as it walks you through how to make changes to the ftp factory code.

1. Identify the change needed and make the code change.
2. Update the version number in the pyproject.toml file
3. Build and install new version locally by following the section, Steps to Install Locally. Remember to update the version number in your requirements.txt to the new version
4. Test using code that interacts with specific change

## Steps to Publish Change

Now that you fully tested the update to the ftp factory, you are now ready to publish this change in Azure DevOps.

1. In Azure DevOps, create a new branch based on main
2. Pull branch down locally
3. Merge changes from main into the new branch
4. Commit and merge the changes from within the new branch up to Azure Devops
5. In Repos, create a Pull Request. You will see a button towards the top of the Repos screen to Create a Pull Request.
   1. Once you are within the pull request, you will see a menu to merge your branch into the main branch. Enter the Title and the Description of the change. The Title can be the version number like, "Version_0_0_32". The description should contain the details of the change. This Pull Request will be sent to Lizz Hunt where she will review the change before publishing. 
   2. Lizz Hunt will review the approval request for the merge. If it passes approval, the change will merge into main and a build and publish pipeline is triggered. Once that builds successfully, the new version is available within Azure DevOps
6. Send out a communication to the team of the updated version number for the Standard_Integration_Connectors project.
7. Pull down the latest Standard_Integration_Connectors locally
