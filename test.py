from pprint import pprint

import click
import faker
import requests

from flask_rpc.latest import RPCRequest as Req


@click.group("run")
def run():
    pass


@run.command("create")
def create():
    f = faker.Faker()

    click.echo("Creating a client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients",
        json={
            "frpc": 1.0,  # Required
            "function": "create",
            "data": {"name": f.name()},
        },
    )
    pprint(response.json(), indent=2)


# Using the RCPRequest class to make a request to the server


@run.command("create-class")
def create_class():
    f = faker.Faker()

    click.echo("Creating a client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients",
        json=Req.build(function="create", data={"name": f.name()}),
    )
    pprint(response.json(), indent=2)


@run.command("read")
def read():
    click.echo("Reading client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients",
        json=Req.build(function="read", data={"client_id": 1}),
    )
    pprint(response.json(), indent=2)


@run.command("read-fail")
def read_fail():
    click.echo("Reading client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/read",
        json=Req.build(function="read", data={"client_id": 11111}),
    )
    pprint(response.json(), indent=2)


@run.command("update")
def update():
    click.echo("Updating client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/update",
        json=Req.build(function="update", data={"client_id": 1, "name": "John Doe"}),
    )
    pprint(response.json(), indent=2)


@run.command("delete")
def delete():
    click.echo("Deleting client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients",
        json=Req.build(function="delete", data={"client_id": 1}),
    )
    pprint(response.json(), indent=2)


@run.command("fail")
def fail():
    click.echo("Sending bad command...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients",
        json=Req.build(function="fail", data={"client_id": 1}),
    )
    pprint(response.json(), indent=2)


@run.command("t1")
def test1():
    click.echo("Running function...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/tester",
        json=Req.build(function="add_numbers", data=[1, 2, 3]),
    )
    pprint(response.json(), indent=2)


@run.command("t2")
def test2():
    click.echo("Running function...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/tester",
        json=Req.build(function="add_string", data="World"),
    )
    pprint(response.json(), indent=2)


if __name__ == "__main__":
    run()
