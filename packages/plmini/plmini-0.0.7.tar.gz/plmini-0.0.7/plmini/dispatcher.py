from typing import Optional

from .client import Client

__all__ = ['Dispatcher']


class Dispatcher:
    host: str
    port: int

    client: Optional[Client]

    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = Client(self.host, self.port)

    def close(self):
        if self.client is not None:
            self.client.close()

    def __call__(self, driver: str, op: str):
        self.client.dispatch(driver, op)

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
