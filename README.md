# 📣 Flask-RPC

```bash
pip install flask-rpc
```

---

Flask - Remote Procedure Call (RPC) is a simple
library that allows you to expose functions
in your Flask application to be called
remotely. It is designed to be straightforward
to use and easy to understand.

Flask-RPC does not follow any current already existing
RPC standard, but uses its own standard,
and primarily works with JSON over HTTP POST
requests to call functions.

This extension is designed to stay slim and provides
methods for generating requests and request responses.

It does not enforce or validate the data passed in, or the
data being sent back; this is left to the user to implement
in whatever way they feel comfortable (or not at all, if there's
no need for it)

Flask-RPC does validate the request coming in using
Pydantic.

This is to ensure that the request is structured
in the way to whatever version of Flask-RPC you are using.

Other than that, the user is free to use whatever data validation
they feel comfortable with. Pydantic and Marshmallow are good choices.

The typical request/response cycle is as follows:

**Request**

```json
{
  "frpc": 1.0,
  "function": "add_numbers",
  "data": [
    1,
    2,
    3
  ]
}
```

**Response**

```json
{
  "frpc": 1.0,
  "ok": true,
  "message": "Function 'add_numbers' executed successfully",
  "data": 6
}
```

## Usage

[This repo](https://github.com/CheeseCake87/flask-rpc) contains a working example of Flask-RPC.

It also includes an example of using the [JS library](https://github.com/CheeseCake87/flask-rpc-js) that helps
in making requests via fetch to Flask-RPC.

### Simplest example

```python
from flask import Flask

from flask_rpc.latest import RPC, RPCResponse


def add_numbers(data):
    if isinstance(data, list):
        return RPCResponse.success(
            sum(data),
            "Function 'add_numbers' executed successfully"
        )


app = Flask(__name__)
rpc = RPC(app, url_prefix="/rpc")  # or RPC(blueprint)
rpc.functions(
    add_numbers=add_numbers
)
```

or

```python
...
RPC(
    app,
    url_prefix="/rpc",
    functions={
        "add_numbers": add_numbers
    }
)
...
```

`RPC(...)`

Will register a POST route with the app or blueprint that you pass in.

`rpc.functions(...)`

Will register the functions that you pass in to be called remotely.
The argument names used will be the name of the function you will call remotely, for example:

```python
rpc.functions(
    add_numbers=add_numbers,
    subtract=subtract_numbers
)
```

Calling `subtract` remotely will call the `subtract_numbers` function.

A request to the `/rpc` endpoint with the following JSON payload:

```python
import requests
from flask_rpc import RPCRequest

response = requests.post(
    "http://localhost:5000/rpc",
    json=RPCRequest.build(
        function="add_numbers",
        data=[1, 2, 3]
    )
)
```

or, if you're using the [JS library](https://github.com/CheeseCake87/flask-rpc-js):

```js
fetch("/rpc", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: frpc(
        function_ = "add_numbers",
        data = [1, 2, 3]
    )
})
```

Will return:

```json
{
  "frpc": 1.0,
  "ok": true,
  "message": "Function 'add_numbers' executed successfully",
  "data": 6
}
```

## Security

You can lock down using RPC routes by using sessions and or host checking.

### Session Auth

`from quart_rpc.latest import RPCAuthSessionKey`

```python
...
RPC(
    app,  # or RPC(blueprint, ...)
    url_prefix="/rpc",
    session_auth=RPCAuthSessionKey("logged_in", [True]),
    functions={
        "add_numbers": add_numbers
    }
)
...
```

or a list of RPCAuthSessionKey:

```python
...
RPC(
    app,  # or RPC(blueprint, ...)
    url_prefix="/rpc",
    session_auth=[
        RPCAuthSessionKey("logged_in", [True]),
        RPCAuthSessionKey("user_type", ["admin"])
    ],
    functions={
        "add_numbers": add_numbers
    }
)
...
```

### Host Auth

In the following example, only requests from `127.0.0.1:5000` will be accepted.

```python
...
RPC(
    app,  # or RPC(blueprint, ...)
    url_prefix="/rpc",
    host_auth=["127.0.0.1:5000"],
    functions={
        "add_numbers": add_numbers
    }
)
...
```