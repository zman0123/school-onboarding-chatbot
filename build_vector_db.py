import sqlite3
import chromadb

from embedding import model


# -------------------------
# ChromaDB 생성
# -------------------------

client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection("onboarding")
    print("기존 컬렉션 삭제")
except:
    pass

collection = client.create_collection(
    name="onboarding",
    metadata={
        "hnsw:space": "cosine"
    }
)


# -------------------------
# SQLite 읽기
# -------------------------

conn = sqlite3.connect("onboarding.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    sentence,
    categories,
    source,
    image_path,
    pdf_path,
    image_description
FROM classified_data
WHERE status != '무응답'
""")

rows = cursor.fetchall()

conn.close()

print(f"\n총 {len(rows)}개의 문장을 임베딩합니다.\n")


# -------------------------
# ChromaDB 저장
# -------------------------

for row in rows:

    row_id = row[0]
    sentence = row[1]
    categories = row[2]
    source = row[3]
    image_path = row[4]
    pdf_path = row[5]

    embedding = model.encode(sentence).tolist()

    category_list = [
        c.strip()
        for c in categories.split(",")
    ]

    for index, category in enumerate(category_list):

        metadata = {
            "category": category,
            "source": source
        }

        if image_path:
            metadata["image_path"] = image_path

        if pdf_path:
            metadata["pdf_path"] = pdf_path

        collection.add(

            ids=[f"{row_id}_{index}"],

            embeddings=[embedding],

            documents=[sentence],

            metadatas=[metadata]

        )

print("\n벡터 DB 생성 완료")
print("문서 개수 :", collection.count())