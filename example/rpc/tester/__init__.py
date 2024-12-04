from flask import Blueprint

from flask_rpc.latest import RPC, RPCAuthSessionKey
from .funcs import add_numbers, add_string

bp = Blueprint("tester", __name__, url_prefix="/tester")

rpc = RPC(bp)

rpc.functions(
    add_string=add_string,
)
rpc.functions_auto_name((add_numbers,))

rpc.functions(
    session_auth__=RPCAuthSessionKey("logged_in", [True]),
    add_string_auth_session=add_string,
)

rpc.functions(host_auth__=["127.0.0.1:5000"], add_string_auth_host=add_string)
