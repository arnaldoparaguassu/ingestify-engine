import re
from collections.abc import Callable
from functools import partial, reduce

# TypeAlias para legibilidade: uma transformação recebe str e retorna str
type TextTransform = Callable[[str], str]


# --- Funções Puras de Sanitização (Transformações Individuais) ---


def strip_whitespace(text: str) -> str:
    """Remove espaços em branco no início/fim e reduz múltiplos espaços internos a um só."""
    text = text.strip()
    return re.sub(r"\s+", " ", text)


def remove_special_characters(text: str, keep_accents: bool = True) -> str:
    """Remove caracteres especiais, mantendo letras, números e acentuação opcionalmente."""
    if keep_accents:
        # Mantém acentos e pontuação básica
        return re.sub(r"[^\w\s\.\,\!\?\-]", "", text)
    # Remove qualquer caractere não alfanumérico ASCII simples
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def remove_stopwords(text: str, stopwords: set[str]) -> str:
    """Remove uma lista/set de palavras de parada (stop-words)."""
    words = text.split()
    filtered = [w for w in words if w.lower() not in stopwords]
    return " ".join(filtered)


def to_lowercase(text: str) -> str:
    """Converte o texto para minúsculas."""
    return text.lower()


# --- Fatores / Builders de Funções Parciais ---


def create_stopword_filter(stopwords: set[str]) -> TextTransform:
    """Cria uma transformação configurada para um conjunto específico de stop-words via partial."""
    return partial(remove_stopwords, stopwords=stopwords)


# --- Pipeline Funcional de Composição ---


class TextSanitizerPipeline:
    """Engine de higienização de texto baseada em composição funcional de transformações."""

    def __init__(self, steps: list[TextTransform] | None = None) -> None:
        self.steps: list[TextTransform] = steps or []

    def add_step(self, transform: TextTransform) -> TextSanitizerPipeline:
        """Adiciona uma etapa ao pipeline (interface fluente)."""
        self.steps.append(transform)
        return self

    def sanitize(self, text: str) -> str:
        """Aplica todas as transformações em sequência usando functools.reduce."""
        return reduce(lambda current_text, fn: fn(current_text), self.steps, text)
