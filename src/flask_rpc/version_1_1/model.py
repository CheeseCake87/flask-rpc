import typing as t

from pydantic import BaseModel


class RPCModel(BaseModel):
    weerpc: float
    function: str
    data: t.Any
