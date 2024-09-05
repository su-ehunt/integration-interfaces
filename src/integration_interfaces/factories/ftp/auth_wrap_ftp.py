import logging
import os

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
)
log = logging.getLogger("logger")

def auth_wrap_ftp(self,func):

    def wrap(*args,**kwargs):
        class_instance = args[0]
        try:
            class_instance.establish_connection()
            func(*args,**kwargs)
        except Exception as e:
            log.exception(e)
            raise e
        finally:
            class_instance.close_connection()
    return wrap