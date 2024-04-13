import typing as t

from flask import Flask, Blueprint, request
from pydantic import BaseModel, ValidationError


class RPCModel(BaseModel):
    frpc: float
    function: str
    data: t.Any


class RPCRequest:
    @classmethod
    def build(
        cls,
        function: str,
        data: t.Optional[str, int, float, bool, list[t.Any], t.Dict[str, t.Any]] = None,
    ) -> t.Dict[str, t.Any]:
        return {"frpc": 1.0, "function": function, "data": data}


class RPCResponse:
    @classmethod
    def fail(
        cls,
        message: str = None,
        data: t.Optional[str, int, float, bool, list[t.Any], t.Dict[str, t.Any]] = None,
    ):
        r = {"frpc": 1.0, "ok": False}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r

    @classmethod
    def success(
        cls,
        data: t.Union[str, int, float, list, bool, t.Dict[str, t.Any]] = None,
        message: str = None,
    ):
        r = {"frpc": 1.0, "ok": True}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r


class RPC:
    LOOKUP: t.Dict[str, t.Callable]

    def __init__(
        self, app_or_blueprint: t.Union[Flask, Blueprint], url_prefix: str = "/"
    ):
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

    def _register_route(
        self, route_compatible: t.Union[Flask, Blueprint], url_prefix: str
    ):
        route_compatible.add_url_rule(
            url_prefix,
            view_func=self._rpc_route,
            provide_automatic_options=True,
            methods=["POST"],
        )

    def _rpc_route(self):
        if not request.is_json:
            return RPCResponse.fail("Request must be JSON.")

        if not request.json:
            return RPCResponse.fail("Request must not be empty.")

        if not request.json.get("frpc") == 1.0:
            return RPCResponse.fail("Invalid Flask-RPC version.")

        try:
            rpcm = RPCModel(**request.json)
        except ValidationError:
            return RPCResponse.fail("Invalid request.")

        try:
            assert rpcm.function in self.LOOKUP
        except AssertionError:
            return RPCResponse.fail("Invalid function.")

        if successful_response := self.LOOKUP[rpcm.function](rpcm.data):
            return successful_response

        return RPCResponse.fail("Unsuccessful command execution.")


__all__ = ["RPC", "RPCResponse", "RPCModel"]
