# payroll/app/models/pydantic.py


from pydantic.main import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.tortoise import Employee, JobGroup


# create pydantic schemas with tortoise ORM helper


class UploadResponseSchema(BaseModel):
    file_id: int
    message: str


EmployeeSchema = pydantic_model_creator(Employee, name="Employee")
JobGroupSchema = pydantic_model_creator(JobGroup, name="JobGroup")
