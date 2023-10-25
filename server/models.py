from enum import Enum

from pydantic import UUID4, BaseModel, Field, model_validator
from pydantic.networks import IPvAnyNetwork
from typing_extensions import Annotated

Port = Annotated[int, Field(ge=0, le=65535)]


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


class Route(BaseModel):
    id: UUID4 | None = None
    source: IPvAnyNetwork | None = None
    source_port: Port | None = None
    destination: IPvAnyNetwork | None = None
    destination_port: Port | None = None
    protocol: Protocol | None = None
    action: Action

    @model_validator(mode="after")
    def check_source_specified(self) -> "Route":
        match self.action:
            case Action.ACCEPT_SRC | Action.BLOCK_SRC if self.source is None:
                raise ValueError("source cannot be null for a SRC action")
            case Action.ACCEPT_DST | Action.BLOCK_DST if self.destination is None:
                raise ValueError("destination cannot be null for a DST action")
            case Action.FORWARD if self.source is None or self.destination is None:
                raise ValueError("both source and destination must be present for FORWARD actions")
        return self
