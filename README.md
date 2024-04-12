# 📣 Flask-RPC

Flask Remote Procedure Call (RPC) is a simple 
library that allows you to expose functions 
in your Flask application to be called 
remotely. It is designed to be straightforward 
to use and easy to understand.

Flask-RPC does not follow any current already existing
RPC standard, but uses its own standard, 
and primarily works with JSON over HTTP POST 
requests to call functions.

The typical request/response cycle is as follows:

**Request**

```json
{
    "frpc": 0.1,
    "function": "add_numbers",
    "data": [1, 2, 3]
}
```

**Response**

```json
{
  "frpc": 0.1,
  "ok": true,
  "message": "Function 'add_numbers' executed successfully",
  "data": 6
}
```

## Installation

```bash
pip install flask-rpc
```
