from flask import Blueprint

from flask_rpc.latest import RPC
from flask_rpc.version_1_0 import RPCAuthSessionKey
from .funcs.login import login
from .funcs.logout import logout
from .funcs.session import get_session

auth = Blueprint("auth", __name__, url_prefix="/auth")

login_rpc = RPC(auth, url_prefix="/login")
login_rpc.functions(login=login)

authenticated_rpc = RPC(auth)
authenticated_rpc.functions(logout=logout, session=get_session)
authenticated_rpc.session_auth(RPCAuthSessionKey("logged_in", [True]))
