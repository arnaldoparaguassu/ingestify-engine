import types

from ingestify_engine.domain import RawDocument
from ingestify_engine.splitter import ChunkSplitter


def test_chunk_splitter_generates_stream() -> None:
    doc = RawDocument(
        content="Python e IA com Ingestify Engine. " * 20,
        source="test.txt",
        doc_format="txt",
    )

    splitter = ChunkSplitter(max_tokens_per_chunk=15)
    chunks_generator = splitter.split(doc)

    # Valida se o retorno é de fato um Generator (Lazy evaluation) e não uma lista pronta
    assert isinstance(chunks_generator, types.GeneratorType)

    # Consome os chunks do gerador
    chunks = list(chunks_generator)

    assert len(chunks) > 1
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert all(c.token_count <= 15 for c in chunks)
    assert chunks[0].document_id == doc.id
