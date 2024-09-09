from package_testers.sql_tests.sql_test_factory import sql_tester_factory
from package_testers.sql_tests.sql_units import SQL_SECRETS

sql_tests = {endpoint: sql_tester_factory(endpoint) for endpoint in SQL_SECRETS}