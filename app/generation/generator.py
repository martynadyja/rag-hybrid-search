import os
from openai import OpenAI
from app.generation.prompts import SYSTEM_PROMPT, format_context_blocks

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

def generate_answer(question: str, retrieved_chunks: list[dict]) -> dict:
    if not retrieved_chunks:
        return {
            "answer": "I did not find any related information in the documentation.", 
            "citations_used": [], "sources": [],
        }

    context_blocks = format_context_blocks(retrieved_chunks)
    prompt = SYSTEM_PROMPT.format(context_blocks=context_blocks, question=question)

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    answer_text = resp.choices[0].message.content

    sources = [{
        "index": i + 1, "chunk_id": c["chunk_id"],
        "source_path": c["metadata"].get("source_path"),
        "section_heading": c["metadata"].get("section_heading"),
        "text": c["text"],
    } for i, c in enumerate(retrieved_chunks)]

    return {"answer": answer_text, "sources": sources}