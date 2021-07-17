# payroll/app/db.py


import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# configure Tortoise ORM to use aerich (db migration tool akin to Django ORM)
# https://tortoise-orm.readthedocs.io/en/latest/migration.html

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,  # we want aerich to handle this
        add_exception_handlers=True,
    )
