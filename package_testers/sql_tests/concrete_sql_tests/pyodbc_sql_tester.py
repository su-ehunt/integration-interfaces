from src.integration_interfaces.factories.sql import SQLServer
from package_testers.sql_tests.concrete_sql_tests.sql_test_snippet import sql


class PyodbcSQLTester():

    def __init__(self,sql_server: SQLServer) -> None:
        self.sql_server = sql_server

    def validate_connection(self):
        '''Validates standard push/pull/list/remove operations 
        work as intended'''
        assert self.sql_server.cnxn is None
        self.sql_server.open_sql_connection()
        assert self.sql_server.cnxn is not None
        self.sql_server.close_sql_connection()
        assert self.sql_server.cnxn is None
    
    def validate_auth_wrap(self):
        '''Validates the Auth Wrapper function is behaving as expexted'''
        assert self.sql_server.cnxn is None
        self.sql_server.get_sql_data(sql)
        assert self.sql_server.cnxn is None
        

    def run_tests(self):
        '''Run all the tests. Gives consistent interface for tests
        of different endpoint types'''
        self.validate_connection()
        self.validate_auth_wrap()

    def run_tests(self):
        self.validate_mock_file_transfer()
        self.validate_auth_wrap()

    def info(self):
        '''Return a Dict of information about this unit test'''
        info_dict = {
            "Concrete Tester Class": "Pyodbc SQL Tester",
            "Endpoint Info": self.sql_server.info()
        }
        return info_dict