from integration_interfaces.aws import session
from integration_interfaces.logging import log

class S3FTP():

    apply_wrap = True

    def __init__(self,secret,secret_name) -> None:
        self.secret_name =secret_name
        self.bucket_name = secret['bucket']
        self.auth = secret['auth']
        self.s3 = None
        self.bucket = None
        self.establish_connection()
    
    def establish_connection(self):
        '''Initialize connection'''
        if not self.connected():
            log.info(f"Connecting to S3 Bucket {self.bucket_name}")
            self.s3 = session.resource('s3')
            self.bucket = self.s3.Bucket(self.bucket_name)

    def close_connection(self):
        '''Closes FTP connection'''
        log.info("No need to close me! I'm an AWS session! It's useful\
                  to keep me open durring the runtime!")
    
    def connected(self):
        '''Returns whether or not the FTP connection is established'''
        return self.s3 is not None
    
    def push_file(self,filename,remote_path):
        '''Push File to FTP'''
        log.info(f"Uploading {filename} to {remote_path} in S3 Bucket \
                 {self.bucket_name} per config in {self.secret_name}")
        self.s3.meta.client.upload_file(filename, self.bucket_name, remote_path)

    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''
        log.info(f"Downloading {remote_path} to {filename} in S3 Bucket \
                 {self.bucket_name} per config in {self.secret_name}")
        self.s3.meta.client.download_file(filename, self.bucket_name, remote_path)

    def ls_files(self,remote_path):
        '''List Files in Directory'''
        log.warning("Doing a list operation in a bucket store is potentially costly\
                    Please be aware of when you invoke an ls like operation on bucket storage.")
        return [self.bucket.objects.all()]

    def rm_file(self,filename):
        '''Deletes Remote File'''
        log.info(f"Deleting {filename} in S3 Bucket \
                 {self.bucket_name} per config in {self.secret_name}")
        obj = self.s3.Object(self.bucket_name, filename)
        obj.delete()

    def info(self):
        '''Returns info dict'''