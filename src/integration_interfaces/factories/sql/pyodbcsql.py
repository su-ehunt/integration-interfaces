from dataclasses import dataclass
from integration_interfaces.logging import log
from integration_interfaces.factories.sql.auth_wrap_sql import auth_wrap_sql
import pyodbc
import pandas as pd

@dataclass
class Pyodbc18SQLAuthSQLServer():
    """
    Pyodbc server class. 
    """

    cnxn: pyodbc.Connection | None
    cursor: pyodbc.Cursor | None

    def __init__(self,secrets,db_secret_name) -> None:
        self.db_database = secrets['db_database']
        self.db_server = secrets['db_server']
        self.cnxn = None
        self.cursor = None
        self.db_username = None
        self.db_password = None
        self.auth = secrets['auth']
        self.db_secret_name = db_secret_name
        self.creds_secret_name = None

    def load_auth(self,creds,creds_secret_name):
        self.db_username = creds['db_username']
        self.db_password = creds['db_password']
        self.creds_secret_name = creds_secret_name

    def verify_auth(self):
        try:
            assert self.db_username is not None
            assert self.db_password is not None
        except Exception as e:
            log.exception("DB Credentials not loaded. Make sure to load credentials")

    def open_sql_connection(self) -> None:
        
        self.verify_auth()
        
        log.info(f"Connecting to {self.db_server}")
        try:
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' \
                    + self.db_server + ',1433;DATABASE=' + self.db_database \
                    + ';uid=' + self.db_username + ';pwd=' + self.db_password + ';Encrypt=no;TrustServerCertificate=yes')
            cursor = cnxn.cursor()
            self.cnxn = cnxn
            self.cursor = cursor
            log.debug('Successfully connected to ' + self.db_database)
        except Exception as e:
            log.error(e)
            raise e

    
    def close_sql_connection(self) -> None:
        self.cnxn.close()
        self.cursor = None

    @auth_wrap_sql
    def get_sql_data(self,sqlcommand):
        '''Connect and execute SQL and return as rows,colnames'''
        log.info('Executing ' + self.db_database + '.' + sqlcommand)
        self.cursor.execute(sqlcommand)
        rows = self.cursor.fetchall()
        collnames = [column[0] for column in self.cursor.description]
        log.info('Successfully pulled data from ' + self.db_database + '.' + sqlcommand)

        return rows,collnames
    
    @auth_wrap_sql
    def get_sql_data_pd(self,sqlcommand):
        """Connect and execute SQL and return as Pandas DataFrame"""

        log.debug('Executing ' + self.db_database + '.' + sqlcommand)
        data = pd.read_sql_query(sqlcommand,self.cnxn)
        log.debug('Successfully pulled data from ' + self.db_database + '.' + sqlcommand)


        return data
    
    def info(self):
        info_dict = {
            "Endpoint DB Secret": self.db_secret_name,
            "Endpoint Cred Secret": self.creds_secret_name,
            "Endpoint auth type": self.auth
        }
        return info_dict