import sqlite3
import os
from datetime import datetime

import streamlit as st

from vector_store import add_document

from pdf_processor import process_pdf

def save_information(
    category,
    sentence,
    image_path=None,
    pdf_path=None
):

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
            pdf_path,
            image_description
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        pdf_path,
        None          # 사진 설명은 저장하지 않음
    ))

    conn.commit()

    doc_id = cursor.lastrowid

    conn.close()

    if sentence.strip():

        add_document(
            doc_id=doc_id,
            sentence=sentence,
            category=category,
            source="teacher",
            image_path=image_path,
            pdf_path=pdf_path
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

                pdf_path=pdf_path

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