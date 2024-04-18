import typing as t


class RPCRequest:
    @classmethod
    def build(
        cls,
        function: str,
        data: t.Union[
            str, int, float, bool, t.List[t.Any], t.Dict[str, t.Any], None
        ] = None,
    ) -> t.Dict[str, t.Any]:
        """
        Build a request.

        Version 1.0.

        :param function: Str
        :param data: Any (JSON serializable)
        :return:
        """
        return {"wrpc": 1.0, "function": function, "data": data}
