import click
import faker
import requests


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
            "data": {
                "name": f.name()
            }
        }
    )
    click.echo(response.text)


@run.command("read")
def create():
    click.echo("Reading client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/read",
        json={
            "frpc": 1.0,  # Required
            "function": "read",
            "data": {
                "client_id": 1
            }
        }
    )
    click.echo(response.text)


@run.command("read-fail")
def create():
    click.echo("Reading client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/read",
        json={
            "frpc": 1.0,  # Required
            "function": "read",
            "data": {
                "client_id": 1111
            }
        }
    )
    click.echo(response.text)


@run.command("update")
def create():
    click.echo("Updating client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/update",
        json={
            "frpc": 1.0,  # Required
            "function": "update",
            "data": {
                "client_id": 1,
                "name": "Jane Doe"
            }
        }
    )
    click.echo(response.text)


@run.command("delete")
def create():
    click.echo("Deleting client...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/delete",
        json={
            "frpc": 1.0,  # Required
            "function": "delete",
            "data": {
                "client_id": 1
            }
        }
    )
    click.echo(response.text)


@run.command("fail")
def create():
    click.echo("Sending bad command...")
    response = requests.post(
        "http://127.0.0.1:5000/rpc/clients/fail",
        json={
            "frpc": 1.0,  # Required
            "function": "fail",
            "data": {
                "client_id": 1
            }
        }
    )
    click.echo(response.text)


if __name__ == '__main__':
    run()
