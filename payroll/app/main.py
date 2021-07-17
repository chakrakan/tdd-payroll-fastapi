# payroll/app/main.py

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health_check, upload
from app.db import init_db

log = logging.getLogger("uvicorn")

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

    app.include_router(health_check.router)
    app.include_router(upload.router)

    return app


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("🚀 Starting up and initializing DB...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("⏳ Shutting down...")
