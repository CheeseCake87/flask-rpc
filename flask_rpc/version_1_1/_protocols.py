import typing as t


@t.runtime_checkable
class RPCAuthSessionKey(t.Protocol):
    _key: str
    _value_in: t.List[t.Any]

    def check(self, ask: t.Any): ...
