from typing import Final

# Configurações globais do Ingestify Engine
APP_NAME: Final[str] = "Ingestify Engine"
VERSION: Final[str] = "0.1.0"


def get_engine_status() -> dict[str, str]:
    """Retorna o status básico de operação do motor de ingestão."""
    return {"app": APP_NAME, "version": VERSION, "status": "operational"}