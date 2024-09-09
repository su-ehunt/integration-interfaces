from functools import wraps
from integration_interfaces.logging import log

def auth_wrap_ftp(func=None, *, apply_wrap=True):
    if func is None:
        return lambda f: auth_wrap_ftp(f, apply_wrap=apply_wrap)

    '''Authenticates and closes FTP connection around FTP interaction
    This avoids having any dangling FTP connections during runtime.'''
    @wraps(func)
    def wrap(*args,**kwargs):
        class_instance = args[0]
        log.info('Checking if underclass has updated wrapper')
        log.info(f'{class_instance.apply_wrap}')
        if class_instance.apply_wrap == True:
             #Should return self as first arg of class method
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
        else:
            if not class_instance.connected():
                class_instance.establish_connection()
            return func(*args,**kwargs)
    return wrap