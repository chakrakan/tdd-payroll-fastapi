# payroll/app/models/pydantic.py

from pydantic.main import BaseModel
from typing import Union


class UploadResponseSchema(BaseModel):
    """
    UploadResponseSchema base model

    Args:
        BaseModel ([type]): [description]
    """

    file_id: int
    message: Union[str, dict]
