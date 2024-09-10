from typing import Protocol

class SQLUnitTester(Protocol):

    def validate_connection(self):
        '''Validates standard push/pull/list/remove operations 
        work as intended'''
    
    def validate_auth_wrap(self):
        '''Validates the Auth Wrapper function is behaving as expexted'''

    def run_tests(self):
        '''Run all the tests. Gives consistent interface for tests
        of different endpoint types'''
    def info(self):
        '''Return a Dict of information about this unit test'''