import chromadb
from sentence_transformers import SentenceTransformer

from classifier import classify_text


model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("onboarding")


def search_documents(query):

    result = classify_text(query)

    categories = result["categories"]

    query_embedding = model.encode(query).tolist()

    if len(categories) > 0:

        results = collection.query(

            query_embeddings=[query_embedding],

            where={
                "category": categories[0]
            },

            n_results=5

        )

    else:

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=5

        )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    THRESHOLD = 0.5

    searched = []

    for doc, meta, dist in zip(documents, metadatas, distances):

        if dist > THRESHOLD:
            continue

        searched.append({

            "document": doc,

            "category": meta["category"],

            "distance": float(dist)

        })

    return searched


if __name__ == "__main__":

    query = input("질문 : ")

    docs = search_documents(query)

    for doc in docs:

        print(doc)