
# Integration Connectors Library

This is a python library we can use to distribute our standard methods for connecting to standard interface types. 
## Getting Started
### Build and Install locally
The easiest way to install this package on your local machine is to pull the latest commit to main onto your computer, navigate to the project directory and run 

``` sh
python -m build .
```

If you do not have the python build package, install it with the following command, then run the previous command again. 

``` sh
python -m pip install build
```

This should generate a folder within your project directory called dist/. You can now install the package using either the generated .whl file or the .tar.gz depending on if you are working within a windows (.whl) or linux/macos (.tar.gz) by running

``` sh
python -m pip install dist/integration_interfaces-x.x.x.tar.gz

```
where x.x.x is replaced by whatever version you have build (specified in [pyproject.toml][pyproject.toml]). If you are modifying a version you already have installed, you may need to use the "--force-upgrade" flag, but beware it will reinstall all dependencies of the package as well and can take a minute. There is a -e flag that to my understanding does a mutable installation of the package, but I do not understand how to use this, and anyone who wants to explore that should feel free and encouraged to do so. 
### Docker and Pipeline Changes
In order to enable Docker to install the integration_interfaces package, a temporary authentication token must be passed to the Docker environment that is generated from within the pipeline, and then modify the environment variables within the docker image with that generated token.

This involves two changes to the azure-pipelines.yaml file in our projects, and a snippet to put in your dockerfile. 
1. Generate Authentication token
Insert the following as the first step of the build

``` yaml
    - task: PipAuthenticate@1
      inputs:
        artifactFeeds: 'integration-connectors'
        onlyAddExtraIndex: true
```
This populates an environment variable PIP_EXTRA_INDEX_URL on the build vm the pipeline is running on.

2. Pass Authentication token to Docker image
Now we need to pass the value of our newly populated environment variable into our docker image
``` yaml
    - task: Docker@2
      displayName: Build an image
      inputs:
        command: build
        dockerfile: '**/Dockerfile_base'
        repository: dockerbase
        tags: latest
        arguments: --build-arg INDEX_URL=$(PIP_EXTRA_INDEX_URL)

```
3. Modify the Dockerfile
Make sure that your dockerfile includes the following layers *before* attempting to install from requirements.txt

``` dockerfile
ARG INDEX_URL
ENV PIP_EXTRA_INDEX_URL=$INDEX_URL

RUN python3.11 -m pip install --upgrade pip &&\
python3.11 -m pip install keyring artifacts-keyring
```
The artifacts-keyring package is for the build vm to be able to authenticate against the Azure DevOps artifact feed that the repository is hosted on. 

With that all configured, you can include integration_interfaces like any other package in the requirements.txt of your project.

### Azure DevOps Project Setup
Finally when you are ready to run your pipeline, you will need to modify some project settings to allow the build vm to see our private python repository.

1. Navigate to Project Settings
2. Under Project Settings, navigate to the Settings tab under Pipelines
3. Set "Limit job authorization scope to current project for non-release pipelines" to false
4. Set "Limit job authorization scope to current project for release pipelines" to false

Now you should be able to configure this package in any of our build pipelines.

## Contribution Guide
In order to ensure the main branch acts as a record of all published versions of the package, the main branch is locked to any commits directly being pushed to it. Instead, you will need to submit a pull request in order to merge a new version.
# Misc.
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
- Add tests: I want to make sure that in the pipeline, before we try uploading to twine, I want our code to pass a set of tests to make sure we didn't break anything with an update. Ideally I want a tester factory which returns a test function for a given protocol to satisfy.
e.g. ftp_tester_factory(secret_name) -> Type FTP TEST
