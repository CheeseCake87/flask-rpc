import typing as t

from pydantic import BaseModel


class RPCModel(BaseModel):
    wrpc: float
    function: str
    data: t.Any
