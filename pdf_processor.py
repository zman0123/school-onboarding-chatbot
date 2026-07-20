import fitz
import re
import uuid

from vector_store import add_document


def process_pdf(pdf_path, category):

    """
    PDF를 읽어서 ChromaDB에 저장한다.
    """
    
    print("★★★★★ process_pdf 실행됨 ★★★★★")

    print("=" * 60)
    print("PDF 처리 시작")
    print("=" * 60)

    # -----------------------------
    # PDF 열기
    # -----------------------------
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:

        page_text = page.get_text()

        if page_text.strip():

            text += page_text + "\n"

    doc.close()

    # -----------------------------
    # 공백 정리
    # -----------------------------
    text = re.sub(r"\s+", " ", text)

    # -----------------------------
    # Chunk 생성
    # -----------------------------
    chunk_size = 800

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size].strip()

        if len(chunk) > 50:

            chunks.append(chunk)

    print(f"총 Chunk 수 : {len(chunks)}")

    # -----------------------------
    # ChromaDB 저장
    # -----------------------------
    for chunk in chunks:

        doc_id = str(uuid.uuid4())

        add_document(

            doc_id=doc_id,

            sentence=chunk,

            category=category,

            source="pdf",

            pdf_path=pdf_path

        )

    print(f"{len(chunks)}개의 Chunk 저장 완료")