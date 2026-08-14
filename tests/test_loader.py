from pathlib import Path
from app.ingestion.loader import load_directory

def test_load_sample_docs(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("# Tytuł\n\nTreść dokumentu testowego.", encoding="utf-8")
    docs = load_directory(tmp_path)
    assert len(docs) == 1
    assert docs[0].file_type == "markdown"
    assert "Treść" in docs[0].raw_text