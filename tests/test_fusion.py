from app.retrieval.fusion import reciprocal_rank_fusion

def test_rrf_merges_and_ranks():
    dense = [{"chunk_id": "a"}, {"chunk_id": "b"}, {"chunk_id": "c"}]
    sparse = [{"chunk_id": "c"}, {"chunk_id": "a"}, {"chunk_id": "d"}]
    fused = reciprocal_rank_fusion(dense, sparse)
    ids = [r["chunk_id"] for r in fused]
    assert "a" in ids and "c" in ids
    assert ids[0] in ("a", "c") # both high up on both lists