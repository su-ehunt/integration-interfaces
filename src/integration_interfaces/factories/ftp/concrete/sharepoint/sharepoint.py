import os
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from datetime import date, timedelta
import datetime
from src.integration_interfaces.aws.secrets_manager import get_secret_json, get_secret
from src.integration_interfaces.logging import log

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

    def __init__(self, sharepointFolder, sharepointSite, timeInDays):

        self.tenant = 'redhawks.onmicrosoft.com'
        self.timeIndays = timeInDays
        self.sharepoint_site_secrets = get_secret_json(sharepoint_site_secret_name)
        self.sharepoint_doc_library = sharepointFolder
        self.sharepoint_full_url = self.sharepoint_site_secrets['sharepoint_base_url'] + '/sites/' + sharepointSite
        self.sharepoint_relative_url = self.sharepoint_site_secrets['sharepoint_site_url'] + '/' + self.sharepoint_doc_library

        self.ms_secrets = get_secret_json(self.sharepoint_site_secrets['sharepoint_auth'])

        clss_sp_pem = get_secret(self.sharepoint_site_secrets['sharepoint_cert'])
        with open(cert_path, "w", newline='') as temp_pem:
            temp_pem.write(clss_sp_pem)

        self.cert_settings = {
            'client_id': self.ms_secrets['client_id'],
            'thumbprint': self.ms_secrets['thumbprint'],
            'cert_path': self.cert_path,
            'scopes': [self.ms_secrets['scopes']]
        }


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
            exit()

    def push_file(self, filename, file_content):
        '''Push File to FTP'''
        log.info('Connecting to SFS SharePoint site to push ' + filename + ' for archival')

        log.info('Uploading ' + filename + ' to SharePoint')
        sharepoint_remote_path = self.sharepoint_doc_library + filename
        sp_dir, name = os.path.split(sharepoint_remote_path)

        file = self.ctx.web.get_folder_by_server_relative_url(sp_dir).upload_file(name, file_content).execute_query()
        log.info('Successfully uploaded ' + filename + ' to SharePoint')


    def ls_files(self):
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

            return folders, files

        except Exception as e:
            print(repr(e))


    def rm_file(self, relativeUrl):
        try:
            file_to_delete = self.ctx.web.get_folder_by_server_relative_url(relativeUrl)
            file_to_delete.delete_object()
            self.ctx.execute_query()
        except Exception as e:
            print(repr(e))


    def deleteFilesInFolder(self, timeInDays):

        try:

            folders, files = self.ls_files()

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
            print(repr(e))


    def info(self):
        '''Returns info dict'''


if __name__ == '__main__':
    initMethod = SharePoint("Example", "ITSSharepointSite", 300)