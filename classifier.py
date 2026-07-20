import sqlite3

# ------------------------------------
# 무응답 목록
# ------------------------------------

IGNORE_WORDS = {
    "",
    ".",
    "x",
    "ㄴ",
    "ㄴㄴ",
    "w",
    "없음",
    "없다",
    "없어요",
    "없어영",
    "없당",
    "무",
    "없습니다",
    "ㄹㄴㅁㅇㄹ"
}


# ------------------------------------
# SQLite에서 키워드 읽기
# ------------------------------------

def load_keywords():

    conn = sqlite3.connect("onboarding.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, keyword
        FROM keywords
    """)

    rows = cursor.fetchall()

    conn.close()

    keywords = []

    for category, keyword in rows:

        keywords.append((
            str(category).strip(),
            str(keyword).strip()
        ))

    return keywords


# ------------------------------------
# 문장 분류
# ------------------------------------

def classify_text(text):

    original_text = str(text).strip()

    # 무응답 확인용
    simple_text = original_text.lower().replace(" ", "")

    if simple_text in IGNORE_WORDS:

        return {
            "text": original_text,
            "status": "무응답",
            "categories": [],
            "keywords": []
        }

    keywords = load_keywords()

    matched_categories = set()
    matched_keywords = set()

    # 공백 제거 후 비교
    compare_text = original_text.lower().replace(" ", "")

    for category, keyword in keywords:

        keyword = keyword.strip()

        compare_keyword = keyword.lower().replace(" ", "")

        if compare_keyword == "":
            continue

        if compare_keyword in compare_text:

            matched_categories.add(category)
            matched_keywords.add(keyword)

    # 상태 결정
    if len(matched_categories) == 0:

        status = "미분류"

    elif len(matched_categories) == 1:

        status = "단일분류"

    else:

        status = "복수분류"

    return {

        "text": original_text,
        "status": status,
        "categories": sorted(list(matched_categories)),
        "keywords": sorted(list(matched_keywords))

    }


# ------------------------------------
# 테스트
# ------------------------------------

if __name__ == "__main__":

    while True:

        text = input("\n문장을 입력하세요 (종료:q) : ")

        if text.lower() == "q":
            break

        result = classify_text(text)

        print("\n===== 분류 결과 =====")
        print("입력 문장 :", result["text"])
        print("매칭 키워드 :", result["keywords"])
        print("매칭 카테고리 :", result["categories"])
        print("상태 :", result["status"])