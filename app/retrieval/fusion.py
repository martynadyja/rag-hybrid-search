"""Reciprocal Rank Fusion: combines the dense and sparse rankings into a single list."""

def reciprocal_rank_fusion(
        dense_results: list[dict], sparse_results: list[dict], 
        dense_weight: float = 0.7, sparse_weight: float = 0.3, k_constant: int = 60,
) -> list[dict]:
    scores: dict[str, float] = {}
    payload: dict[str, dict] = {}

    for rank, r in enumerate(dense_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0) + dense_weight * (1 / (k_constant + rank + 1))
        payload.setdefault(cid, r)

    for rank, r in enumerate(sparse_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0) + sparse_weight * (1 / (k_constant + rank + 1))
        if cid in payload:
            payload[cid].update({"bm25_score": r.get("bm25_score")})
        else:
            payload[cid] = r

    fused = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return [{**payload[cid], "rrf_score": score} for cid, score in fused]