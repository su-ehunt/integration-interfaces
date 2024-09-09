from typing import Protocol

class EndpointUnitTester(Protocol):

    def run_tests(self):
        '''Runs unit tests'''