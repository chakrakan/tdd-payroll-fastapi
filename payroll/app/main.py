# payroll/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.api import ping

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]


def create_application() -> FastAPI:
    app = FastAPI(title="Wave Payroll")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,  # we want aerich to handle this
        add_exception_handlers=True,
    )

    app.include_router(ping.router)

    return app


app = create_application()
