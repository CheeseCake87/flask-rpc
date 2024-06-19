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

        Version 1.1.

        :param function: Str
        :param data: Any (JSON serializable)
        :return:
        """
        return {"weerpc": 1.1, "function": function, "data": data}
