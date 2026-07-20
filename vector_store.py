import chromadb
from sentence_transformers import SentenceTransformer
from embedding_model import model

# -----------------------------
# 모델 로드
# -----------------------------
print("Vector Store 모델 로드 중...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Vector Store 모델 로드 완료")


# -----------------------------
# ChromaDB 연결
# -----------------------------
client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "onboarding"
)


# -----------------------------
# 문서 추가
# -----------------------------
def add_document(
    doc_id,
    sentence,
    category,
    source="survey",
    image_path=None,
    pdf_path=None
):

    embedding = model.encode(sentence).tolist()

    metadata = {

        "category": category,

        "source": source

    }

    # 사진이 있으면 저장
    if image_path is not None:

        metadata["image_path"] = image_path

    # PDF가 있으면 저장
    if pdf_path is not None:

        metadata["pdf_path"] = pdf_path

    collection.add(

        ids=[str(doc_id)],

        embeddings=[embedding],

        documents=[sentence],

        metadatas=[metadata]

    )

    print(f"[VectorStore] 추가 완료 : {sentence}")


# -----------------------------
# 테스트
# -----------------------------
if __name__ == "__main__":

    add_document(

        999999,

        "기숙사는 밤 11시에 소등합니다.",

        "기숙사",

        source="teacher"

    )

    print("현재 문서 개수 :", collection.count())