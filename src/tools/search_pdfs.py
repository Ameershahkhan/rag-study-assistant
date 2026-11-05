from langchain.tools import tool

from retrieval import search


@tool
def search_pdfs(query: str) -> str:
    """Search the lecture PDFs for information about a topic.
    Use this for any question about the course material."""
    results = search(query, k=4)
    parts = []
    for doc, _score in results:
        label = f"[{doc.metadata['source']} - page {doc.metadata['page']}]"
        parts.append(f"{label}\n{doc.page_content}")
    return "\n\n".join(parts)