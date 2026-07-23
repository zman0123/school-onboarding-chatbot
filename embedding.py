from sentence_transformers import SentenceTransformer

print("모델 로드 중...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("모델 로드 완료")