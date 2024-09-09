from src.integration_interfaces.factories import ftp_factory
from package_testers.ftp_tests.concrete_ftp_tests import FTPFullTester,FTPROTester
from package_testers.ftp_tests.ftp_test_protocol import FTPUnitTester

def ftp_tester_factory(secret_name) -> type[FTPUnitTester]:
    ftp_server = ftp_factory(secret_name)
    if ftp_server.auth[0:3] == 'ro_':
        return FTPROTester(ftp_server)
    else:
        return FTPFullTester(ftp_server)
    

