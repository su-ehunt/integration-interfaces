from integration_interfaces.factories.endpoint_factory import read_secret_to_endpoint,FTPServer
from dataclasses import dataclass

@dataclass
class Slate():
    ug_server: FTPServer
    gr_server: FTPServer
    def __init__(self) -> None:
        self.ug_server = read_secret_to_endpoint('Slate/sftp_ug_server')
        self.gr_server = read_secret_to_endpoint('Slate/sftp_gr_server')
        self.db_creds = read_secret('Slate/db_replica')
    