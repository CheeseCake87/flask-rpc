# 📣 Flask-RPC

```bash
pip install flask-rpc
```

---

> 🚨Seeking contributions to bring more RPC protocols to Flask-RPC.

Flask - Remote Procedure Call (RPC) is a simple
library that allows you to expose functions
in your Flask application to be called
remotely. It is designed to be straightforward
to use and easy to understand.

Flask-RPC currently only uses the [weeRPC](https://github.com/CheeseCake87/weeRPC)
as its protocol, which is a micro JSON-based protocol that allows for
easy communication between the client and server.

This extension is designed to stay slim and provides
methods for generating requests and responses.

It does not enforce or validate the data passed in, or the
data being sent back; this is left to you to implement
in whatever way you feel comfortable (or not at all, if there's
no need for it)

Flask-RPC does validate the version of weeRPC on an incoming request. This
is to ensure that the request is structured in a way that the version
of RPC you are using expects.

Other than that, you are free to use whatever data validation
you feel comfortable with. Pydantic and Marshmallow are good choices.

The typical request/response cycle of weeRPC is as follows:

**Request**

```json
{
  "wrpc": 1.0,
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
  "wrpc": 1.0,
  "ok": true,
  "message": "Function 'add_numbers' executed successfully",
  "data": 6
}
```

## Usage

[This repo](https://github.com/CheeseCake87/flask-rpc) contains a working example of Flask-RPC.

It also includes an example of using the [JS library](https://github.com/CheeseCake87/wrpc-js) that helps
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

or, if you're using the [JS library](https://github.com/CheeseCake87/wrpc-js):

```js
fetch("/rpc", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: wrpc(
        function_ = "add_numbers",
        data = [1, 2, 3]
    )
})
```

Will return:

```json
{
  "wrpc": 1.0,
  "ok": true,
  "message": "Function 'add_numbers' executed successfully",
  "data": 6
}
```

## Security

You can lock down RPC routes by using sessions and or host checking.

### Session Auth

`from flask_rpc.latest import RPCAuthSessionKey`

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
