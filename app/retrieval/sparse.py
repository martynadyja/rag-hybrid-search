import pickle
import os

BM25_PATH = os.getenv("BM25_INDEX_PATH", "./data/processed/bm25_index.pkl")

def _tokenize(text: str) -> list[str]:
    return text.lower().split()

def sparse_search(query: str, k: int = 10) -> list[dict]:
    with open(BM25_PATH, "rb") as f:
        data = pickle.load(f)
    bm25, chunks = data["bm25"], data["chunks"]

    scores = bm25.get_scores(_tokenize(query))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    out = []
    for idx in ranked:
        chunk = chunks[idx]
        out.append({
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
            "metadata": {"source_path": chunk.source_path, "section_heading": chunk.section_heading},
            "bm25_score": float(scores[idx]),
        })
    return out