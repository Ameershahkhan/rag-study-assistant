from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_DIR = Path("pdfs")
STORE_PATH = Path("vector_store.json")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_pdfs(pdf_dir: Path) -> list[Document]:
    """Read every PDF and return one Document per page."""
    pages = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        reader = PdfReader(pdf_path)
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(
                    Document(
                        page_content=text,
                        metadata={"source": pdf_path.name, "page": page_number},
                    )
                )
    return pages


def build_store() -> None:
    pages = load_pdfs(PDF_DIR)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(pages)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    store = InMemoryVectorStore.from_documents(chunks, embeddings)
    store.dump(str(STORE_PATH))

    print(f"Pages read: {len(pages)}")
    print(f"Chunks stored: {len(chunks)}")
    print(f"Saved to: {STORE_PATH}")


if __name__ == "__main__":
    build_store()