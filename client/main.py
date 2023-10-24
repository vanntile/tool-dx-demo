from enum import Enum
from typing_extensions import Annotated
from uuid import UUID

import requests
import typer
from rich import print


class Action(str, Enum):
    ACCEPT_SRC = "ACCEPT_SRC"
    ACCEPT_DST = "ACCEPT_DST"
    BLOCK_SRC = "BLOCK_SRC"
    BLOCK_DST = "BLOCK_DST"
    FORWARD = "FORWARD"


class Protocol(str, Enum):
    tcp = "tcp"
    udp = "udp"
    icmp = "icmp"


state = {"address": None}

app = typer.Typer(help="CLI tool for configuring routers.")


@app.callback()
def main(address: Annotated[str, typer.Option(envvar="ADDRESS", help="Router address")] = None):
    if address is None:
        address = typer.prompt("Provide address of the router to configure")
    print(f"Will configure router at: {address}")
    state["address"] = address


@app.command()
def read(limit: Annotated[int, typer.Option(min=0)] = 1000):
    """
    Read existing configuration
    """
    try:
        res = requests.get(f"{state['address']}/routes?limit={limit}")
        data = res.json()
        print("[blue]Succesful request[/blue]")
        print(data)
    except requests.exceptions.Timeout:
        print("[red]Request timed out[/red]")
    except requests.exceptions.RequestException as e:
        print(f"[red]Request failed:[/red] {e}")


@app.command()
def create(
    action: Annotated[Action, typer.Option(case_sensitive=False)],
    protocol: Annotated[Protocol, typer.Option(case_sensitive=False)] = None,
):
    """
    Create a new route.

    --action is required to determine necessary fields.
    --protocol is optional
    """
    print(f"Action {action.value} {protocol.value if protocol else 0}")

    body = {"action": action.value}
    match action:
        case Action.ACCEPT_SRC | Action.BLOCK_SRC:
            body["source"] = typer.prompt("IP network address (CIDR format)")
            if typer.confirm("Use custom port?"):
                body["source_port"] = typer.prompt(text="Port value", type=int)
        case Action.ACCEPT_DST | Action.BLOCK_DST:
            body["destination"] = typer.prompt("IP network address (CIDR format)")
            if typer.confirm("Use custom port?"):
                body["destination_port"] = typer.prompt(text="Port value", type=int)
        case Action.FORWARD:
            body["source"] = typer.prompt("Source IP network address (CIDR format)")
            if typer.confirm("Use custom source port?"):
                body["source_port"] = typer.prompt(text="Port value", type=int)
            body["destination"] = typer.prompt("Destination IP network address (CIDR format)")
            if typer.confirm("Use custom destination port?"):
                body["destination_port"] = typer.prompt(text="Port value", type=int)

    # Confirm operations
    print(f"Will send the following route:")
    print(body)
    typer.confirm("Send route?", abort=True)

    try:
        res = requests.post(f"{state['address']}/routes", json=body)
        data = res.json()
        print("[blue]Succesful request[/blue]")
        print(data)
    except requests.exceptions.Timeout:
        print("[red]Request timed out[/red]")
    except requests.exceptions.RequestException as e:
        print(f"[red]Request failed:[/red] {e}")


@app.command()
def get(id: UUID):
    """
    Get a single route by --id
    """
    try:
        res = requests.get(f"{state['address']}/routes/{id}")
        data = res.json()
        print("[blue]Succesful request[/blue]")
        print(data)
    except requests.exceptions.Timeout:
        print("[red]Request timed out[/red]")
    except requests.exceptions.RequestException as e:
        print(f"[red]Request failed:[/red] {e}")


if __name__ == "__main__":
    app()
