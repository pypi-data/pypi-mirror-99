import threading
from typing import Callable, Iterator, List, Optional

from jsonschema import Draft7Validator as Validator

from .client import Client

__all__ = ['Driver']


class Interval:
    thread: threading.Thread
    event: threading.Event

    def __init__(self, interval: float, function: Callable, *args, **kwargs):
        def target():
            while not self.event.wait(interval):
                function()
        self.thread = threading.Thread(target=target, args=args, kwargs=kwargs)
        self.event = threading.Event()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.event.set()
        self.thread.join()


class Driver:
    name: str
    validator: Validator
    ops: List[str]
    host: str
    port: int

    client: Optional[Client]
    opstream: Optional[Iterator[str]]
    interval: Optional[Interval]
    token: str

    def __init__(self, name: str, schema: dict, ops: list[str], host: str = 'localhost', port: int = 5000):
        self.name = name
        self.validator = Validator(schema)
        self.ops = ops
        self.host = host
        self.port = port

        self.client = None
        self.opstream = None
        self.interval = None

    def connect(self):
        if self.client is None:
            self.client = Client(self.host, self.port)

        if self.opstream is None:
            schema = self.validator.schema
            self.token = self.client.register(self.name, schema, self.ops)

        if self.interval is None:
            self.interval = Interval(1.0, self.heartbeat)
            self.interval.start()

    def listen(self):
        return self.client.subscribe(self.name, self.token)

    def close(self):
        if self.interval is not None:
            self.interval.cancel()

        if self.client is not None:
            self.client.disconnect(self.name, self.token)
            self.client.close()

        self.client = None
        self.opstream = None
        self.interval = None

    def update(self, instance):
        self.validator.validate(instance)
        if self.client is not None:
            self.client.update(self.name, self.token, instance)

    def heartbeat(self):
        if self.client is not None:
            self.client.heartbeat(self.name, self.token)

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
