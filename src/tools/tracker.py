from langchain.tools import tool

from db import get_connection, fetch_weak_topics


@tool
def log_quiz_result(topic: str, question: str, correct: bool, source: str = "") -> str:
    """Save whether the student answered a quiz question correctly.
    Call this after grading every quiz answer."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO quiz_results (topic, question, correct, source) "
            "VALUES (?, ?, ?, ?)",
            (topic.lower().strip(), question, int(correct), source),
        )
    return "Result saved."

@tool
def get_weak_topics() -> str:
    """Show the topics the student struggles with most, based on past quizzes.
    Use this when the student asks what to review or what they are weak at."""
    rows = fetch_weak_topics()
    if not rows:
        return "No quiz results yet."
    return "\n".join(f"{topic}: {n}/{total} correct" for topic, total, n in rows)