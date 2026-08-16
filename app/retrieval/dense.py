import os
import chromadb
from app.ingestion.embeddings import embed_texts

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./daya/processed/chroma")
COLLECTION_NAME = "internal_docs"

def dense_search(query: str, k: int = 10) -> list[dict]:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)
    query_emb = embed_texts([query])[0]
    results = collection.query(query_embeddings=[query_emb], n_results=k)

    out = []
    for i in range(len(results["ids"][0])):
        out.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "dense_distance": results["distances"][0][i],
            "dense_score": 1 / (1 + results["distances"][0][i]),
        })
    return out