from ingestify_engine.config import APP_NAME, VERSION, get_engine_status


def test_engine_status_returns_correct_data() -> None:
    # Arrange & Act
    status = get_engine_status()

    # Assert
    assert status["app"] == APP_NAME
    assert status["version"] == VERSION
    assert status["status"] == "operational"