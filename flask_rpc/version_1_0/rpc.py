import typing as t

from flask import Blueprint, Flask, request, session
from pydantic import ValidationError

from ._protocols import RPCAuthSessionKey
from .model import RPCModel
from .response import RPCResponse
from .utilities import snake_case


class RPC:
    LOOKUP: t.Dict[str, t.Callable]

    _host_auth: t.List[str]
    _session_auth: t.Union[RPCAuthSessionKey, t.List[RPCAuthSessionKey]]

    def __init__(
        self,
        app_or_blueprint: t.Union[Flask, Blueprint],
        functions: t.Optional[t.Dict[str, t.Callable]] = None,
        url_prefix: str = "/",
        host_auth: t.Optional[t.List[str]] = None,
        session_auth: t.Optional[
            t.Union[RPCAuthSessionKey, t.List[RPCAuthSessionKey]]
        ] = None,
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

        if host_auth:
            self.host_auth(host_auth)
        else:
            self.host_auth([])

        if session_auth:
            self.session_auth(session_auth)
        else:
            self.session_auth([])

    def host_auth(self, hosts: t.List[str]):
        self._host_auth = hosts

    def session_auth(
        self, auth_session_keys: t.Union[RPCAuthSessionKey, t.List[RPCAuthSessionKey]]
    ):
        self._session_auth = auth_session_keys

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
        if not url_prefix.startswith("/"):
            url_prefix = f"/{url_prefix}"

        _default = ("/", "/rpc")
        _blueprint_name = ""
        if isinstance(route_compatible, Blueprint):
            _blueprint_name = f"_{route_compatible.name}"

        route_compatible.add_url_rule(
            url_prefix,
            view_func=self._rpc_route,
            endpoint="_rpc"
            if url_prefix in _default
            else f"_rpc{_blueprint_name}_{snake_case(url_prefix)}",
            provide_automatic_options=True,
            methods=["POST"],
        )

    def _rpc_route(self):
        if not self.LOOKUP:
            return RPCResponse.fail("No functions registered.")

        if self._session_auth:
            if isinstance(self._session_auth, RPCAuthSessionKey):
                if not self._session_auth.check(session):
                    return RPCResponse.fail("Unauthorized.")

            if isinstance(self._session_auth, list):
                for auth_session_key in self._session_auth:
                    if isinstance(auth_session_key, RPCAuthSessionKey):
                        if not auth_session_key.check(session):
                            return RPCResponse.fail("Unauthorized.")
                    else:
                        raise ValueError("Invalid session_auth type.")

        if self._host_auth:
            if request.host not in self._host_auth:
                return RPCResponse.fail(f"Unauthorized ({request.host})")

        if not request.is_json:
            return RPCResponse.fail("Request must be JSON.")

        _json = request.get_json()

        if not _json:
            return RPCResponse.fail("Request must not be empty.")

        if not _json.get("wrpc") == 1.0:
            return RPCResponse.fail("Invalid wrpc version.")

        try:
            rpcm = RPCModel(**_json)
        except ValidationError:
            return RPCResponse.fail("Invalid request.")

        try:
            assert rpcm.function in self.LOOKUP
        except AssertionError:
            return RPCResponse.fail("Invalid function.")

        if successful_response := self.LOOKUP[rpcm.function](rpcm.data):
            return successful_response

        return RPCResponse.fail("Unsuccessful command execution.")
