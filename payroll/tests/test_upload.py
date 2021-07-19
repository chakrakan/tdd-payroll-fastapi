# payroll/app/tests/test_upload.py

import magic


mime = magic.Magic(mime=True)


def test_file_upload_valid(test_app_with_db, change_test_dir):
    # Given
    change_test_dir
    filename = "time-report-2.csv"

    # When
    response = test_app_with_db.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "text/csv")}
    )

    json_response = response.json()

    # Then
    assert response.status_code in (202, 409)
    assert json_response["file_id"] == 2
    assert (
        "Accepted" in json_response["message"]
        if type(json_response["message"]) is not dict
        else "DUPLICATE_REPORT" in json_response["message"].keys()
    )


def test_file_upload_invalid_name(test_app, change_test_dir):
    # Given
    change_test_dir
    filename = "time-report-2copy.csv"

    # When
    response = test_app.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "text/csv")}
    )

    json_response = response.json()

    # Then
    assert response.status_code == 409
    assert json_response["file_id"] == 0


def test_file_upload_valid_empty(test_app_with_db, change_test_dir):
    # Given
    change_test_dir
    filename = "time-report-43.csv"

    # When
    response = test_app_with_db.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "text/csv")}
    )

    json_response = response.json()

    # Then
    assert response.status_code == 202
    assert json_response["file_id"] == 43
    assert (
        "Accepted" in json_response["message"]
        if type(json_response["message"]) is not dict
        else "DUPLICATE_REPORT" in json_response["message"].keys()
    )


def test_file_upload_invalid_type(test_app, change_test_dir):
    # Given
    change_test_dir
    filename = "wave-logo.png"
    mime_type = mime.from_file(filename)

    # When
    response = test_app.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), mime_type)}
    )

    json_response = response.json()

    # Then
    assert response.status_code == 409
    assert json_response["file_id"] == 0
    assert "INVALID_TYPE" in json_response["message"].keys()
