from ingestify_engine.sanitizer import (
    TextSanitizerPipeline,
    create_stopword_filter,
    remove_special_characters,
    strip_whitespace,
    to_lowercase,
)


def test_strip_whitespace() -> None:
    raw = "   Texto   com    muitos   espaços.   \n\t"
    assert strip_whitespace(raw) == "Texto com muitos espaços."


def test_remove_special_characters() -> None:
    raw = "Olá, Mundo! @#$ Teste_123."
    cleaned = remove_special_characters(raw, keep_accents=True)
    assert cleaned == "Olá, Mundo!  Teste_123."


def test_sanitizer_pipeline_execution() -> None:
    # Arrange: Configura stop-words e cria o pipeline
    pt_stopwords = {"de", "em", "o", "a", "para"}
    stopword_step = create_stopword_filter(pt_stopwords)

    pipeline = (
        TextSanitizerPipeline()
        .add_step(strip_whitespace)
        .add_step(to_lowercase)
        .add_step(stopword_step)
    )

    # Act
    raw_text = "   Este é um Texto DE Exemplo PARA Ingestão em IA!   "
    result = pipeline.sanitize(raw_text)

    # Assert
    assert result == "este é um texto exemplo ingestão ia!"


def test_empty_pipeline_returns_original_text() -> None:
    pipeline = TextSanitizerPipeline()
    original = "Texto Intacto"
    assert pipeline.sanitize(original) == original
