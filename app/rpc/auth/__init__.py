from flask import Blueprint

from flask_rpc.latest import RPC
from .funcs.login import login
from .funcs.logout import logout
from .funcs.session import get_session

auth = Blueprint("auth", __name__, url_prefix="/auth")

rpc = RPC(auth)

rpc.functions(login=login, logout=logout, session=get_session)
