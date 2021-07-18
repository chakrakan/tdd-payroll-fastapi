# payroll/app/tests/test_upload.py


def test_file_upload_valid(test_app):
    # Given
    filename = "time-report-2.csv"

    # When
    response = test_app.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "text/csv")}
    )

    json_response = response.json()

    # Then
    assert response.status_code == 202
    assert json_response["file_id"] == 2
    assert "Accepted" in json_response["message"]


def test_file_upload_invalid_name(test_app):
    # Given
    filename = "time-report-2copy.csv"

    # When
    response = test_app.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "text/csv")}
    )

    json_response = response.json()

    # Then
    assert response.status_code == 409
    assert json_response["file_id"] == 0
    assert "INVALID_NAME" in json_response["message"].keys()


def test_file_upload_invalid_type(test_app):
    # Given
    filename = "wave-logo.png"

    # When
    response = test_app.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "image/png")}
    )

    json_response = response.json()

    # Then
    assert response.status_code == 409
    assert json_response["file_id"] == 0
    assert "INVALID_TYPE" in json_response["message"].keys()
