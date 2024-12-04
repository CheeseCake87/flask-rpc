def snake_case(v: str) -> str:
    sc = [
        "-",
        ".",
        " ",
        ":",
        ";",
        "!",
        "?",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "<",
        ">",
        "=",
        "+",
        "*",
        "/",
        "\\",
    ]
    return (
        "".join([x if x not in sc else "_" for x in v.lower()])
        .replace("__", "_")
        .replace("_", "", 1)
    )


if __name__ == "__main__":
    print(
        snake_case("/url/with/slashes-and-dashes"),
    )
