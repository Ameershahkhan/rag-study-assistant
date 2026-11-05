import sqlite3
from pathlib import Path

DB_PATH = Path("study.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            question TEXT NOT NULL,
            correct INTEGER NOT NULL,
            source TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn


def fetch_weak_topics(limit: int = 5):
    """Return (topic, total, num_correct) rows, weakest topics first."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT topic, COUNT(*) AS total, SUM(correct) AS num_correct
            FROM quiz_results
            GROUP BY topic
            ORDER BY 1.0 * SUM(correct) / COUNT(*) ASC, total DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()