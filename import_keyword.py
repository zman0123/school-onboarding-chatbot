import sqlite3
import pandas as pd

# 1. 엑셀 파일 읽기
df = pd.read_excel("keywords.xlsx")

# 2. SQLite 연결
conn = sqlite3.connect("onboarding.db")
cursor = conn.cursor()

# 3. 엑셀 데이터를 하나씩 DB에 저장
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO keywords (category, keyword)
        VALUES (?, ?)
    """, (row["category"], row["keyword"]))

# 4. 저장
conn.commit()

# 5. 연결 종료
conn.close()

print("키워드 등록 완료!")