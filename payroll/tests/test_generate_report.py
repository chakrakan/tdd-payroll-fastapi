# payroll/tests/test_generate_report.py


def test_generate_with_data(test_app_with_db):
    # Given

    # When
    response = test_app_with_db.get("v1/report")

    json_response = response.json()

    # Then
    assert response.status_code == 200
    assert len(json_response["payrollReport"]["employeeReports"]) > 0
