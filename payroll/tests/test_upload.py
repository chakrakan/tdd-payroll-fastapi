# payroll/app/tests/test_upload.py

import magic


mime = magic.Magic(mime=True)


def test_file_upload_valid(test_app, change_test_dir):
    # Given
    change_test_dir
    filename = "time-report-2.csv"

    # When
    response = test_app.post(
        "v1/upload", files={"csv_file": (filename, open(filename, "rb"), "text/csv")}
    )

    json_response = response.json()
    print(json_response)

    # Then
    assert response.status_code == 202
    assert json_response["file_id"] == 2
    assert "Accepted" in json_response["message"]


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
    assert "INVALID_NAME" in json_response["message"].keys()


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
