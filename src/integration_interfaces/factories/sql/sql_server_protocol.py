from typing import Protocol
from pandas import DataFrame

class SQLServer(Protocol):
    """Base protocol class for SQL servers"""
    
    def load_auth(self,creds,cred_secret_name) -> None:
        """Loads in authorization information"""

    def open_sql_connection(self) -> None:
        """Opens SQL connection"""

    def close_sql_connection(self) -> None:
        """Close the SQL connection"""
    
    def get_sql_data(self,sql) -> tuple[list,list]:
        """Returns SQL query result as rows,columnnames"""

    def get_sql_data_pd(self,sql) -> DataFrame:
        """Returns SQL query result as Pandas DataFrame"""
    
    def info(self):
        """Returns dict describing endpoint"""