"""It builds a ChromaDB (dense) index and a BM25 (sparse) index from the same chunks."""

import os
import pickle
from pathlib import Path

import chromadb
from rank_bm25 import BM25Okapi

from app.ingestion.chunking import Chunk
from app.ingestion.dedup import find_duplicates
from app.ingestion.embeddings import embed_texts_np

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/processed/chroma")
BM25_PATH = os.getenv("BM25_INDEX_PATH", "./data/processed/bm25_index.pkl")
COLLECTION_NAME = "internal_docs"

def _tokenize(text: str) -> list[str]:
    return text.lower().split()

def build_indexes(chunks: list[Chunk], dedup_threshold: float = 0.95) -> dict:
    texts = [c.text for c in chunks]
    embeddings = embed_texts_np(texts)

    dup_indices = find_duplicates(embeddings, threshold=dedup_threshold)
    kept = [(c, e) for i, (c, e) in enumerate(zip(chunks, embeddings)) if i not in dup_indices]
    print(f"[dedup] {len(dup_indices)}/{len(chunks)} chunks discarded as duplicates.")

    kept_chunks = [c for c, _ in kept]
    kept_embeddings = [e.tolist() for _, e in kept]

    # --- Dense index: ChromaDB ---

    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)
    collection.add(
        ids=[c.chunk_id for c in kept_chunks],
        embeddings=kept_embeddings,
        documents=[c.text for c in kept_chunks],
        metadatas=[{
            "source_path": c.source_path, "chunking_strategy": c.chunking_strategy,
            "section_heading": c.section_heading or "", "char_count": c.char_count,
            "doc_id": c.doc_id,
        } for c in kept_chunks],
    )

    # --- Sparse index: BM25 ---

    tokenized = [_tokenize(c.text) for c in kept_chunks]
    bm25 = BM25Okapi(tokenized)
    Path(BM25_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(BM25_PATH, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": kept_chunks}, f)

    return {"total_chunks": len(chunks), "kept": len(kept_chunks), "duplicates": len(dup_indices)}