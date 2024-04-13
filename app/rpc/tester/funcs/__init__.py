from flask_rpc.latest import RPCResponse as Res


# accept list return int
def add_numbers(data: list):
    return Res.success(data=sum(data), message="add_numbers")


# accept string return string
def add_string(data: str):
    return Res.success(data=f"Hello {data}!", message="add_string")
