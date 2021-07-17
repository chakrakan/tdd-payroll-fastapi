# payroll/app/models/pydantic.py


from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.tortoise import TimeReport


# create pydantic models
time_report_pydantic = pydantic_model_creator(TimeReport, name="TimeReport")
