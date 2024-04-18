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

        Version 1.0.

        :param message: Str
        :param data: Any (JSON serializable)
        :return:
        """
        r = {"frpc": 1.0, "ok": False}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

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

        Version 1.0.

        :param data: Any (JSON serializable)
        :param message: Str
        :return:
        """
        r = {"frpc": 1.0, "ok": True}

        if message:
            r["message"] = message
        if data:
            r["data"] = data

        return r
