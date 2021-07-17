# payroll/app/db.py


import os

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
