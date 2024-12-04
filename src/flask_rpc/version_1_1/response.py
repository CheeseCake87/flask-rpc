import typing as t


class RPCResponse:
    @classmethod
    def fail(
        cls,
        message: str = None,
        data: t.Union[
            str, int, float, bool, t.List[t.Any], t.Dict[str, t.Any], None
        ] = None,
    ):
        """
        Return a failed response.

        Version 1.1.

        :param message: Str
        :param data: Any (JSON serializable)
        :return:
        """
        r = {
            "weerpc": 1.0,
            "ok": False,
            "message": message if message else None,
            "data": data if data else None,
        }

        return r

    @classmethod
    def success(
        cls,
        data: t.Union[
            str, int, float, bool, t.List[t.Any], t.Dict[str, t.Any], None
        ] = None,
        message: str = None,
    ):
        """
        Return a successful response.

        Version 1.1.

        :param data: Any (JSON serializable)
        :param message: Str
        :return:
        """
        r = {
            "weerpc": 1.0,
            "ok": True,
            "message": message if message else None,
            "data": data if data else None,
        }

        return r
