import os
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from datetime import date, timedelta
import datetime
from src.integration_interfaces.aws.secrets_manager import get_secret_json, get_secret
from src.integration_interfaces.logging import log #EH REVIEW: Remove src prefix. 

sharepoint_site_secret_name = 'Canvas_SIS/Sharepoint'
cert_path = '/tmp/temp_pem.pem'
time_format = '%Y-%m-%dT%H:%M:%SZ'

sharepoint_site_secrets = {
    "sharepoint_sa_user": "",
    "sharepoint_sa_password" : "",
    "sharepoint_base_url": "",
    "sharepoint_site_url": "",
    "sharepoint_auth": "Microsoft_Sharepoint_Auth",
    "sharepoint_cert": "Microsoft_Certificate"
}

ms_secrets = {
    "client_id": "",
    "thumbprint" : "",
    "scopes": "",
}

class SharePoint:
    #This factory method is incompatable with the FTP factory. It is expecting an input of the dict object returned by secrets manager
    #(see ftp_factory line 10) followed by the string name of the secret (useful for logging purposes).
    def __init__(self, sharepointFolder, sharepointSite, timeInDays):

        self.tenant = 'redhawks.onmicrosoft.com' #This should not be hard coded
        self.timeIndays = timeInDays #This should either be a value in the secret for the sharepoint site, or an agreed upon constant. It should not be passed to the __init__ method directly.
        self.sharepoint_site_secrets = get_secret_json(sharepoint_site_secret_name)#Group with other secret retrieval and put at top
        self.sharepoint_doc_library = sharepointFolder
        self.sharepoint_full_url = self.sharepoint_site_secrets['sharepoint_base_url'] + '/sites/' + sharepointSite #Sharepoint site should be value within secret dict that gets passed to init method, not passed to init method
        self.sharepoint_relative_url = self.sharepoint_site_secrets['sharepoint_site_url'] + '/' + self.sharepoint_doc_library
        #Where is self.ctx? The connected method can't tell if a variable that hasn't been declared is none, we'll get a runtime error.
        #Make sure to add self.ctx=None to the __init__ method.
        self.ms_secrets = get_secret_json(self.sharepoint_site_secrets['sharepoint_auth'])#Gropu with other secret retrieval

        clss_sp_pem = get_secret(self.sharepoint_site_secrets['sharepoint_cert'])
        with open(cert_path, "w", newline='') as temp_pem: #Put this at the end of __init__ method as this has effects outside of class (i.e. on the runtime environment). Don't put it in the middle of a bunch of code that just manipulates the class.
            temp_pem.write(clss_sp_pem)

        self.cert_settings = {
            'client_id': self.ms_secrets['client_id'],
            'thumbprint': self.ms_secrets['thumbprint'],
            'cert_path': self.cert_path,
            'scopes': [self.ms_secrets['scopes']]
        } #The order of how you import objects is confusing. Group together assignments of class variables (i.e. self.variable = ...), t
        #then put anything that has effects outside the class (i.e. file system I/O) after that. 


    def establish_connection(self):
        log.info('Begin SharePoint authentication')
        #ctx_auth = AuthenticationContext(sharepoint_full_url)
        #ctx_auth.acquire_token_for_user(self.sp_user, self.sp_pw)
        #ctx = ClientContext(sharepoint_full_url, ctx_auth)

        self.ctx = ClientContext(self.sharepoint_full_url).with_client_certificate(self.tenant, **self.cert_settings)
        log.info('Successfully connected to ' + self.sharepoint_full_url)

    def close_connection(self):
        '''Closes FTP connection'''
        log.info("No need to close me! I'm an ClientContext session! It's useful\
                          to keep me open durring the runtime!")

    def connected(self):
        '''Returns whether or not the FTP connection is established'''
        return self.ctx is not None


    def pull_file(self,file_name,remote_path):
        log.info('Connecting to SFS SharePoint site to download ' + file_name + ' from SharePoint')

        log.info('Downloading ' + file_name + ' from SharePoint')
        sharepoint_file_url = self.sharepoint_relative_url + file_name
        response = File.open_binary(self.ctx, sharepoint_file_url)

        if response.status_code == requests.codes.ok:
            with open(file_name, 'wb') as local_file:
                local_file.write(response.content)
            log.info('Successfully downloaded ' + file_name + ' from SharePoint')
        else:
            log.info(file_name + ' does not exist in SharePoint. Exiting Process.')
            exit() #NEVER USE THIS FUNCTION CALL OUTSIDE VERY SPECIFIC CIRCUMSTANCES. This hard exits the python interpreter. 
            #Raise an error if that is the intended behavior so the exception can abe handled outside the function scope, and this function doesn't fully exit the python runtime pre-emptively.

    def push_file(self, filename, file_content):
        '''Push File to FTP'''
        #Need to add if not self.connected(); self.establish_connection()
        log.info('Connecting to SFS SharePoint site to push ' + filename + ' for archival')

        log.info('Uploading ' + filename + ' to SharePoint')
        sharepoint_remote_path = self.sharepoint_doc_library + filename
        sp_dir, name = os.path.split(sharepoint_remote_path)

        file = self.ctx.web.get_folder_by_server_relative_url(sp_dir).upload_file(name, file_content).execute_query()
        log.info('Successfully uploaded ' + filename + ' to SharePoint')


    def ls_files(self): #This function is not a generic ls function. This is a function that gets things that meet our audit criteria. 
        #We don't want to filter out EVERY sharepoint file that doesn't meet the audit criteria, the audit criteria is more about cleaning
        #directories that we historically just dump files into whenever we run an integration job. This logic should not be part of a generic ls function
        log.info('Connecting to SharePoint site to delete')

        try:
            target_folder_url = self.sharepoint_doc_library
            libraryFolderroot = self.ctx.web.get_folder_by_server_relative_url(target_folder_url)
            self.ctx.load(libraryFolderroot)
            self.ctx.execute_query()

            cutoff_date = (date.today() - timedelta(days=self.timeIndays))
            log.info("Cutoff date :  " + str(cutoff_date))
            cutoff_year = cutoff_date.year
            cutoff_month = cutoff_date.month
            cutoff_day = cutoff_date.day

            include_fields = ["TimeLastModified", "ServerRelativeUrl", "TimeCreated"]
            from_datetime = datetime.datetime(cutoff_year, cutoff_month, cutoff_day, 0, 0)
            filter_text = "TimeLastModified lt datetime'{0}'".format(from_datetime.isoformat())
            folders = libraryFolderroot.folders.filter(filter_text).select(include_fields).get().execute_query()
            files = libraryFolderroot.files.filter(filter_text).select(include_fields).get().execute_query()

            return folders, files #Combine these outputs as a consolidated list. Folders should be distinguished from files based on if they end in a "/" or "\"
            #This operation should behave like a standard POSIX ls operation. 

        except Exception as e:
            print(repr(e)) #No print statements, use log.error("Description of function") followed by log.exception(e)


    def rm_file(self, relativeUrl):
        try:
            file_to_delete = self.ctx.web.get_folder_by_server_relative_url(relativeUrl)
            file_to_delete.delete_object()
            self.ctx.execute_query()
        except Exception as e:
            print(repr(e)) #See earlier comment on print statements


    def deleteFilesInFolder(self, timeInDays):

        try:

            folders, files = self.ls_files() #replace with self.run_audit(), ls method needs to be more generic than it's implimentation here.

            log.info("Total folders to delete : " + str(len(folders)))
            log.info("Total files to delete : " + str(len(files)))

            for item in folders:
                log.info("Folder url: %s", item.properties["ServerRelativeUrl"])
                log.info("CreatedDate: %s", item.properties["TimeCreated"])
                log.info("LastModifiedDate: %s", item.properties["TimeLastModified"])
                self.rm_file(item.properties["ServerRelativeUrl"])
                log.info("Folder Deleted")

            for item in files:
                log.info("File url: %s", item.properties["ServerRelativeUrl"])
                log.info("CreatedDate: %s", item.properties["TimeCreated"])
                log.info("LastModifiedDate: %s", item.properties["TimeLastModified"])
                self.rm_file(item.properties["ServerRelativeUrl"])
                log.info("File Deleted")

        except Exception as e:
            print(repr(e)) #See previous comment on print statements


    def info(self):
        '''Returns info dict'''
        #Where is the information dictionary about this enpoint type?

#It would be much better to test that you can initialize this through the factory.
if __name__ == '__main__':
    initMethod = SharePoint("Example", "ITSSharepointSite", 300)