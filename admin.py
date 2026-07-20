import sqlite3
import os
from datetime import datetime

import streamlit as st

from vector_store import add_document

from image_processor import analyze_image

from pdf_processor import process_pdf

def save_information(
    category,
    sentence,
    image_path=None,
    pdf_path=None,
    image_description = None
):
    add_document(
        doc_id=f"image_{datetime.now().timestamp()}",
        sentence=image_description,
        category=category,
        source="image",
        image_path=image_path
    )

    conn = sqlite3.connect("onboarding.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO classified_data
        (
            question,
            sentence,
            categories,
            keywords,
            status,
            created_at,
            source,
            image_path,
            pdf_path
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,

    (
        "관리자 입력",
        sentence,
        category,
        "",
        "단일분류",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "teacher",
        image_path,
        pdf_path
    ))

    conn.commit()

    # 새로 생성된 id
    doc_id = cursor.lastrowid

    conn.close()

    # ChromaDB에도 저장
    # 텍스트가 있을 때만 ChromaDB 저장
    if sentence.strip():

        add_document(
            doc_id=doc_id,
            sentence=sentence,
            category=category,
            image_path=image_path,
            pdf_path=pdf_path
        )
    
    if image_description:

        add_document(
            doc_id=f"image_{doc_id}",
            sentence=image_description,
            category=category,
            source="image",
            image_path=image_path
        )


def admin_page():

    st.title("👨‍🏫 관리자 페이지")

    st.write("학교 정보를 추가할 수 있습니다.")

    st.divider()

    category = st.selectbox(

        "카테고리",

        [

            "공부법",
            "과목정보",
            "급식",
            "기숙사",
            "동아리",
            "선생님정보",
            "시설",
            "시험수업",
            "진학",
            "학교생활"

        ]

    )

    sentence = st.text_area(

        "추가할 정보",

        height=150

    )

    image = st.file_uploader(

        "📷 사진 업로드",

        type=["png", "jpg", "jpeg"]

    )

    pdf = st.file_uploader(

        "📄 PDF 업로드",

        type=["pdf"]

    )

    if st.button("저장"):

    # 아무것도 입력하지 않은 경우만 막기
        if (
            sentence.strip() == ""
            and image is None
            and pdf is None
        ):

            st.warning("텍스트, 사진 또는 PDF 중 하나 이상을 입력하세요.")

        else:

            image_path = None
            pdf_path = None

            os.makedirs("photos", exist_ok=True)
            os.makedirs("pdfs", exist_ok=True)

        # ------------------------
        # 사진 저장
        # ------------------------
            if image:

                image_path = os.path.join(
                    "photos",
                    image.name
                )

                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            if image_path:

                print("사진 분석 시작")

                image_description = analyze_image(image_path)

                print(image_description)

        # ------------------------
        # PDF 저장
        # ------------------------
            if pdf:

                pdf_path = os.path.join(
                    "pdfs",
                    pdf.name
                )

                with open(pdf_path, "wb") as f:
                    f.write(pdf.getbuffer())

        # ------------------------
        # 텍스트가 없으면 빈 문자열 저장
        # ------------------------
            save_information(

                category=category,

                sentence=sentence.strip(),

                image_path=image_path,

                pdf_path=pdf_path,

                image_description=image_description

            )
        # ------------------------
        # PDF 벡터화
        # ------------------------
            if pdf_path:

                print("process_pdf 호출 직전")

                process_pdf(

                    pdf_path=pdf_path,

                    category=category

                )

            st.success("저장되었습니다.")