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
        data: t.Union[
            str, int, float, bool, t.List[t.Any], t.Dict[str, t.Any], None
        ] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Build a request.

        Version 1.0.

        :param function: Str
        :param data: Any (JSON serializable)
        :return:
        """
        return {"frpc": 1.0, "function": function, "data": data}


class RPCResponse:
    @classmethod
    def fail(
        cls,
        message: str = None,
        data: t.Union[
            str, int, float, bool, t.List[t.Any], t.Dict[str, t.Any], None
        ] = None,
    ):
        """
        Return a failed response.

        Version 1.0.

        :param message: Str
        :param data: Any (JSON serializable)
        :return:
        """
        r = {"frpc": 1.0, "ok": False}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r

    @classmethod
    def success(
        cls,
        data: t.Union[
            str, int, float, bool, t.List[t.Any], t.Dict[str, t.Any], None
        ] = None,
        message: str = None,
    ):
        """
        Return a successful response.

        Version 1.0.

        :param data: Any (JSON serializable)
        :param message: Str
        :return:
        """
        r = {"frpc": 1.0, "ok": True}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r


class RPC:
    LOOKUP: t.Dict[str, t.Callable]

    def __init__(
        self,
        app_or_blueprint: t.Union[Flask, Blueprint],
        url_prefix: str = "/",
        functions: t.Dict[str, t.Callable] = None,
    ):
        """
        Register the RPC route.

        :param app_or_blueprint: Flask / Blueprint
        :param url_prefix: Str
        """
        self.LOOKUP = {}

        if not hasattr(app_or_blueprint, "add_url_rule"):
            raise TypeError(
                f"Looks like {app_or_blueprint}, type({type(app_or_blueprint)}) might "
                f"not be an instance of Flask, Flask Blueprint or be compatible with "
                "setting Flask routes."
            )

        self._register_route(app_or_blueprint, url_prefix)

        if functions:
            self.functions(**functions)

    def functions(self, **kwargs: t.Callable):
        """
        Register RPC functions.

        remote_name=local_name

        :param kwargs:
        :return: None
        """
        for k, v in kwargs.items():
            if not callable(v):
                raise TypeError(f"Expected a callable, got {type(v)}.")

            if not v.__name__:
                raise ValueError(f"Callable {v} must have a name.")

            if k in self.LOOKUP:
                raise ValueError(f"Function {k} already exists.")

            self.LOOKUP[k] = v

    def functions_auto_name(self, functions: t.Iterable[t.Callable]):
        """
        Register RPC functions with their local names.

        remote_name=local_name

        remote_name will always be the name of the function.

        :param functions: Iterable of functions
        :return: None
        """
        for f in functions:
            if not callable(f):
                raise TypeError(f"Expected a callable, got {type(f)}.")

            if not f.__name__:
                raise ValueError(f"Callable {f} must have a name.")

            if f.__name__ in self.LOOKUP:
                raise ValueError(f"Function {f.__name__} already exists.")

            self.LOOKUP[f.__name__] = f

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
            return RPCResponse.fail("Invalid frpc version.")

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
