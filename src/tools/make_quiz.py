from langchain.tools import tool

from retrieval import search


@tool
def make_quiz(topic: str, num_questions: int = 5) -> str:
    """Create a quiz on a topic from the lecture PDFs.
    Use this when the student asks to be quizzed or tested."""
    results = search(topic, k=6)
    material = "\n\n".join(
        f"[{doc.metadata['source']} - page {doc.metadata['page']}]\n{doc.page_content}"
        for doc, _score in results
    )
    return (
        f"Write {num_questions} quiz questions about '{topic}' using ONLY the "
        "material below. Ask one question at a time and wait for the student's "
        "answer. Never show answers in advance. After each answer, say if it was "
        "correct, explain why, and cite the page.\n\n"
        f"MATERIAL:\n{material}"
    )