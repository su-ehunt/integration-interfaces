
from integration_interfaces.aws.secrets_manager import get_secret_json
from integration_interfaces.logging import log
from integration_interfaces.factories.ftp.ftp_server_protocol import FTPServer
from integration_interfaces.factories.ftp.ftp_protocols import FTP_PROTOCOLS


def ftp_factory(secret_name) -> FTPServer:
    """Function to take in a secret and return the endpoint object we want"""
    secret = get_secret_json(secret_name)
    auth = secret["auth"].lower()
    try:
        ftp_method = FTP_PROTOCOLS[auth]
    except KeyError:
        log.error(f'No Auth method matching {auth} found in {FTP_PROTOCOLS.keys()}')
        log.error(f'Please make sure you spelled the auth method correctly, or to add a new auth method')
    except Exception as e:
        log.exception(e)
        raise e
    try:
        return ftp_method(secret,secret_name)
    except Exception as e:
        log.error(f'Failed to initialize FTP class. Make sure the secret stored in {secret_name}\
                  has all the required fields for initiating a {auth} FTP server.')
        log.exception(e)
        raise e

