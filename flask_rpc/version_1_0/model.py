import typing as t

from pydantic import BaseModel


class RPCModel(BaseModel):
    frpc: float
    function: str
    data: t.Any
