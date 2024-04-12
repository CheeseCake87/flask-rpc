from flask_rpc.latest import RPCResponse


def logout(params):
    return RPCResponse.successful_response(
        data={
            "user_id": 1,
        }
    )
