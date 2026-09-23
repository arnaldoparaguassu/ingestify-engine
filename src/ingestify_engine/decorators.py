import functools
import logging
import time
from collections.abc import Callable

logger = logging.getLogger("ingestify_engine")


def log_execution_time[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Decorador que mede e registra o tempo de execução de uma função."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed_time = time.perf_counter() - start_time
            logger.info(f"Função '{func.__name__}' executada em {elapsed_time:.4f}s")

    return wrapper


def retry[**P, R](
    max_attempts: int = 3,
    delay: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorador parametrizado que aplica retry com backoff exponencial."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        logger.error(
                            f"Função '{func.__name__}' falhou após {max_attempts} tentativas. Erro: {exc}"
                        )
                        raise

                    logger.warning(
                        f"Tentativa {attempt}/{max_attempts} falhou para '{func.__name__}'. "
                        f"Aguardando {current_delay:.2f}s antes do retry. Erro: {exc}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff_factor

            # Garantia do fluxo estático
            raise RuntimeError("Execução inalcançável no retry")

        return wrapper

    return decorator
