# payroll/app/api/crud.py


# from app.models.pydantic import time_report_pydantic
from fastapi import UploadFile

# from app.models.tortoise import TimeReport


async def process_file(file: UploadFile) -> str:
    report_id = file.filename.split("-")[2]
    return report_id
