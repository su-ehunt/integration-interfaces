from src.integration_interfaces.factories import sql_factory
from package_testers.sql_tests.concrete_sql_tests import PyodbcSQLTester
from package_testers.sql_tests.sql_test_protocol import SQLUnitTester

def sql_tester_factory(secret_tuple) -> type[SQLUnitTester]:
    db_name = secret_tuple[0]
    cred_name = secret_tuple[1]
    sql_server = sql_factory(db_name,cred_name)
    return PyodbcSQLTester(sql_server)
