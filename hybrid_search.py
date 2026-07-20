import chromadb

from sentence_transformers import SentenceTransformer

from classifier import classify_text


# ----------------------------
# 모델 로드
# ----------------------------

print("모델 불러오는 중...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("모델 로드 완료")


# ----------------------------
# ChromaDB 연결
# ----------------------------

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("onboarding")


# ----------------------------
# 질문 입력
# ----------------------------

query = input("\n질문을 입력하세요 : ")


# ----------------------------
# 카테고리 분류
# ----------------------------

result = classify_text(query)

categories = result["categories"]

print("\n감지된 카테고리 :", categories)


# ----------------------------
# 질문 임베딩
# ----------------------------

query_embedding = model.encode(query).tolist()


# ----------------------------
# 검색
# ----------------------------

if len(categories) == 0:

    print("\n카테고리를 찾지 못했습니다.")
    print("전체 데이터에서 검색합니다.\n")

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=5

    )

else:

    category = ",".join(categories)

    print(f"\n'{category}' 카테고리에서 검색합니다.\n")

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=5,

        where={
            "category": category
        }

    )


# ----------------------------
# 출력
# ----------------------------

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


print("="*60)
print("검색 결과")
print("="*60)

THRESHOLD = 0.35

for i in range(len(documents)):

    print(f"\n[{i+1}]")

    print("문장 :", documents[i])

    print("카테고리 :", metadatas[i]["category"])

    print("거리 :", round(distances[i],4))