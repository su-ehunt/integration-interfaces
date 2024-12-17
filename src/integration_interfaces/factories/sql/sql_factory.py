from integration_interfaces.logging import log
from integration_interfaces.aws.secrets_manager import get_secret_json
from integration_interfaces.factories.sql.sql_server_protocol import SQLServer
from integration_interfaces.factories.sql.sql_protocols import SQL_PROTOCOLS

def sql_factory(db_secret,cred_secret) -> type[SQLServer]:
    """
    SQL Factory takes in a secret describing the database in the first 
    argument, and connection credentials in the second, and returns a sql server object
    """
    db_connection_vals = get_secret_json(db_secret)
    db_auth = get_secret_json(cred_secret)
    auth = db_connection_vals["auth"].lower()
    try:
        sql_method = SQL_PROTOCOLS[auth]
    except KeyError as e:
        log.error(f'No Auth method matching {auth} found in {SQL_PROTOCOLS.keys()}')
        log.error(f'Please make sure you spelled the auth method correctly, or to add a new auth method')
    except Exception as e:
        log.exception(e)
        raise e
    try:
        unauath_serv = sql_method(db_connection_vals, db_secret)
    except Exception as e:
        log.error(f'Failed to initialize SQL class. Make sure the secret stored in {db_secret}\
                  has all the required fields for initiating a {auth} SQL server.')
        log.exception(e)
        raise e
    try:
        unauath_serv.load_auth(db_auth,cred_secret)
        return unauath_serv
    except Exception as e:
        log.exception(e)
        raise e
