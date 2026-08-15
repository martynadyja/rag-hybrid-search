"""Chunk deduplication via cosine similarity."""

import numpy as np

def find_duplicates(embeddings: np.ndarray, threshold: float = 0.95) -> set[int]:

    """Returns a set of chunk indices that are near-duplicates of earlier ones."""

    duplicates = set()
    kept_embeddings = []
    kept_indices = []
    for i, emb in enumerate(embeddings):
        is_dup = False
        for kept_idx, kept_emb in zip(kept_indices, kept_embeddings):
            sim = float(np.dot(emb, kept_emb) / (np.linalg.norm(emb) * np.linalg.norm(kept_emb) + 1e-8))
            if sim > threshold:
                duplicates.add(i)
                is_dup = True
                break
        if not is_dup:
            kept_embeddings.append(emb)
            kept_indices.append(i)
    return duplicates