"""Grounded generation prompt with numbered source citations."""

SYSTEM_PROMPT = """You are an assistant that answers ONLY based on the context provided below.

Rules:
1. Answer only using the context fragments below - do not use any external knowledge.
2. Mark every specific claim with the source number in square brackets, e.g. [1], [2].
3. If the context does not contain enough information, say so explicitly - do not guess.
4. If different fragments contradict each other, point out that discepancy.

Context:
{context_blocks}

User question: {question}

Answer concisely, with citations in square brackets."""

def format_context_blocks(chunks: list[dict]) -> str:
    blocks = []
    for i, c in enumerate(chunks, start=1):
        source = c["metadata"].get("source_path", "unknown")
        heading = c["metadata"].get("section_heading", "")
        blocks.append(f"[{i}] (source: {source}{' - ' + heading if heading else ''})\n{c['text']}")
    return "\n\n".join(blocks)