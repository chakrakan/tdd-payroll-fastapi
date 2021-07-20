# payroll/app/models/tortoise.py

from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class JobGroup(TimestampMixin, Model):
    """
    JobGroup model for the DB

    Args:
        Model ([Model]): [description]
    """

    group = fields.CharField(max_length=1, null=False, pk=True)
    hourly_rate = fields.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Group {self.group}, Hourly Rate: ${self.hourly_rate:.2f}"

    class Meta:
        table = "job_group"
        unique_together = ("group", "hourly_rate")


class TimeReport(TimestampMixin, Model):
    """
    Time Report class to contain parsed CSV info... pretty much a data dump

    Args:
        Model ([type]): [description]
    """

    report_id = fields.IntField(null=False)
    date = fields.DatetimeField(null=False)
    hours_worked = fields.DecimalField(max_digits=4, decimal_places=2, null=False)
    employee = fields.ForeignKeyField("models.Employee", related_name="employee_ids")
    job_group = fields.ForeignKeyField("models.JobGroup", related_name="job_groups")

    def __str__(self):
        return (
            f"Report ID: {self.report_id}\n"
            f"Date: {self.date} Hours Worked: {self.hours_worked}\n"
            f"Employee ID: {self.employee} Job Group: {self.job_group}"
        )

    class Meta:
        table = "time_report"
        ordering = ["date"]


class Employee(TimestampMixin, Model):
    """
    An extensible class to manage Employees in the DB

    Args:
        Model ([Model]): [Base model class from the ORM]
    """

    id = fields.IntField(pk=True)
    job_group = fields.ForeignKeyField("models.JobGroup", related_name="job_group")

    def __str__(self):
        return f"Employee ID: {self.id}, Job Group: {self.job_group}"

    class Meta:
        table = "employee"


class EmployeeReport(TimestampMixin, Model):
    """
    More Specific EmployeeReport class to generate report structure from

    Args:
        Model ([type]): [description]
    """

    report_employee = fields.ForeignKeyField(
        "models.Employee",
        related_name="employee_reports",
    )
    start_date = fields.DatetimeField(null=False)
    end_date = fields.DatetimeField(null=False)
    amount_paid = fields.DecimalField(max_digits=14, decimal_places=2, null=False)

    def __str__(self):
        return (
            f"Report:\n"
            f"Start/End Date: {self.start_date}/{self.end_date}\n"
            f"Employee ID: {self.report_employee.pk} "
            f"Amount Paid: ${self.amount_paid:.2f}"
        )

    class Meta:
        table = "employee_report"
        ordering = ["start_date"]
