# RAG Study Assistant

An AI study agent that answers questions from my Agentic AI lecture PDFs, quizzes me on them, and remembers which topics I get wrong.

## Features
- **RAG search**: answers come from the lecture slides, with file and page cited
- **Quiz mode**: generates questions from the PDFs, one at a time, and grades each answer
- **Weak-topic tracker**: saves results in SQLite and shows what to review, even after restarting
- **Guardrails**: says so when the PDFs don't contain the answer instead of guessing
- **Per-session chat memory** so follow-up questions work
- **Web UI**: React frontend and Flask API

## How it works
1. `ingest.py` reads the PDFs, splits them into chunks, and embeds each chunk with a local HuggingFace model.
2. Vectors are saved to `vector_store.json`.
3. The LangChain agent (Groq LLM) decides which tool to call: `search_pdfs`, `make_quiz`, `log_quiz_result`, or `get_weak_topics`.
4. A Flask API exposes the agent to the React frontend.

## Tech stack
Python, LangChain, Groq (llama-3.3-70b-versatile), sentence-transformers, SQLite, Flask, React + Vite

## Setup
```bash
git clone https://github.com/Ameershahkhan/rag-study-assistant.git
cd rag-study-assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then add your GROQ_API_KEY
mkdir pdfs                # then copy your own lecture PDFs into it
python src/ingest.py      # builds the vector store
```

## Run
```bash
# Terminal 1: API
python src/app.py

# Terminal 2: frontend
cd frontend-react
npm install
npm run dev
```
Open http://localhost:5173

## Project structure
```
src/
  ingest.py     PDFs -> chunks -> vector store
  retrieval.py  similarity search
  agent.py      LangChain agent + system prompt
  db.py         SQLite helpers
  app.py        Flask API (/chat, /weak-topics)
  tools/        search_pdfs, make_quiz, tracker
frontend-react/ React + Vite UI
```

## Notes
The lecture PDFs are not included in this repository. Add your own PDFs to `pdfs/`.

## Roadmap
- Richer UI (source cards, quiz mode, dark mode)
- Streaming replies
- Persistent chat history