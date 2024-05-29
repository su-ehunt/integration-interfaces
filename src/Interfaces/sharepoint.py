import logging
import os
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

# Set logging variables
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'),
                    format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')
log = logging.getLogger('logger')


class SharePoint:
    def __init__(self, sp_base_url, sp_site, sp_doc,  sp_cert_path, sp_tenant, sp_client_id, sp_thumbprint, sp_scope):
        self.sp_base_url = sp_base_url
        self.sp_site = sp_site
        self.sp_doc = sp_doc

        #self.sp_user = sp_user
        #self.sp_pw = sp_pw

        self.sp_cert_path = sp_cert_path
        self.sp_tenant = sp_tenant
        self.sp_client_id = sp_client_id
        self.sp_thumbprint = sp_thumbprint
        self.sp_scope = sp_scope
        #self.file_name = file_name
        #self.file_archive = file_archive

    def auth(self):
        log.info('Begin SharePoint authentication')
        sharepoint_full_url = self.sp_base_url + self.sp_site
        sharepoint_relative_url = self.sp_site + '/' + self.sp_doc
        #ctx_auth = AuthenticationContext(sharepoint_full_url)
        #ctx_auth.acquire_token_for_user(self.sp_user, self.sp_pw)
        #ctx = ClientContext(sharepoint_full_url, ctx_auth)

        cert_settings = {
            'client_id': self.sp_client_id,
            'thumbprint': self.sp_thumbprint,
            'cert_path': self.sp_cert_path,
            'scopes': [self.sp_scope]
        }

        ctx = ClientContext(sharepoint_full_url).with_client_certificate(self.sp_tenant, **cert_settings)
    

        log.info('Successfully connected to ' + sharepoint_full_url)


        return sharepoint_relative_url, ctx

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
        x, ctx = self.auth()

        log.info('Uploading ' + file_name + ' to SharePoint')
        sharepoint_remote_path = self.sp_doc + file_name
        sp_dir, name = os.path.split(sharepoint_remote_path)

        file = ctx.web.get_folder_by_server_relative_url(sp_dir).upload_file(name, file_content).execute_query()
        log.info('Successfully uploaded ' + file_name + ' to SharePoint')

    '''def delete_file(self):
        log.info('Connecting to SFS SharePoint site to delete ' + self.file_name)
        sharepoint_relative_url, ctx = self.auth()

        log.info('Deleting ' + self.file_name + ' from SharePoint')
        file_rel_url = sharepoint_relative_url + self.file_name
        file_to_delete = ctx.web.get_file_by_server_relative_url(file_rel_url).delete_object().execute_query()
        log.info('Successfully deleted ' + self.file_name + ' in SharePoint')'''
