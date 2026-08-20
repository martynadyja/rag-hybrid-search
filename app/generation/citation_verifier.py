"""Checks whether each citation [n] is actually supported by the content of source n."""

import re
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

VERIFY_PROMPT = """Does the following source SUPPORT this claim? Answer ONLY "YES" or "NO".

Claim: {claim}

Source:
{source_text}

Answer (YES/NO):"""

def extract_claims_with_citations(answer_text: str) -> list[tuple[str, list[int]]]:

    """Splits the answer into sentences and extracts citation numbers next to each sentence."""

    sentences = re.split(r"(?<=[.!?])\s+", answer_text)
    claims = []
    for sent in sentences:
        citation_nums = [int(n) for n in re.findall(r"\[(\d+)\]", sent)]
        if citation_nums:
            clean_claim = re.sub(r"\[\d+\]", "", sent).strip()
            claims.append((clean_claim, citation_nums))
    return claims

def verify_citations(answer_text: str, sources: list[dict]) -> dict:
    claims = extract_claims_with_citations(answer_text)
    sources_by_index = {s["index"]: s for s in sources}

    results = []
    for claim, citation_nums in claims:
        for num in citation_nums:
            source = sources_by_index.get(num)
            if source is None:
                results.append({"claim": claim, "citation": num, "verified": False, "reason": "no such source"})
                continue
            resp = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": VERIFY_PROMPT.format(
                    claim=claim, source_text=source["text"][:1500])}],
                    temperature=0, max_tokens=5,
            )
            verified = "YES" in resp.choices[0].message.content.upper()
            results.append({"claim": claim, "citation": num, "verified": verified})

    total = len(results)
    verified_count = sum(1 for r in results if r["verified"])
    coverage = verified_count / total if total else 1.0
    return {"claims": results, "citation_coverage": coverage}

