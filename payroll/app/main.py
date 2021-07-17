# payroll/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

    app.include_router(ping.router)

    return app


app = create_application()
