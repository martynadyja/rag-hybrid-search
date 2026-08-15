"""Generating embeddings via OpenAI with retries."""

import os
import numpy as np
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=10))
def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    resp = client.embeddings.create(model=MODEL, input=texts)
    return [d.embedding for d in resp.data]

def embed_texts_np(texts: list[str]):
    return np.array(embed_texts(texts))