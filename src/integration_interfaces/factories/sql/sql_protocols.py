from typing import Dict
from integration_interfaces.factories.sql.pyodbcsql import Pyodbc18SQLAuthSQLServer
from integration_interfaces.factories.sql.sql_server_protocol import SQLServer


SQL_PROTOCOLS: Dict[str,type[SQLServer]] = {
    "pyodbc18-sql-auth": Pyodbc18SQLAuthSQLServer
}
