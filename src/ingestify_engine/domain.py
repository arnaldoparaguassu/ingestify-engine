from datetime import UTC, datetime
from typing import Literal, Protocol, TypeVar, runtime_checkable
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

# Literal: Garante em tempo de checagem estática que apenas estes formatos são aceitos
DocumentFormat = Literal["pdf", "txt", "md"]

# TypeVar: Cria um genérico T para nossos repositórios/leitores
T = TypeVar("T")


class DocumentMetadata(BaseModel):
    """Metadados associados a um documento processado."""

    model_config = ConfigDict(frozen=True)

    author: str | None = None
    tags: list[str] = Field(default_factory=list)
    custom_attributes: dict[str, str] = Field(default_factory=dict)


class RawDocument(BaseModel):
    """Representa um documento bruto carregado na memória.

    Substituímos a classe simples por um modelo Pydantic validado e imutável.
    """

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    content: str = Field(min_length=1, description="O conteúdo em texto do documento")
    source: str = Field(description="Caminho do arquivo ou URI de origem")
    doc_format: DocumentFormat
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)


class DocumentChunk(BaseModel):
    """Representa um trecho (chunk) de um documento após a fase de quebra/chunking."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    chunk_index: int = Field(ge=0, description="Índice sequencial do chunk no documento")
    content: str = Field(min_length=1)
    token_count: int = Field(ge=0)


@runtime_checkable
class DocumentReaderProtocol(Protocol):
    """Protocolo (Interface) para leitores de documentos."""

    def read(self, source_path: str) -> RawDocument: ...


@runtime_checkable
class StorageProtocol(Protocol[T]):
    """Protocolo Genérico para persistência de dados."""

    def save(self, item: T) -> bool: ...

    def fetch(self, item_id: str) -> T | None: ...
