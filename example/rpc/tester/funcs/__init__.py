from flask_rpc.exceptions import DataException
from flask_rpc.latest import RPCResponse as Res
from flask_rpc.validation import DataList, DataStr


# accept list return int
def add_numbers(data: list):
    try:
        DataList(data)
    except DataException:
        return Res.fail("Invalid data type.", {"data": "list"})

    return Res.success(data=sum(data), message="add_numbers")


# accept string return string
def add_string(data: str):
    try:
        DataStr(data)
    except DataException:
        return Res.fail("Invalid data type.", {"data": "str"})

    return Res.success(data=f"Hello {data}!", message="add_string")
