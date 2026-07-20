import sqlite3
from datetime import datetime


def save_result(question, answer, category, matched_keywords, status):

    conn = sqlite3.connect("onboarding.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses
        (question, answer, category, matched_keywords, status, created_at)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        question,
        answer,
        category,
        matched_keywords,
        status,
        datetime.now()
    ))

    conn.commit()
    conn.close()