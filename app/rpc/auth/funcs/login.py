from flask import session

from flask_rpc.latest import RPCResponse


# _ is used to show that the function does not use the request object
def login(_):
    session["user_id"] = 100
    return RPCResponse.success(
        data={
            "user_id": 100,
        }
    )
