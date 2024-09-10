from integration_interfaces.factories.ftp import FTPServer
from package_testers.ftp_tests.concrete_ftp_tests.params import MOCK_FILE_NAME
import os

class FTPFullTester():
    def __init__(self,ftp_server: FTPServer) -> None:
        self.ftp_server = ftp_server
    
    def validate_mock_file_transfer(self):
        with open(MOCK_FILE_NAME,'rw') as f:
            f.write('Hello world!')
        #ensure we can send files 
        self.ftp_server.push_file(MOCK_FILE_NAME,'/')
        os.remove(MOCK_FILE_NAME)
        #ensure file we send shows up on destination server
        files = self.ftp_server.ls_files('/'+ MOCK_FILE_NAME)
        assert MOCK_FILE_NAME in files
        #ensure we can pull files
        self.ftp_server.pull_file(MOCK_FILE_NAME,'/')
        assert MOCK_FILE_NAME in os.listdir()
        #ensure we can remove files
        self.ftp_server.rm_file(MOCK_FILE_NAME)
        updated_files = self.ftp_server.ls_files('/'+ MOCK_FILE_NAME)
        assert MOCK_FILE_NAME not in updated_files
    
    def validate_auth_wrap(self):
        pass
    
    def run_tests(self):
        self.validate_mock_file_transfer()
        self.validate_auth_wrap()

    def info(self):
        '''Return a Dict of information about this unit test'''
        info_dict = {
            "Concrete Tester Class": "FTP Full Tester",
            "Endpoint Info": self.ftp_server.info()
        }
        return info_dict
