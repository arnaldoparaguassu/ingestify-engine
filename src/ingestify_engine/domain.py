from typing import Literal, Protocol, TypeVar, runtime_checkable

# Literal: Garante em tempo de checagem estática que apenas estes formatos são aceitos
DocumentFormat = Literal["pdf", "txt", "md"]

# TypeVar: Cria um genérico T para nossos repositórios/leitores
T = TypeVar("T")


class RawDocument:
    """Representa um documento bruto carregado na memória."""

    def __init__(self, content: str, source: str, doc_format: DocumentFormat) -> None:
        self.content = content
        self.source = source
        self.doc_format = doc_format


# runtime_checkable permite usar isinstance(obj, DocumentReaderProtocol) se necessário
@runtime_checkable
class DocumentReaderProtocol(Protocol):
    """Protocolo (Interface) para leitores de documentos.

    Qualquer classe que implemente 'read' com esta assinatura
    satisfaz o protocolo automaticamente (Duck Typing Estático).
    """

    def read(self, source_path: str) -> RawDocument: ...


@runtime_checkable
class StorageProtocol(Protocol[T]):
    """Protocolo Genérico para persistência de dados."""

    def save(self, item: T) -> bool: ...

    def fetch(self, item_id: str) -> T | None: ...
