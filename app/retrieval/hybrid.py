from app.retrieval.dense import dense_search
from app.retrieval.sparse import sparse_search
from app.retrieval.fusion import reciprocal_rank_fusion
from app.retrieval.reranker import rerank

def hybrid_search(
        query: str, k: int = 20, dense_weight: float = 0.7, sparse_weight: float = 0.3,
        use_reranker: bool = True, final_k: int = 5,
        ) -> list[dict]:
    dense_results = dense_search(query, k=k)
    sparse_results = sparse_search(query, k=k)
    fused = reciprocal_rank_fusion(dense_results, sparse_results, dense_weight, sparse_weight)

    if use_reranker:
        return rerank(query, fused, top_k=final_k, candidate_pool=20)
    return fused[:final_k]