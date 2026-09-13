from pathlib import Path

import pytest
from pydantic import ValidationError

from ingestify_engine.domain import DocumentReaderProtocol, RawDocument
from ingestify_engine.readers import LocalTextReader


def process_with_protocol(reader: DocumentReaderProtocol, path: str) -> RawDocument:
    """Função auxiliar que exige que o argumento siga o Protocolo."""
    return reader.read(path)


def test_local_text_reader_satisfies_protocol(tmp_path: Path) -> None:
    # Arrange: Cria um arquivo temporário usando a fixture 'tmp_path' do pytest
    test_file = tmp_path / "sample.md"
    test_content = "# Hello Ingestify\nEste é um teste de ingestão com Pydantic."
    test_file.write_text(test_content, encoding="utf-8")

    reader = LocalTextReader()

    # Act
    doc = process_with_protocol(reader, str(test_file))

    # Assert
    assert doc.content == test_content
    assert doc.doc_format == "md"
    assert doc.id is not None
    assert isinstance(reader, DocumentReaderProtocol)


def test_local_text_reader_file_not_found() -> None:
    reader = LocalTextReader()

    with pytest.raises(FileNotFoundError):
        reader.read("arquivo_inexistente.txt")


def test_pydantic_validation_empty_content() -> None:
    # O Pydantic deve disparar ValidationError se min_length=1 for violado
    with pytest.raises(ValidationError):
        RawDocument(content="", source="test.txt", doc_format="txt")


def test_pydantic_immutability() -> None:
    doc = RawDocument(content="Conteúdo original", source="test.txt", doc_format="txt")

    # Como configuramos model_config = ConfigDict(frozen=True), a alteração deve falhar
    with pytest.raises(ValidationError):
        doc.content = "Novo conteúdo"  # type: ignore[misc]
