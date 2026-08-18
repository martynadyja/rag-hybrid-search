"""Cross-encoder-style reranking via LLM-as-judge: evaluates the relevance of top-N candidates."""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAi_API_KEY"])
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

RERANK_PROMPT = """Rate the relevance of the following passage to the user's question.
Return ONLY a number from 0 to 10 (0 = completely irrelevant, 10 = perfectly answers the question).

Question: {query}

Passage:
{text}

Score (number only):"""

def _score_one(query: str, text: str) -> float:
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": RERANK_PROMPT.format(query=query, text=text[:1500])}],
        temperature=0,
        max_tokens=5,
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return float(raw.split()[0])
    except (ValueError, IndexError):
        return 0.0

def rerank(query: str, candidates: list[dict], top_k: int = 5, candidate_pool: int = 20) -> list[dict]:
    pool = candidates[:candidate_pool]
    for c in pool:
        c["rerank_score"] = _score_one(query, c["text"])
    pool.sort(key=lambda c: c["rerank_score"], reverse=True)
    return pool[:top_k]