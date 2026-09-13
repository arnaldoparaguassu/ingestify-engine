from pathlib import Path

import pytest

from ingestify_engine.domain import DocumentReaderProtocol, RawDocument
from ingestify_engine.readers import LocalTextReader


def process_with_protocol(reader: DocumentReaderProtocol, path: str) -> RawDocument:
    """Função auxiliar que exige que o argumento siga o Protocolo."""
    return reader.read(path)


def test_local_text_reader_satisfies_protocol(tmp_path: Path) -> None:
    # Arrange: Cria um arquivo temporário usando a fixture 'tmp_path' do pytest
    test_file = tmp_path / "sample.md"
    test_content = "# Hello DocMind\nEste é um teste de ingestão."
    test_file.write_text(test_content, encoding="utf-8")

    reader = LocalTextReader()

    # Act: Passamos o reader para uma função que exige o DocumentReaderProtocol
    doc = process_with_protocol(reader, str(test_file))

    # Assert
    assert doc.content == test_content
    assert doc.doc_format == "md"
    assert isinstance(reader, DocumentReaderProtocol)  # Validação do runtime_checkable


def test_local_text_reader_file_not_found() -> None:
    reader = LocalTextReader()

    with pytest.raises(FileNotFoundError):
        reader.read("arquivo_inexistente.txt")
