from flask import Blueprint

from flask_rpc.latest import RPC
from .funcs import create_client, read_client, update_client, delete_client

clients = Blueprint("clients", __name__, url_prefix="/clients")

rpc = RPC(clients)

rpc.functions(
    create=create_client,
    read=read_client,
    update=update_client,
    delete=delete_client,
)
