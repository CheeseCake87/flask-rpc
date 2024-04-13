from flask import Blueprint

from flask_rpc.latest import RPC
from .funcs import add_numbers, add_string

bp = Blueprint("tester", __name__, url_prefix="/tester")

rpc = RPC(bp)

rpc.functions(
    add_string=add_string,
)
rpc.functions_auto_name((add_numbers,))
