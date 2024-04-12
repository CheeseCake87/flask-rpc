import typing as t

from flask import Flask, Blueprint, request
from pydantic import BaseModel, ValidationError


class RPCModel(BaseModel):
    frpc: float
    function: str
    data: t.Any


class RPCRequest:
    @classmethod
    def build(cls, function: str, data: t.Optional[dict[str, t.Any]] = None) -> dict[str, t.Any]:
        return {
            "frpc": 1.0,
            "function": function,
            "data": data
        }


class RPCResponse:
    @classmethod
    def failed_response(cls, message: str = None, data: dict[str, t.Any] = None):
        r = {"frpc": 1.0, "ok": False}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r

    @classmethod
    def successful_response(cls, data: dict[str, t.Any] = None, message: str = None):
        r = {"frpc": 1.0, "ok": True}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r


class RPC:
    LOOKUP: dict[str, t.Callable]

    def __init__(self, app_or_blueprint: t.Union[Flask, Blueprint], url_prefix: str = "/"):
        self.LOOKUP = {}

        if not hasattr(app_or_blueprint, "add_url_rule"):
            raise TypeError(
                f"Looks like {app_or_blueprint}, type({type(app_or_blueprint)}) might "
                f"not be an instance of Flask, Flask Blueprint or be compatible with "
                "setting Flask routes."
            )

        self._register_route(app_or_blueprint, url_prefix)

    def functions(self, **kwargs: t.Callable):
        for k, v in kwargs.items():
            self.LOOKUP[k] = v

    def _register_route(self, route_compatible: t.Union[Flask, Blueprint], url_prefix: str):
        route_compatible.add_url_rule(
            url_prefix,
            view_func=self._rpc_route,
            provide_automatic_options=True,
            methods=["POST"],
        )

    def _rpc_route(self):
        if not request.is_json:
            return RPCResponse.failed_response("Request must be JSON.")

        if not request.json:
            return RPCResponse.failed_response("Request must not be empty.")

        if not request.json.get("frpc") == 1.0:
            return RPCResponse.failed_response("Invalid Flask-RPC version.")

        try:
            rpcm = RPCModel(**request.json)
        except ValidationError:
            return RPCResponse.failed_response("Invalid request.")

        try:
            assert rpcm.function in self.LOOKUP
        except AssertionError:
            return RPCResponse.failed_response("Invalid function.")

        if successful_response := self.LOOKUP[rpcm.function](params=rpcm.data):
            return successful_response

        return RPCResponse.failed_response("Unsuccessful command execution.")


__all__ = ["RPC", "RPCResponse", "RPCModel"]
