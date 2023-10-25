import uuid
from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Query
from pydantic import UUID4

from models import Route

app = FastAPI()

routes: list[Route] = []


@app.get("/routes", response_model=list[Route], status_code=status.HTTP_200_OK)
def read_routes(limit: Annotated[int | None, Query(ge=0)] = None):
    if limit is not None:
        return routes[:limit]
    return routes


@app.post("/routes", response_model=Route, status_code=status.HTTP_201_CREATED)
def create_route(route: Route):
    if route.id is not None:
        raise HTTPException(status_code=432, detail="Route not found")

    route.id = uuid.uuid4()
    routes.append(route)

    return route


@app.get("/routes/{route_id}", response_model=Route, status_code=status.HTTP_200_OK)
def read_route(route_id: UUID4):
    for route in routes:
        if route.id == route_id:
            return route
    raise HTTPException(status_code=404, detail="Route not found")
