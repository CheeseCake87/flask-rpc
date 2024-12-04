from flask_rpc.latest import RPCResponse


# _ is used to show that the function does not use the request object
def logout(_):
    return RPCResponse.success(
        data={
            "user_id": 1,
        }
    )
