import chromadb
from sentence_transformers import SentenceTransformer

from embedding import model

from classifier import classify_text

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("onboarding")


def add_document(doc_id, sentence, category):

    embedding = model.encode(sentence).tolist()

    collection.add(

        ids=[str(doc_id)],

        embeddings=[embedding],

        documents=[sentence],

        metadatas=[

            {
                "category": category
            }

        ]

    )

print("모델 불러오는 중...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("모델 로드 완료")


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("onboarding")


def search_documents(query, n_results=8):

    # -----------------------------
    # 질문 분류
    # -----------------------------
    result = classify_text(query)

    categories = result["categories"]

    query_embedding = model.encode(query).tolist()

    # -----------------------------
    # Hybrid Search
    # -----------------------------
    if len(categories) > 0:

        results = collection.query(

            query_embeddings=[query_embedding],

            where={
                "category": categories[0]
            },

            n_results=n_results

        )

    else:

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=n_results

        )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # -----------------------------
    # 디버깅 출력
    # -----------------------------
    print("\n=== 전체 검색 결과 ===\n")

    for doc, meta, dist in zip(documents, metadatas, distances):

        print(doc)
        print(meta)
        print(round(dist, 4))
        print("----------------")

    # -----------------------------
    # Threshold 없이 모두 반환
    # -----------------------------
    searched = []

    for doc, meta, dist in zip(documents, metadatas, distances):

        searched.append({

    "document": doc,

    "category": meta["category"],

    "distance": float(dist),

    "image_path": meta.get("image_path"),

    "pdf_path": meta.get("pdf_path"),

    "source": meta.get("source")

})

    return categories, searched


if __name__ == "__main__":

    query = input("질문을 입력하세요 : ")

    categories, docs = search_documents(query)

    print("\n예상 카테고리 :", categories)

    print("\n검색 결과\n")

    for i, doc in enumerate(docs, start=1):

        print(f"[{i}]")

        print("문장 :", doc["document"])

        print("카테고리 :", doc["category"])

        print("출처 :", doc["source"])

        print("사진 :", doc["image_path"])

        print("PDF :", doc["pdf_path"])

        print("거리 :", round(doc["distance"],4))
        
        print("-" * 50)