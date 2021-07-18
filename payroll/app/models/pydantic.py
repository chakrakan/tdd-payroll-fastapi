# payroll/app/models/pydantic.py


from pydantic.main import BaseModel

# from tortoise.contrib.pydantic import pydantic_model_creator

# from app.models.tortoise import Employee, JobGroup
from typing import Union


class UploadResponseSchema(BaseModel):
    """
    UploadResponseSchema base model

    Args:
        BaseModel ([type]): [description]
    """

    file_id: int
    message: Union[str, dict]


# create pydantic schemas with tortoise ORM helper
# EmployeeSchema = pydantic_model_creator(Employee, name="Employee")
# JobGroupSchema = pydantic_model_creator(JobGroup, name="JobGroup")
