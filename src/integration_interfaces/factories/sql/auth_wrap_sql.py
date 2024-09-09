from integration_interfaces.logging import log

def auth_wrap_sql(func):
    '''Authenticates and closes SQL connection around SQL interaction
    This avoids having any dangling SQL connections during runtime.'''
    def wrap(*args,**kwargs):
        class_instance = args[0] #Should return self as first arg of class method
        try:
            log.info('Establishing SQL connection')
            class_instance.open_sql_connection()
            log.info('SQL Connection Established, Executing SQL method')
            return func(*args,**kwargs)
        except Exception as e:
            log.exception(e)
            raise e
        finally:
            class_instance.close_sql_connection()
    return wrap