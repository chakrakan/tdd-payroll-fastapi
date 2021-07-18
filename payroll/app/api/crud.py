# payroll/app/api/crud.py

from tempfile import SpooledTemporaryFile
from app.models.tortoise import TimeReport

FILE_EXT = {"csv"}
NAMING_CONVENTION = r"time-report-\d+\..*"

ERRORS = {
    "DUPLICATE_REPORT": "Error: Duplicate report",
}


async def process_file(csv_file: SpooledTemporaryFile) -> int:
    time_report = TimeReport()
    return time_report.id


async def generate_report_service() -> dict:
    # logic to generate report
    return
