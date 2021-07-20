# payroll/app/models/pydantic.py

from typing import Union

from pydantic.main import BaseModel


class UploadResponseSchema(BaseModel):
    """
    UploadResponseSchema base model

    Args:
        BaseModel ([type]): [description]
    """

    file_id: int
    message: Union[str, dict]
