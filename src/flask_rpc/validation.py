import typing as t

from .exceptions import DataException


class DataBool:
    _data: bool

    def __init__(self, data: bool):
        self.set(data)

    def set(self, data: bool):
        if isinstance(data, bool):
            self._data = data
        else:
            raise DataException("data is not of type bool")


class DataStr:
    _data: str

    def __init__(self, data: str):
        self.set(data)

    def set(self, data: str):
        if isinstance(data, str):
            self._data = data
        else:
            raise DataException("data is not of type str")


class DataInt:
    _data: int

    def __init__(self, data: int):
        self.set(data)

    def set(self, data: int):
        if isinstance(data, int):
            self._data = data
        else:
            raise DataException("data is not of type int")


class DataList:
    _data: list

    def __init__(self, data: list):
        self.set(data)

    def set(self, data: list):
        if isinstance(data, list):
            self._data = data
        else:
            raise DataException("data is not of type list")


class DataDict:
    _data: dict
    _protected_keys: t.Optional[t.List[str]]

    def __init__(self, data: dict):
        self.set(data)

    def set(self, data: dict):
        if isinstance(data, dict):
            self._data = data
        else:
            raise DataException("data is not of type dict")

    def get_ensure_key(self, key: str):
        if key not in self._data:
            raise DataException(f"{key} not in data")
        return self._data[key]

    def get(self, key: str, value_if_not_found: t.Any = None) -> t.Any:
        return self._data.get(key, value_if_not_found)

    def has_protected_field(
        self, values, protected_fields: t.Optional[t.List[str]] = None
    ):
        if not protected_fields:
            return False

        return any(k in values for k in protected_fields)

    @property
    def raw(self) -> dict:
        return self._data
