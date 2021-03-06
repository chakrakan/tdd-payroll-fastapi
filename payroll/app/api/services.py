# payroll/app/api/crud.py

import calendar
import re
from datetime import datetime
from decimal import Decimal
from os.path import splitext
from typing import List, Optional, Tuple

from fastapi.datastructures import UploadFile
from tortoise.functions import Sum

from app.models.tortoise import Employee, EmployeeReport, JobGroup, TimeReport

# extendable file types and const naming convention

FILE_EXT = {".csv"}
NAMING_CONVENTION = re.compile("time-report-\\d+$")
MAX_WORK_HR_PER_EMP = 12


async def process_file(uploaded_file: UploadFile, file_id: int):
    """
    Main file processing handler.
    O(3N) -> O(N) runtime based on size of file.
    Bulk creates DB items.
    Reads a SpooledTemporaryFile which automatically gets written to
    tmp/ if a size is specified or if fileno() is triggered.
    Also, this function is passed into FastAPIs BackgroundTasks which will
    parallelize processing across specified number of workers (4)

    Args:
        csv_file (SpooledTemporaryFile): [description]

    Returns:
        int: [description]
    """

    try:
        # file decode
        csv_byte_literal = await uploaded_file.read()
        data = csv_byte_literal.decode("utf-8").splitlines()

        # consts and holders
        time_reports = []
        employee_reports = []
        start_day = 1
        end_day = 15

        if len(data) > 1:

            # create data in DB + map them up in O(N) time where
            # N is number of CSV rows

            for line in data[1:]:
                data_row = line.split(",")
                formatted_date = await parse_date(data_row[0].strip())
                month_range = calendar.monthrange(
                    formatted_date.year, formatted_date.month
                )[1]

                start_day = start_day if formatted_date.day <= 15 else 16
                end_day = end_day if formatted_date.day <= 15 else month_range

                formatted_start_date = datetime(
                    formatted_date.year, formatted_date.month, start_day
                )
                formatted_end_date = datetime(
                    formatted_date.year, formatted_date.month, end_day
                )

                formatted_hrs = Decimal(data_row[1].strip())

                # get or create a job_group or employee dynamically
                db_job = await get_job_group(data_row[3].strip())
                db_employee = await get_employee(int(data_row[2].strip()), db_job.pk)

                time_reports.append(
                    TimeReport(
                        report_id=file_id,
                        date=formatted_date,
                        hours_worked=formatted_hrs,
                        employee_id=db_employee.pk,
                        job_group_id=db_job.pk,
                    )
                )

                amount_to_pay = formatted_hrs * db_job.hourly_rate

                employee_reports.append(
                    EmployeeReport(
                        report_employee_id=db_employee.pk,
                        start_date=formatted_start_date,
                        end_date=formatted_end_date,
                        amount_paid=amount_to_pay,
                    )
                )

            # upload/commit and bulk create all time_reports
            await TimeReport.bulk_create(time_reports)
            await EmployeeReport.bulk_create(employee_reports)
            await uploaded_file.close()  # close file after DB data dump

            print(f"Processing {uploaded_file.filename} complete!")
        else:
            print(f"{uploaded_file.filename} has 0 data rows. Abort processing")

    except Exception as e:
        print(f"Error in proces_file: {e}")


async def get_employee_report(emp_id: int) -> List:
    """
    Performs a Sum aggregate on `amount_paid` followed by
    group-by/order-by operation to get values processed from PgSQL.
    Search with filter is O(logn) worst case.

    Args:
        emp_id (int): [emp id]

    Returns:
        List: [List of Employee report data for emp_id]
    """
    employee_reports = (
        await EmployeeReport.annotate(sum=Sum("amount_paid"))
        .filter(report_employee_id=emp_id)
        .group_by("report_employee_id", "start_date", "end_date")
        .order_by("start_date")
        .values_list("report_employee_id", "start_date", "end_date", "sum")
    )

    return employee_reports


async def check_work_hrs(emp_id: int) -> Optional[list]:
    """
    Extra function does a Sum on `hours_worked` to check
    edge case where two files with different IDs may contain the SAME
    values resulting in a particular employee's hours worked to be unrealistic
    (over 24 etc.)

    I've set a hard limit for 12 hrs/day for an employee that is tested during
    report generation based on the sample `time-report-42.csv` file which has
    a max value of 12 for hours work in a single day.


    Args:
        emp_id (int): [employee id]

    Returns:
        Optional[list]: [contains the tuple of requested data]
    """
    try:
        over_worked_data = (
            await TimeReport.annotate(total_hours_per_day=Sum("hours_worked"))
            .group_by("employee_id", "date")
            .filter(employee_id=emp_id, total_hours_per_day__gt=12)
            .first()
            .values_list("employee_id", "date", "total_hours_per_day")
        )

        if type(over_worked_data) == list and len(over_worked_data) > 0:
            return over_worked_data[0]

    except Exception as e:
        print(f"Error in check_work_hrs: {e}")


async def parse_date(date_string: str):
    """`time-report-42.csv` contains dates as `dd/mm/YYYY` however,
    in the next example in the docs, another example is given with
    `YYYY-mm-dd` format. Hence, a slight helper function to check
    the correct format and map for proper datetime generation.

    Args:
        date_string (str): [date]

    Raises:
        ValueError: [description]
    """
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    raise ValueError("Error: no valid date format found")


async def generate_report_service() -> Tuple:
    """
    Report generator handler, can be extended in the future
    if the GET request supports time_periods to limit querying entire DB

    O(N+M), worst case O(max(N,M)) or reduced to O(N)

    Returns:
        tuple: [contains the report if successfully generated as the first arg,
        and errors encountered during processing in the 2nd]
    """
    ERRORS = {}
    REPORT = {"payrollReport": {"employeeReports": []}}

    try:
        # check if there are any values in our table
        total_employees = await Employee.all()
        num_employees = len(total_employees)
        print(f"DB has {num_employees} employees, gathering reports, please wait...")
        if num_employees > 0:
            employee_reports = []

            # O(N+M) where N is number of employees, M reports
            for employee in total_employees:
                # get report and store
                employee_reports.extend(await get_employee_report(employee.pk))
                report_hrs = await check_work_hrs(employee.pk)
                if report_hrs is not None:
                    ERRORS["INVALID_DATA"] = (
                        f"Error: Employee {report_hrs[0]} is overworked. "
                        f"A single Employee can work a maximum of 12 hrs/day. "
                    )
                    break

            # iterate over reports and create json obj only if valid work hrs
            if len(ERRORS) == 0 and len(employee_reports) > 0:
                # O(M)
                for report in employee_reports:
                    report_obj = {
                        "employeeId": str(report[0]),
                        "payPeriod": {
                            "startDate": report[1].strftime("%Y-%m-%d"),
                            "endDate": report[2].strftime("%Y-%m-%d"),
                        },
                        "amountPaid": f"${report[3]:.2f}",
                    }
                    # append to main JSON response
                    REPORT["payrollReport"]["employeeReports"].append(report_obj)

                print("Report Generated!")
        else:
            ERRORS["NO_DATA"] = (
                "Error: There is no data in the database. "
                "Please make sure you upload a time report first via "
                "the APIs `/v1/upload` endpoint!"
            )
    except Exception as e:
        print(f"Error generating generate_report_service: {e}")
        ERRORS["INTERNAL_ERROR"] = "Error: Internal server error!"

    return (REPORT, ERRORS)


async def get_job_group(group_name: str) -> JobGroup:
    """Get or create a job group in the DB from CSV

    Args:
        group_name (str): [job group char]
    """
    try:
        JOB_GROUPS = {"A": 20.00, "B": 30.00}
        created_group = (
            group_name in JOB_GROUPS.keys()
            and await JobGroup.get_or_create(
                group=group_name, hourly_rate=Decimal(JOB_GROUPS[group_name])
            )
        )
        return created_group[0]
    except Exception as e:
        print(f"Error in get_job_group: {e}")


async def get_employee(employee_id: int, job_group: str) -> Employee:
    """Get or create employee in DB from CSV

    Args:
        employee_id (int): [employee id]
    """
    try:
        created_employee = await Employee.get_or_create(
            id=employee_id, job_group_id=job_group
        )
        return created_employee[0]
    except Exception as e:
        print(f"Error in get_employee: {e}")


async def validate_file(file_with_ext: str, content_type: str) -> tuple:
    """
    File validator

    Args:
        file_with_ext (str): [description]
        content_type (str): [file mime type]

    Returns:
        tuple: [integer file_id and ERRORS that happened during processing]
    """

    ERRORS = {}

    (name, ext) = (splitext(file_with_ext)[0], splitext(file_with_ext)[-1])

    try:
        is_valid_type = content_type == "text/csv" and ext in FILE_EXT
        if not is_valid_type:
            ERRORS["INVALID_TYPE"] = (
                f"Error: {file_with_ext} is not a valid text/csv file. "
                f"This API only supports text/csv files."
            )

        is_valid_name = bool(NAMING_CONVENTION.search(name))
        if not is_valid_name:
            ERRORS["INVALID_NAME"] = (
                f"Error: {file_with_ext} does not have the right naming convention. "
                f"This API only supports CSV files with strict `time-report-[0-9]+` "
                f"based naming where the digits represent the report ID."
            )
        file_id = int(name.split("-")[2]) if is_valid_type and is_valid_name else 0

        # check if file_id alreayd in database
        file_in_db = (
            file_id != 0 and await TimeReport.filter(report_id=file_id).exists()
        )
        if file_in_db:
            ERRORS["DUPLICATE_REPORT"] = f"Error: {file_with_ext} already exists in DB."

        print(
            (
                f"Validate file: {content_type}, {name}, {ext}, {is_valid_name}, "
                f"{is_valid_type}, {file_id}, {file_in_db}"
            )
        )
    except Exception as e:
        print(f"Error in validate_file: {e}")

    return (file_id, ERRORS)
