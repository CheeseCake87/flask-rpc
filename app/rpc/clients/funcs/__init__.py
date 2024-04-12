from app.models.clients import Clients
from flask_rpc.latest import RPCResponse


def create_client(data):
    status, message, result = Clients.create(**data)

    if not status:
        return RPCResponse.failed_response(message, data)

    return RPCResponse.successful_response(
        data={
            "client_id": result.client_id,
            "name": result.name,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )


def read_client(data):
    status, message, result = Clients.read(**data)

    if not status:
        return RPCResponse.failed_response(message, data)

    return RPCResponse.successful_response(
        data={
            "client_id": result.client_id,
            "name": result.name,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )


def update_client(data):
    status, message, result = Clients.update(**data)

    if not status:
        return RPCResponse.failed_response(message, data)

    return RPCResponse.successful_response(
        data={
            "client_id": result.client_id,
            "name": result.name,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )


def delete_client(data):
    status, message, result = Clients.delete(**data)

    if not status:
        return RPCResponse.failed_response(message, data)

    return RPCResponse.successful_response(
        {"client_id": result.client_id, "name": result.name}
    )
