from package_testers.ftp_tests import ftp_tests
from package_testers.sql_tests import sql_tests
from package_testers.test_protocol import EndpointUnitTester
from typing import Dict



assert not (ftp_tests.keys() & sql_tests.keys()) #Makes sure sql secrets and ftp secrets provided are distinct sets
tests: Dict[str,EndpointUnitTester] = ftp_tests | sql_tests
