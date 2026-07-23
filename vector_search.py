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

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("onboarding")


def search_documents(query, n_results=8):

    # -----------------------------
    # 질문 분류
    # -----------------------------
    result = classify_text(query)

    categories = result["categories"]

    query_embedding = model.encode(query).tolist()

    # =============================
    # 일반 검색 (학생 + 관리자)
    # =============================
    if len(categories) > 0:

        normal_results = collection.query(

            query_embeddings=[query_embedding],

            where={
                "category": categories[0]
            },

            n_results=n_results

        )

    else:

        normal_results = collection.query(

            query_embeddings=[query_embedding],

            n_results=n_results

        )

    # =============================
    # PDF만 따로 검색
    # =============================
    if len(categories) > 0:

        pdf_results = collection.query(

            query_embeddings=[query_embedding],

            where={
                "$and": [
                    {"category": categories[0]},
                    {"source": "pdf"}
                ]
            },

            n_results=3

        )

    else:

        pdf_results = collection.query(

            query_embeddings=[query_embedding],

            where={
                "source": "pdf"
            },

            n_results=3

        )

    # =============================
    # 결과 합치기 (중복 제거)
    # =============================
    searched = []
    seen = set()

    def append_results(results):

        if len(results["documents"]) == 0:
            return

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(documents, metadatas, distances):

            key = (doc, meta.get("source"))

            if key in seen:
                continue

            seen.add(key)

            searched.append({

                "document": doc,

                "category": meta["category"],

                "distance": float(dist),

                "image_path": meta.get("image_path"),

                "pdf_path": meta.get("pdf_path"),

                "source": meta.get("source")

            })

    append_results(pdf_results)      # PDF 먼저 추가
    append_results(normal_results)   # 일반 검색 추가

    # =============================
    # 디버깅 출력
    # =============================
    print("\n=== 검색 결과 ===\n")

    for item in searched:

        print(item["document"])
        print(item["source"])
        print(item["pdf_path"])
        print(item["image_path"])
        print(item["distance"])
        print("----------------")

    return categories, searched

    return categories, searched


if __name__ == "__main__":

    query = input("질문을 입력하세요 : ")

    print("=" * 50)
    print("ChromaDB 전체 문서")
    print("=" * 50)

    results = collection.get()

    for doc, meta in zip(results["documents"], results["metadatas"]):
        print(doc)
        print(meta)
        print("-" * 40)

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
        print("거리 :", round(doc["distance"], 4))
        print("-" * 50)