from collections.abc import Generator

import tiktoken

from ingestify_engine.domain import DocumentChunk, RawDocument


class ChunkSplitter:
    """Fatia um RawDocument em múltiplos DocumentChunks usando Generators (Streaming)."""

    def __init__(self, model_name: str = "gpt-4o", max_tokens_per_chunk: int = 100) -> None:
        self.tokenizer = tiktoken.encoding_for_model(model_name)
        self.max_tokens = max_tokens_per_chunk

    def split(self, document: RawDocument) -> Generator[DocumentChunk]:
        """Gera chunks sob demanda (lazy evaluation) via yield."""

        tokens = self.tokenizer.encode(document.content)
        total_tokens = len(tokens)

        if total_tokens == 0:
            return

        for chunk_index, i in enumerate(range(0, total_tokens, self.max_tokens)):
            chunk_tokens = tokens[i : i + self.max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            yield DocumentChunk(
                document_id=document.id,
                content=chunk_text,
                chunk_index=chunk_index,
                token_count=len(chunk_tokens),
            )
