from pathlib import Path

from ingestify_engine.domain import DocumentFormat, RawDocument


class LocalTextReader:
    """Leitor de arquivos de texto locais (.txt / .md).

    Observe que NÃO herdamos de DocumentReaderProtocol!
    Ainda assim, o Mypy validará que esta classe é totalmente compatível.
    """

    def read(self, source_path: str) -> RawDocument:
        path = Path(source_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")

        # Determina o formato com base na extensão
        ext = path.suffix.lower().lstrip(".")
        if ext not in ("txt", "md"):
            raise ValueError(f"Formato não suportado: {ext}")

        doc_format: DocumentFormat = ext  # type: ignore[assignment]

        content = path.read_text(encoding="utf-8")
        return RawDocument(content=content, source=str(path), doc_format=doc_format)
