from app.ingestion.loader import RawDocument
from app.ingestion.chunking import fixed_size_chunking, structure_aware_chunking

def test_fixed_size():
    doc = RawDocument("d1", "path", "txt", "A " * 1000)
    chunks = fixed_size_chunking(doc, chunk_size=200, overlap=20)
    assert len(chunks) > 1
    assert all(c.chunking_strategy == "fixed_size" for c in chunks)

def test_structure_aware():
    text = "# Sekcja 1\nTreść A\n\n## Sekcja 2\nTreść B"
    doc = RawDocument("d2", "path", "markdown", text)
    chunks = structure_aware_chunking(doc)
    assert len(chunks) == 2
    assert chunks[0].section_heading == "Sekcja 1"