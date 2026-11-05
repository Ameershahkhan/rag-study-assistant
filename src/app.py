import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from agent import build_agent
from pathlib import Path
from flask import send_from_directory
from db import fetch_weak_topics

app = Flask(__name__)
CORS(app)
agent = build_agent()


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify(error="message is required"), 400

    session_id = data.get("session_id") or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": message}]}, config
        )
    except Exception:
        app.logger.exception("Agent call failed")
        return jsonify(error="The agent failed. Check the server logs."), 500

    return jsonify(reply=result["messages"][-1].content, session_id=session_id)


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/weak-topics")
def weak_topics():
    rows = fetch_weak_topics()
    return jsonify(
        topics=[{"topic": t, "total": n, "correct": c} for t, n, c in rows]
    )



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)