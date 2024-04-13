from flask import Blueprint

from flask_rpc.latest import RPC
from .funcs import *

bp = Blueprint("tester", __name__, url_prefix="/tester")

rpc = RPC(bp)

rpc.functions(add_numbers=add_numbers)
