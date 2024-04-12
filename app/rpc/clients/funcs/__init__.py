from flask_rpc.latest import RPCResponse
from app.models.clients import Clients

"""
The functions below are fairly simple, and it's hard to see the value
in abstracting the logic into their own functions. However, the idea is
that as the application grows, these functions will become more complex,
and it will be easier to manage.

For example, the rpc.clients.funcs package should be the only place where
the logic for creating, reading, updating, and deleting clients should be
located.

It's also easier to test these functions in isolation without the need to
call a route.
"""


def create_client(params):
    status, message, result = Clients.create(**params)

    if not status:
        return RPCResponse.failed_response(message, params)

    return RPCResponse.successful_response(
        data={
            "client_id": result.client_id,
            "name": result.name,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )


def read_client(params):
    status, message, result = Clients.read(**params)

    if not status:
        return RPCResponse.failed_response(message, params)

    return RPCResponse.successful_response(
        data={
            "client_id": result.client_id,
            "name": result.name,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )


def update_client(params):
    status, message, result = Clients.update(**params)

    if not status:
        return RPCResponse.failed_response(message, params)

    return RPCResponse.successful_response(
        data={
            "client_id": result.client_id,
            "name": result.name,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )


def delete_client(params):
    status, message, result = Clients.delete(**params)

    if not status:
        return RPCResponse.failed_response(message, params)

    return RPCResponse.successful_response(
        {"client_id": result.client_id, "name": result.name}
    )
