"""Multi-format document loader: markdown, txt, html, pdf -> clean plaintext + metadata."""

from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

@dataclass
class RawDocument:
    doc_id: str
    source_path: str
    file_type: str
    raw_text: str
    pages: list[str] = field(default_factory=list) # for PDF, per-page text

def _hash_path(path: Path) -> str:
    return hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]

def load_markdown(path: Path) -> RawDocument:
    text = path.read_text(encoding="utf-8")
    return RawDocument(doc_id=_hash_path(path), source_path=str(path),
                       file_type="markdown", raw_text=text)

def load_txt(path: Path) -> RawDocument:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return RawDocument(doc_id=_hash_path(path), source_path=str(path),
                       file_type="txt", raw_text=text)

def load_html(path: Path) -> RawDocument:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return RawDocument(doc_id=_hash_path(path), source_path=str(path),
                       file_type="html", raw_text=text)

def load_pdf(path: Path) -> RawDocument:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    full_text = "\n\n".join(pages)
    return RawDocument(doc_id=_hash_path(path), source_path=str(path),
                       file_type="pdf", raw_text=full_text, pages=pages)

LOADERS = {".md": load_markdown, ".txt": load_txt, ".html": load_html,
           ".htm": load_html, ".pdf": load_pdf}

def load_document(path: str | Path) -> RawDocument:
    path = Path(path)
    loader = LOADERS.get(path.suffix.lower())
    if loader is None:
        raise ValueError(f"Unsupported file type: {path.suffix}.")
    return loader(path)

def load_directory(directory: str | Path) -> list[RawDocument]:
    directory = Path(directory)
    docs = []
    for suffix in LOADERS:
        for path in directory.rglob(f"*{suffix}"):
            try:
                docs.append(load_document(path))
            except Exception as e:
                print(f"[WARN] Failed to load {path}: {e}.")
    return docs