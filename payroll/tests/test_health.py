# payroll/tests/test_ping.py


def test_health(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("/v1/health")

    # Then
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "status": "live", "testing": True}
