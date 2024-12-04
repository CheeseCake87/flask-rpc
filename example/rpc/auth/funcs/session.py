from flask import session

from flask_rpc.latest import RPCResponse


# _ is used to show that the function does not use the request object
def get_session(_):
    return RPCResponse.success(data={**session})
