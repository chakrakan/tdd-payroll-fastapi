# payroll/app/api/crud.py

from tempfile import SpooledTemporaryFile
from app.models.tortoise import TimeReport

# extendable file types and const naming convention

FILE_EXT = {"csv"}
NAMING_CONVENTION = r"time-report-\d+\..*"

ERRORS = {
    "DUPLICATE_REPORT": "Error: Duplicate report",
}


async def process_file(csv_file: SpooledTemporaryFile) -> int:
    """
    Main file processing handler

    Args:
        csv_file (SpooledTemporaryFile): [description]

    Returns:
        int: [description]
    """
    time_report = TimeReport()
    return time_report.id


async def generate_report_service() -> dict:
    """
    Report generator handler

    Returns:
        dict: [description]
    """
    # logic to generate report
    return
