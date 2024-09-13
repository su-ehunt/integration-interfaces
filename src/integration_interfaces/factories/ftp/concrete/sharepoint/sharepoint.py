import logging
import os
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from datetime import date, timedelta
import datetime
from src.integration_interfaces.aws.secrets_manager import get_secret_json, get_secret
from tenacity import retry, stop_after_attempt, wait_exponential

# Set logging variables
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'),
                    format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')
log = logging.getLogger('logger')

canvas_secret_name = 'Canvas_SIS'
ms_secret_name = 'Microsoft_Sharepoint_Auth'
mscert_secret_name = 'Microsoft_Certificate'
cert_path = '/tmp/temp_pem.pem'
time_format = '%Y-%m-%dT%H:%M:%SZ'

class SharePoint:

    def __init__(self, sharepointFolder, sharepointSite, timeInDays):

        self.tenant = 'redhawks.onmicrosoft.com'
        self.timeIndays = timeInDays
        canvas_secrets = get_secret_json(canvas_secret_name)
        self.sharepoint_user = canvas_secrets['sharepoint_sa_user']
        self.sharepoint_password = canvas_secrets['sharepoint_sa_password']
        self.sharepoint_base_url = canvas_secrets['sharepoint_base_url']
        self.sharepoint_site_url = canvas_secrets['sharepoint_site_url']
        self.sharepoint_doc_library = sharepointFolder
        self.sharepoint_full_url = self.sharepoint_base_url + '/sites/' + sharepointSite
        # self.sharepoint_relative_url = self.sharepoint_site_url + '/' + self.sharepoint_doc_library

        ms_secrets = get_secret_json(ms_secret_name)
        self.client_id = ms_secrets['client_id']
        self.thumbprint = ms_secrets['thumbprint']
        self.scopes = ms_secrets['scopes']

        clss_sp_pem = get_secret(mscert_secret_name)
        with open(cert_path, "w", newline='') as temp_pem:
            temp_pem.write(clss_sp_pem)

        self.cert_settings = {
            'client_id': self.client_id,
            'thumbprint': self.thumbprint,
            'cert_path': self.cert_path,
            'scopes': [self.scopes]
        }


    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=30))
    def auth(self):
        log.info('Begin SharePoint authentication')
        #ctx_auth = AuthenticationContext(sharepoint_full_url)
        #ctx_auth.acquire_token_for_user(self.sp_user, self.sp_pw)
        #ctx = ClientContext(sharepoint_full_url, ctx_auth)

        self.ctx = ClientContext(self.sharepoint_full_url).with_client_certificate(self.tenant, **self.cert_settings)
        log.info('Successfully connected to ' + self.sharepoint_full_url)


    '''def download_file(self):
        log.info('Connecting to SFS SharePoint site to download ' + self.file_name + ' from SharePoint')
        sharepoint_relative_url, ctx = self.auth()

        log.info('Downloading ' + self.file_name + ' from SharePoint')
        sharepoint_file_url = sharepoint_relative_url + self.file_name
        response = File.open_binary(ctx, sharepoint_file_url)

        if response.status_code == requests.codes.ok:
            with open(self.file_name, 'wb') as local_file:
                local_file.write(response.content)
            log.info('Successfully downloaded ' + self.file_name + ' from SharePoint')
        else:
            log.info(self.file_name + ' does not exist in SharePoint. Exiting Process.')
            exit()'''

    def upload_file(self,file_name,file_content):
        log.info('Connecting to SFS SharePoint site to push ' + file_name + ' for archival')

        log.info('Uploading ' + file_name + ' to SharePoint')
        sharepoint_remote_path = self.sp_doc + file_name
        sp_dir, name = os.path.split(sharepoint_remote_path)

        file = self.ctx.web.get_folder_by_server_relative_url(sp_dir).upload_file(name, file_content).execute_query()
        log.info('Successfully uploaded ' + file_name + ' to SharePoint')


    def filterFoldersFiles(self):
        log.info('Connecting to SharePoint site to delete')

        try:
            target_folder_url = self.sp_doc
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

    def deleteFolder(self, relativeUrl):
        try:
            file_to_delete = self.ctx.web.get_folder_by_server_relative_url(relativeUrl)
            file_to_delete.delete_object()
            self.ctx.execute_query()
        except Exception as e:
            print(repr(e))

    def deleteFile(self, relativeUrl):
        try:
            file_to_delete = self.ctx.web.get_file_by_server_relative_url(relativeUrl)
            file_to_delete.delete_object()
            self.ctx.execute_query()
        except Exception as e:
            print(repr(e))

    def deleteContentInFolder(self, timeInDays):

        try:

            folders, files = self.filterFoldersFiles()

            log.info("Total folders to delete : " + str(len(folders)))
            log.info("Total files to delete : " + str(len(files)))

            for item in folders:
                log.info("Folder url: %s", item.properties["ServerRelativeUrl"])
                log.info("CreatedDate: %s", item.properties["TimeCreated"])
                log.info("LastModifiedDate: %s", item.properties["TimeLastModified"])
                self.deleteFolder(item.properties["ServerRelativeUrl"])
                log.info("Folder Deleted")

            for item in files:
                log.info("File url: %s", item.properties["ServerRelativeUrl"])
                log.info("CreatedDate: %s", item.properties["TimeCreated"])
                log.info("LastModifiedDate: %s", item.properties["TimeLastModified"])
                self.deleteFile(item.properties["ServerRelativeUrl"])
                log.info("File Deleted")

        except Exception as e:
            print(repr(e))

