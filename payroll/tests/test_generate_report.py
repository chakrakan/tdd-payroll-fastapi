# payroll/tests/test_generate_report.py


def test_generate_with_data(test_app_with_db, change_test_dir):
    # Given
    change_test_dir
    first_filename = "time-report-2.csv"

    test_app_with_db.post(
        "v1/upload",
        files={"csv_file": (first_filename, open(first_filename, "rb"), "text/csv")},
    )

    # When
    response = test_app_with_db.get("v1/report")

    json_response = response.json()

    # Then
    assert response.status_code == 409
    assert "INVALID_DATA" in json_response.keys()


def test_new_file_conflicting_date(test_app_with_db, change_test_dir):
    # Given
    change_test_dir
    first_filename = "time-report-2.csv"

    test_app_with_db.post(
        "v1/upload",
        files={"csv_file": (first_filename, open(first_filename, "rb"), "text/csv")},
    )

    second_filename = "time-report-3.csv"

    test_app_with_db.post(
        "v1/upload",
        files={"csv_file": (second_filename, open(second_filename, "rb"), "text/csv")},
    )

    response = test_app_with_db.get("v1/report")
    json_response = response.json()

    # Then
    assert response.status_code == 409
    assert "INVALID_DATA" in json_response.keys()
