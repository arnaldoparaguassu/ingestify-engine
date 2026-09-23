import pytest

from ingestify_engine.decorators import log_execution_time, retry


def test_log_execution_time_preserves_function_metadata() -> None:
    @log_execution_time
    def sample_func(a: int, b: int) -> int:
        """Soma dois números."""
        return a + b

    assert sample_func(2, 3) == 5
    assert sample_func.__name__ == "sample_func"
    assert sample_func.__doc__ == "Soma dois números."


def test_retry_succeeds_after_failures() -> None:
    attempts = 0

    @retry(max_attempts=3, delay=0.01, backoff_factor=1.0, exceptions=(ValueError,))
    def flaky_function() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Falha temporária")
        return "sucesso"

    result = flaky_function()
    assert result == "sucesso"
    assert attempts == 3


def test_retry_raises_exception_when_max_attempts_exceeded() -> None:
    attempts = 0

    @retry(max_attempts=2, delay=0.01, exceptions=(RuntimeError,))
    def always_fails() -> None:
        nonlocal attempts
        attempts += 1
        raise RuntimeError("Erro persistente")

    with pytest.raises(RuntimeError, match="Erro persistente"):
        always_fails()

    assert attempts == 2
