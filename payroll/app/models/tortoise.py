# payroll/app/models/tortoise.py

from tortoise.models import Model
from tortoise import fields


class JobGroup(Model):
    """
    JobGroup model for the DB

    Args:
        Model ([Model]): [description]
    """

    group = fields.CharField(max_length=1, pk=True)
    hourly_rate = fields.DecimalField(max_digits=8, decimal_places=2, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Group {self.group}, Hourly Rate: ${self.hourly_rate:.2f}"

    class Meta:
        table = "job_group"


class TimeReport(Model):
    """
    Time Report class to contain parsed CSV info

    Args:
        Model ([type]): [description]
    """

    id = fields.IntField(pk=True)
    date = fields.DateField(null=False)
    hours_worked = fields.DecimalField(max_digits=4, decimal_places=2, null=False)
    employee_id = fields.ForeignKeyField(
        "models.Employee", related_name="employee_reports"
    )
    job_group = fields.ForeignKeyField("models.JobGroup", related_name="group_reports")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Report ID: {self.id}\n"
            f"Date: {self.date} Hours Worked: {self.hours_worked}\n"
            f"Employee ID: {self.employee_id} Job Group: {self.job_group}"
        )

    class Meta:
        table = "time_report"


class Employee(Model):
    """
    An extensible class to manage Employees in the DB

    Args:
        Model ([Model]): [Base model class from the ORM]
    """

    id = fields.IntField(pk=True)
    job_group = fields.ForeignKeyField("models.JobGroup", related_name="job_group")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Employee ID: {self.id}"

    class Meta:
        table = "employee"
