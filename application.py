import uvicorn
from fastapi import FastAPI

from di.container import Container
from src.entrypoints import streamAPI


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[streamAPI])

    app = FastAPI()
    app.container = container
    app.include_router(streamAPI.router)
    return app


app = create_app()
