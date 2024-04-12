from flask import session

from flask_rpc.latest import RPCResponse


def get_session(params):
    return RPCResponse.successful_response(data={**session})
