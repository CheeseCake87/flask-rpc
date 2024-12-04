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
    _funcs_host_auth_lookup: t.Dict[str, t.List[str]]
    _funcs_session_auth_lookup: t.Dict[str, t.List[RPCAuthSessionKey]]

    def __init__(
        self,
        app_or_blueprint: t.Union[Flask, Blueprint],
        functions: t.Optional[t.Dict[str, t.Callable]] = None,
        url_prefix: str = "/",
        session_auth: t.Optional[
            t.Union[RPCAuthSessionKey, t.List[RPCAuthSessionKey]]
        ] = None,
        host_auth: t.Optional[t.List[str]] = None,
    ):
        """
        Register the RPC route.

        host_auth will check the request.host, setting this will mean
        that only requests from the specified hosts will be allowed.

        session_auth will check the session, setting this will mean
        that only requests with the specified session key, and value will be allowed.

        :param app_or_blueprint: Flask / Blueprint
        :param functions: Optional Dict[str, Callable]
        :param url_prefix: Str
        :param host_auth: Optional List[str]
        :param session_auth: Optional Union[RPCAuthSessionKey, List[RPCAuthSessionKey]]
        """
        self.LOOKUP = {}
        self._funcs_host_auth_lookup = {}
        self._funcs_session_auth_lookup = {}

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

    def functions(
        self,
        session_auth__: t.Optional[
            t.Union[RPCAuthSessionKey, t.List[RPCAuthSessionKey]]
        ] = None,
        host_auth__: t.Optional[t.List[str]] = None,
        **kwargs: t.Callable,
    ):
        """
        Register RPC functions.

        .functions(lookup_name_here=callable_function_here)

        host_auth will check the request.host only for the functions being
        added here. Setting this will mean that only requests from the
        specified hosts will be allowed.

        session_auth will check the session only for the functions being
        added here. setting this will mean that only requests with the specified
        session key, and value will be allowed.

        :param host_auth__: Optional List[str]
        :param session_auth__: Optional RPCAuthSessionKey or List[RPCAuthSessionKey]
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

            if session_auth__:
                if isinstance(session_auth__, RPCAuthSessionKey):
                    if k not in self._funcs_session_auth_lookup:
                        self._funcs_session_auth_lookup[k] = [session_auth__]
                    else:
                        if session_auth__ not in self._funcs_session_auth_lookup[k]:
                            self._funcs_session_auth_lookup[k].append(session_auth__)

                elif isinstance(session_auth__, list):
                    for auth_session_key in session_auth__:
                        if isinstance(auth_session_key, RPCAuthSessionKey):
                            if k not in self._funcs_session_auth_lookup:
                                self._funcs_session_auth_lookup[k] = [auth_session_key]
                            else:
                                if (
                                    auth_session_key
                                    not in self._funcs_session_auth_lookup[k]
                                ):
                                    self._funcs_session_auth_lookup[k].append(
                                        auth_session_key
                                    )

            if host_auth__:
                if k not in self._funcs_host_auth_lookup:
                    self._funcs_host_auth_lookup[k] = host_auth__
                else:
                    if host_auth__ not in self._funcs_host_auth_lookup[k]:
                        self._funcs_host_auth_lookup[k] = (
                            self._funcs_host_auth_lookup[k] + host_auth__
                        )

    def functions_auto_name(
        self,
        functions: t.Iterable[t.Callable],
        session_auth__: t.Optional[
            t.Union[RPCAuthSessionKey, t.List[RPCAuthSessionKey]]
        ] = None,
        host_auth__: t.Optional[t.List[str]] = None,
    ):
        """
        Register RPC functions with their local names.

        .functions_auto_name([callable_function_here])

        host_auth will check the request.host only for the functions being
        added here. Setting this will mean that only requests from the
        specified hosts will be allowed.

        session_auth will check the session only for the functions being
        added here. setting this will mean that only requests with the specified
        session key, and value will be allowed.

        :param functions: Iterable of functions
        :param host_auth__: Optional List[str]
        :param session_auth__: Optional RPCAuthSessionKey or List[RPCAuthSessionKey]
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

            if session_auth__:
                if isinstance(session_auth__, RPCAuthSessionKey):
                    if f.__name__ not in self._funcs_session_auth_lookup:
                        self._funcs_session_auth_lookup[f.__name__] = [session_auth__]
                    else:
                        if (
                            session_auth__
                            not in self._funcs_session_auth_lookup[f.__name__]
                        ):
                            self._funcs_session_auth_lookup[f.__name__].append(
                                session_auth__
                            )

                elif isinstance(session_auth__, list):
                    for auth_session_key in session_auth__:
                        if isinstance(auth_session_key, RPCAuthSessionKey):
                            if f.__name__ not in self._funcs_session_auth_lookup:
                                self._funcs_session_auth_lookup[f.__name__] = [
                                    auth_session_key
                                ]
                            else:
                                if (
                                    auth_session_key
                                    not in self._funcs_session_auth_lookup[f.__name__]
                                ):
                                    self._funcs_session_auth_lookup[f.__name__].append(
                                        auth_session_key
                                    )

            if host_auth__:
                if f.__name__ not in self._funcs_host_auth_lookup:
                    self._funcs_host_auth_lookup[f.__name__] = host_auth__
                else:
                    if host_auth__ not in self._funcs_host_auth_lookup[f.__name__]:
                        self._funcs_host_auth_lookup[f.__name__] = (
                            self._funcs_host_auth_lookup[f.__name__] + host_auth__
                        )

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

        if not _json.get("weerpc") == 1.1:
            return RPCResponse.fail("Invalid weerpc version.")

        try:
            rpcm = RPCModel(**_json)
        except ValidationError:
            return RPCResponse.fail("Invalid request.")

        try:
            assert rpcm.function in self.LOOKUP
        except AssertionError:
            return RPCResponse.fail("Invalid function.")

        if self._funcs_session_auth_lookup.get(rpcm.function):
            for auth_session_key in self._funcs_session_auth_lookup[rpcm.function]:
                if not auth_session_key.check(session):
                    return RPCResponse.fail("Unauthorized.")

        if self._funcs_host_auth_lookup.get(rpcm.function):
            if request.host not in self._funcs_host_auth_lookup[rpcm.function]:
                return RPCResponse.fail(f"Unauthorized ({request.host})")

        if successful_response := self.LOOKUP[rpcm.function](rpcm.data):
            return successful_response

        return RPCResponse.fail("Unsuccessful command execution.")
