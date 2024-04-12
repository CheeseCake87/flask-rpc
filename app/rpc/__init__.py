from flask import Blueprint


def load_nested_blueprints(bp):
    from .auth import auth
    from .clients import clients

    bp.register_blueprint(auth)
    bp.register_blueprint(clients)


rpc = Blueprint("rpc", __name__, url_prefix="/rpc")

load_nested_blueprints(rpc)
