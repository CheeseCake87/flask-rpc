import typing as t


class RPCAuthSessionKey:
    _key: str
    _value_in: t.List[t.Any]

    def __init__(self, key: str, value_in: t.List[t.Any]):
        self._key = key
        self._value_in = value_in

    def check(self, ask: t.Any):
        if self._key not in ask:
            return False

        if ask.get(self._key) in self._value_in:
            return True

        return False
