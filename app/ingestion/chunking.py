"""Three chunking strategies: fixed-size, structure-aware, semantic."""

from __future__ import annotations
import re
import numpy as np
from dataclasses import dataclass, field

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.loader import RawDocument

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    source_path: str
    text: str
    section_heading: str | None
    chunking_strategy: str
    char_count: int = field(init=False)

    def __post_init__(self):
        self.char_count = len(self.text)

def fixed_size_chunking(doc: RawDocument, chunk_size: int = 800, overlap: int = 150) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    pieces = splitter.split_text(doc.raw_text)
    return [
        Chunk(chunk_id=f"{doc.doc_id}-fixed-{i}", doc_id=doc.doc_id,
              source_path=doc.source_path, text=p, section_heading=None,
              chunking_strategy="fixed_size")
        for i, p in enumerate(pieces)
    ]

def structure_aware_chunking(doc: RawDocument) -> list[Chunk]:

    """Splits by markdown headers (#, ##, ###)."""

    lines = doc.raw_text.splitlines()
    sections: list[tuple[str | None, list[str]]] = [(None, [])]
    for line in lines:
        if re.match(r"^#{1,3}\s+", line):
            sections.append((line.lstrip("#").strip(), []))
        else:
            sections[-1][1].append(line)

    chunks = []
    for i, (heading, body_lines) in enumerate(sections):
        body = "\n".join(body_lines).strip()
        if not body:
            continue
        chunks.append(Chunk(
            chunk_id=f"{doc.doc_id}-struct-{i}", doc_id=doc.doc_id,
            source_path=doc.source_path, text=body,
            section_heading=heading, chunking_strategy="structure_aware"))
    return chunks

def semantic_chunking(doc: RawDocument, embed_fn, similarity_drop_threshold: float = 0.25) -> list[Chunk]:

    """It segments the text at topic shifts by calculating the cosine similarity of consecutive sentences."""

    sentences = re.split(r"(?<=[.!?])\s+", doc.raw_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) < 3:
        return fixed_size_chunking(doc)

    embeddings = embed_fn(sentences)
    boundaries = [0]
    for i in range(1, len(sentences)):
        sim = float(np.dot(embeddings[i], embeddings[i - 1]) /
                    (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i - 1]) + 1e-8))
        if sim < (1 - similarity_drop_threshold):
            boundaries.append(i)
    boundaries.append(len(sentences))

    chunks = []
    for i in range(len(boundaries) - 1):
        text = " ".join(sentences[boundaries[i]:boundaries[i + 1]])
        if not text.strip():
            continue
        chunks.append(Chunk(
            chunk_id=f"{doc.doc_id}-semantic-{i}", doc_id=doc.doc_id,
            source_path=doc.source_path, text=text, section_heading=None,
            chunking_strategy="semantic"))
    return chunks

STRATEGIES = {"fixed_size": fixed_size_chunking, "structure_aware": structure_aware_chunking,
              "semantic": semantic_chunking}