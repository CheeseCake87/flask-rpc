from flask_rpc.latest import RPCResponse


# _ is used to show that the function does not use the request object
def logout(_):
    return RPCResponse.successful_response(
        data={
            "user_id": 1,
        }
    )
