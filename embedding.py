import sqlite3
import chromadb

from sentence_transformers import SentenceTransformer


print("모델 불러오는 중...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("모델 로드 완료")


client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection("onboarding")
    print("기존 컬렉션 삭제")
except:
    pass

collection = client.create_collection(
    name="onboarding",
    metadata={
        "hnsw:space":"cosine"
    }
)

conn = sqlite3.connect("onboarding.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    sentence,
    categories
FROM classified_data
WHERE status != '무응답'
""")

rows = cursor.fetchall()

conn.close()


print(f"\n총 {len(rows)}개의 문장을 임베딩합니다.\n")


for row in rows:

    row_id = row[0]
    sentence = row[1]
    categories = row[2]

    embedding = model.encode(sentence).tolist()

    # 쉼표 기준으로 분리
    category_list = [c.strip() for c in categories.split(",")]

    # 카테고리마다 하나씩 저장
    for index, category in enumerate(category_list):

        collection.add(

            ids=[f"{row_id}_{index}"],

            embeddings=[embedding],

            documents=[sentence],

            metadatas=[

                {
                    "category": category
                }

            ]

        )

print("완료!")
print(collection.count())