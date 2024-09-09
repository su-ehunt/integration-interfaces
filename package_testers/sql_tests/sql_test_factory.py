from src.integration_interfaces.factories import sql_factory
from package_testers.ftp_tests.concrete_ftp_tests import FTPFullTester,FTPROTester
from package_testers.ftp_tests.ftp_test_protocol import FTPUnitTester

def sql_tester_factory(secret_tuple) -> type[FTPUnitTester]:
    db_name = secret_tuple[0]
    cred_name = secret_tuple[1]
    ftp_server = sql_factory(db_name,cred_name)
    if ftp_server.auth[0:3] == 'ro_':
        return FTPROTester(ftp_server)
    else:
        return FTPFullTester(ftp_server)
    

