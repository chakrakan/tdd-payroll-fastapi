# payroll/app/models/tortoise.py

from tortoise.models import Model
from tortoise import fields


class JobGroup(Model):
    """JobGroup model which holds the unique char for the group and the hourly_rate
    e.g. group A, hourly_rate 20

    Args:
        Model ([Model]): [Base model class from the ORM]
    """

    group = fields.CharField(pk=True, max_length=1)
    hourly_rate = fields.IntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group} - ${self.hourly_rate}/hr"


class Employee(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
