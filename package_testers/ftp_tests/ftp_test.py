from package_testers.ftp_tests.ftp_test_factory import ftp_tester_factory
from package_testers.ftp_tests.ftp_units import FTP_SECRETS

ftp_tests = {endpoint: ftp_tester_factory(endpoint) for endpoint in FTP_SECRETS}