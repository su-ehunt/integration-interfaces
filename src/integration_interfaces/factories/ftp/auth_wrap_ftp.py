from integration_interfaces.logging import log

def auth_wrap_ftp(func):
    '''Authenticates and closes FTP connection around FTP interaction
    This avoids having any dangling FTP connections during runtime.'''
    def wrap(*args,**kwargs):
        class_instance = args[0] #Should return self as first arg of class method
        try:
            log.info('Establishing FTP connection')
            class_instance.establish_connection()
            log.info('FTP Connection Established, Executing FTP method')
            func(*args,**kwargs)
        except Exception as e:
            log.exception(e)
            raise e
        finally:
            class_instance.close_connection()
    return wrap