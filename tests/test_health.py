from app import create_app


def test_health_endpoint_returns_ok():
    app = create_app()
    app.config.update(TESTING=True)

    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "application": "Uber 2",
        "version": "2.0.0",
    }
