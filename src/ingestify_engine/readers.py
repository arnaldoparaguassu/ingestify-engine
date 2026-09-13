from pathlib import Path
from typing import cast

from ingestify_engine.domain import DocumentFormat, RawDocument


class LocalTextReader:
    """Leitor de arquivos de texto locais (.txt / .md)."""

    def read(self, source_path: str) -> RawDocument:
        path = Path(source_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")

        # Determina o formato com base na extensão
        ext = path.suffix.lower().lstrip(".")
        if ext not in ("txt", "md"):
            raise ValueError(f"Formato não suportado: {ext}")

        doc_format: DocumentFormat = cast(DocumentFormat, ext)

        content = path.read_text(encoding="utf-8")

        return RawDocument(
            content=content,
            source=str(path),
            doc_format=doc_format,
        )
