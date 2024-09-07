from typing import Protocol

class FTPServer(Protocol):
    """Base Protocol class for our FTP endpoints"""
    
    def establish_connection(self,secret):
        '''Initialize connection'''

    def close_connection(self):
        '''Closes FTP connection'''
    
    def connected(self):
        '''Returns whether or not the FTP connection is established'''

    def push_file(self,filename,remote_path):
        '''Push File to FTP'''

    def pull_file(self,filename,remote_path):
        '''Pul File from FTP'''

    def ls_files(self,remote_path):
        '''List Files in Directory'''

    def rm_file(self,filename):
        '''Deletes Remote File'''