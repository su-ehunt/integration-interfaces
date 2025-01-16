import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

from datetime import date, timedelta
import datetime
from integration_interfaces.aws.secrets_manager import get_secret_json, get_secret
from integration_interfaces.logging import log
from integration_interfaces.aws.client_session import client


    def __init__(self,secret: dict,secret_name: str):

        if 'sharepoint_auth' in secret.keys():
            cert_secret = secret['sharepoint_auth']
        else:
            cert_secret = 'Microsoft_Sharepoint_Auth'

        if 'sharepoint_cert' in secret.keys():
            self.sharepoint_pkey = secret['sharepoint_cert']
        else:
            self.sharepoint_pkey = 'Microsoft_Certificate'   

    def __init__(self):
        if 'tenant' in secret.keys():
            self.tenant = secret['tenant']
        else:
            self.tenant = 'redhawks.onmicrosoft.com'

        self.ctx = None
        # self.sharepoint_doc_library = sharepointFolder
        self.sharepoint_full_url = self.sharepoint_site_secrets['sharepoint_base_url'] + '/sites/' + self.sharepoint_site_secrets['sharepoint_site_name']
        # self.sharepoint_relative_url = self.sharepoint_site_secrets['sharepoint_site_url'] + '/' + self.sharepoint_doc_library
        if 'base_dir' in secret.keys():
            self.base_dir = secret['base_dir']
        else:
            self.base_dir = ''
        
        if 'sharepoint_base_url' in secret.keys():
            self.sharepoint_base_url = secret['sharepoint_base_url']
        else:
            self.sharepoint_base_url = 'https://redhawks.sharepoint.com'


        self.cert_settings = {
            'client_id': self.ms_secrets['client_id'],
            'thumbprint': self.ms_secrets['thumbprint'],
            'cert_path': cert_path,
            'scopes': [self.ms_secrets['scopes']]
        }

        clss_sp_pem = get_secret(client, self.sharepoint_site_secrets['sharepoint_cert'])
        with open(cert_path, "w",
class SharePointFTP():
                  newline='') as temp_pem:
            temp_pem.write(clss_sp_pem)

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


    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
    def pull_file(self,file_name,remote_path):

        if not self.connected():
            self.establish_connection()

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
            raise Exception('File does not exist')


    def push_file(self, filename, file_content, target_folder_url):
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
        '''Push File to FTP'''
        if not self.connected():
            self.establish_connection()

        log.info('Connecting to SFS SharePoint site to push ' + filename + ' for archival')

        log.info('Uploading ' + filename + ' to SharePoint')
        sharepoint_remote_path = target_folder_url + filename
        sp_dir, name = os.path.split(sharepoint_remote_path)

        file = self.ctx.web.get_folder_by_server_relative_url(sp_dir).upload_file(name, file_content).execute_query()
        log.info('Successfully uploaded ' + filename + ' to SharePoint')


    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
    def ls_files(self, target_folder_url):

        ListofItems = []

        try:
            if not self.connected():
                self.establish_connection()

            libraryFolderroot = self.ctx.web.get_folder_by_server_relative_url(target_folder_url)
            self.ctx.load(libraryFolderroot)
            self.ctx.execute_query()
            libraryFolderroot.expand(["Files", "Folders"]).get().execute_query()

            for item in libraryFolderroot.files:
                ListofItems.append(item.properties["ServerRelativeUrl"])

            for item in libraryFolderroot.folders:
                ListofItems.append(item.properties["ServerRelativeUrl"])

        except Exception as e:
            log.exception(e)
            raise e

        return ListofItems


    def filter_files(self, target_folder_url):
        log.info('Connecting to SharePoint site to delete')

        try:
            if not self.connected():
                self.establish_connection()

            libraryFolderroot = self.ctx.web.get_folder_by_server_relative_url(target_folder_url)
            self.ctx.load(libraryFolderroot)
            self.ctx.execute_query()

            cutoff_date = (date.today() - timedelta(days=self.sharepoint_site_secrets['time_in_days']))
            log.info("Cutoff date :  " + str(cutoff_date))
            cutoff_year = cutoff_date.year
            cutoff_month = cutoff_date.month
            cutoff_day = cutoff_date.day

            include_fields = ["TimeLastModified", "ServerRelativeUrl", "TimeCreated"]
            from_datetime = datetime.datetime(cutoff_year, cutoff_month, cutoff_day, 0, 0)
            filter_text = "TimeLastModified lt datetime'{0}'".format(from_datetime.isoformat())
            folders = libraryFolderroot.folders.filter(filter_text).select(include_fields).get().execute_query()
            files = libraryFolderroot.files.filter(filter_text).select(include_fields).get().execute_query()

            return folders, files

        except Exception as e:
            log.exception(e)
            raise e


    def rm_file(self, relativeUrl):
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
        try:
            if not self.connected():
                self.establish_connection()

            file_to_delete = self.ctx.web.get_folder_by_server_relative_url(relativeUrl)
            file_to_delete.delete_object()
            self.ctx.execute_query()

        except Exception as e:
            log.exception(e)
            raise e


    def deleteFilesInFolder(self, target_folder_url):

        try:

            folders, files = self.filter_files(target_folder_url)

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
            log.exception(e)
            raise e


    def info(self):
        '''Returns info dict'''
        #Where is the information dictionary about this enpoint type?
