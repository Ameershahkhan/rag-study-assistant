from functools import lru_cache

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from ingest import EMBEDDING_MODEL, STORE_PATH


@lru_cache(maxsize=1)
def load_store() -> InMemoryVectorStore:
    """Load the saved vectors once and reuse them."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return InMemoryVectorStore.load(str(STORE_PATH), embeddings)


def search(query: str, k: int = 4):
    """Return the k most similar chunks as (Document, score) pairs."""
    return load_store().similarity_search_with_score(query, k=k)


if __name__ == "__main__":
    question = input("Ask something about your lectures: ")
    for doc, score in search(question):
        print(f"[{score:.2f}] {doc.metadata['source']} - page {doc.metadata['page']}")
        print(doc.page_content[:200].replace("\n", " "))
        print()