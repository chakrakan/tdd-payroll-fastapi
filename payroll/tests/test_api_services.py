# payroll/tests/test_api_services.py

# from ..app.api.services import generate_report_service


# def test_new_file_conflicting_date(test_app_with_db, change_test_dir):
#     # Given
#     change_test_dir
#     first_filename = "time-report-2.csv"

#     first_response = test_app_with_db.post(
#         "v1/upload",
#         files={"csv_file": (first_filename, open(first_filename, "rb"), "text/csv")},
#     )

#     first_json_response = first_response.json()

#     assert first_json_response.status_code == 409
#     assert first_json_response["file_id"] == 2
#     assert "Accepted" in first_json_response["message"]

#     second_filename = "time-report-3.csv"

#     second_response = test_app_with_db.post(
#         "v1/upload",
#         files={"csv_file": (second_filename, open(second_filename, "rb"),
#                    "text/csv")},
#     )

#     second_json_response = second_response.json()

#     assert second_json_response.status_code == 202
#     assert second_json_response["file_id"] == 3
#     assert "Accepted" in second_json_response["message"]

# Then
# (REPORT, ERRORS) = await generate_report_service()
