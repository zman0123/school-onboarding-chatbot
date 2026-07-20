import sqlite3


def save_result(question, result):

    conn = sqlite3.connect("onboarding.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO classified_data
        (
            question,
            sentence,
            categories,
            keywords,
            status
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            question,
            result["text"],
            ",".join(result["categories"]),
            ",".join(result["keywords"]),
            result["status"]
        )

    )

    conn.commit()

    print("DB저장완료")

    conn.close()