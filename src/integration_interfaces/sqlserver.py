class SQLServer():

    def get_db_credentials(self,db_username,db_password):
        if db_username is None or db_password is None:
            raise ValueError("Need to specify both username and password for db credentials")
        self.db_username = db_username
        self.db_password = db_password

    def _open_sql_connection(self): #Protected method to make sure connections are handled responsibly

        if self.db_username is None or self.db_password is None:
            raise ValueError("No Credentials Provided for SQL Connection")
        
        log.info(f"Connecting to {self.db_server}")
        try:
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' \
                    + self.db_server + ',1433;DATABASE=' + self.db_database \
                    + ';uid=' + self.db_username + ';pwd=' + self.db_password)
            cursor = cnxn.cursor()
            log.debug('Successfully connected to ' + self.db_database)
        except Exception as e:
            log.error(e)
            raise e
    
        return cnxn, cursor
    
    def get_sql_data(self,sqlcommand):
        #Connect and retrive database object and store it in data

        log.info('Connecting to ' + self.db_database)
        cnxn, cursor = self._open_sql_connection()
        try:
            log.debug('Executing ' + self.db_database + '.' + sqlcommand)
            cursor.execute(sqlcommand)
            rows = cursor.fetchall()
            collnames = [column[0] for column in cursor.description]
            log.debug('Successfully pulled data from ' + self.db_database + '.' + sqlcommand)
        except Exception as e:
            log.error(e)
            raise e

        finally: # Ensures we close the connection even if we have an unhandeled expression https://docs.python.org/3/reference/compound_stmts.html#finally
            cnxn.commit()
            cnxn.close()
            log.info('Successfully closed SQL connection')

        return rows,collnames
    
    def get_sql_data_pd(self,sqlcommand):

        log.info('Connecting to ' + self.db_database)
        cnxn, cursor = self._open_sql_connection()
        try:
            log.debug('Executing ' + self.db_database + '.' + sqlcommand)
            data = pd.read_sql_query(sqlcommand,cnxn)
            log.debug('Successfully pulled data from ' + self.db_database + '.' + sqlcommand)
        except Exception as e:
            log.error(e)
            raise e

        finally: # Ensures we close the connection even if we have an unhandeled expression https://docs.python.org/3/reference/compound_stmts.html#finally
            cnxn.commit()
            cnxn.close()
            log.info('Successfully closed SQL connection')

        return data