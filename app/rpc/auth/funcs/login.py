from flask import session

from flask_rpc.latest import RPCResponse


def login(params):
    session["user_id"] = 1
    return RPCResponse.successful_response(
        data={
            "user_id": 1,
        }
    )
