import json
from typing import Any, Callable, List

import grpc
from jsonschema import validate

from .pb import plmini_pb2, plmini_pb2_grpc

__all__ = ['Client']


class DriverInfo:
    driver: str
    schema: str
    ops: List[str]
    state: Any
    dispatch: Callable[[str]]

    def __init__(self, driver: str, schema: str, ops: List[str], state: Any, dispatch: Callable[[str]]):
        self.driver = driver
        self.schema = schema
        self.ops = ops
        self.state = state
        self.dispatch = dispatch


class Client:
    channel: grpc.Channel
    stub: plmini_pb2_grpc.OperatorStub

    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.channel = grpc.insecure_channel('{}:{}'.format(host, port))
        self.stub = plmini_pb2_grpc.OperatorStub(self.channel)

    def close(self):
        self.channel.close()

    def register(self, driver: str, schema: dict, ops: List[str]) -> bytes:
        res = self.stub.Register(plmini_pb2.RegisterRequest(
            driver=driver,
            schema=json.dumps(schema),
            ops=ops,
        ))
        return res.token

    def subscribe(self, driver: str, token: str):
        stream = self.stub.Subscribe(plmini_pb2.SubscribeRequest(
            driver=driver,
            token=token,
        ))
        return map(lambda req: req.op, stream)

    def dispatch(self, driver: str, op: str):
        self.stub.Dispatch(plmini_pb2.DispatchRequest(
            driver=driver,
            op=op,
        ))

    def heartbeat(self, driver: str, token: str):
        self.stub.Heartbeat(plmini_pb2.HeartbeatRequest(
            driver=driver,
            token=token,
        ))

    def disconnect(self, driver: str, token: str):
        self.stub.Disconnect(plmini_pb2.DisconnectRequest(
            driver=driver,
            token=token,
        ))

    def update(self, driver: str, token: str, instance: Any):
        self.stub.Update(plmini_pb2.UpdateRequest(
            driver=driver,
            token=token,
            value=json.dumps(instance),
        ))

    def list(self) -> List[str]:
        return self.stub.List(plmini_pb2.Empty()).drivers

    def info(self, driver: str) -> DriverInfo:
        res = self.stub.Driver(plmini_pb2.DriverRequest(driver=driver))
        schema = json.loads(res.schema)
        ops = res.ops
        state = json.loads(res.state)
        validate(instance=state, schema=schema)
        def dispatch(op: str): return self.client.dispatch(driver, op)
        return DriverInfo(
            driver=driver,
            schema=schema,
            ops=ops,
            state=state,
            dispatch=dispatch,
        )
