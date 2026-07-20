import os
import streamlit as st
from dotenv import load_dotenv
from chatbot import ask_chatbot
from admin import admin_page
load_dotenv()
# ---------------------------------------
# 페이지 설정
# ---------------------------------------
menu = st.sidebar.radio(
    "메뉴",
    [
        "학생 챗봇",
        "관리자"
    ]
)
if menu =="학생 챗봇":
    st.set_page_config(
    page_title="AI 온보딩 챗봇",
    page_icon="🎓",
    layout="wide"
)
st.title("🎓 고등학교 AI 온보딩 챗봇")
st.write(
    "신입생이 학교생활에 대해 질문하면 설문 데이터를 기반으로 AI가 답변합니다."
)
# ---------------------------------------
# 대화 저장
# ---------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
# --------------------------------------
# 입
# ---------------------------------------
question = st.chat_input("궁금한 것을 질문하세요.")
if question:
    # 사용자 출력
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    with st.chat_message("user"):
        st.markdown(question)
    # AI 답변 생성
    with st.spinner("답변 생성 중..."):
        result = ask_chatbot(question)
    answer = result["answer"]

    categories = result["categories"]

    documents = result["documents"]

    image_paths = result["image_paths"]
    # AI 출력
    with st.chat_message("assistant"):
        st.markdown(answer)

        # ------------------------
        # 관련 사진 표시
        # ------------------------

        if len(image_paths) > 0:

            st.subheader("🖼️ 관련 사진")

            shown = set()

            for path in image_paths:

                if path in shown:
                    continue

                shown.add(path)

                if os.path.exists(path):

                    st.image(
                        path,
                        use_container_width=True
                        )

            st.divider()

        st.divider()
        st.subheader("🏷️ 예상 카테고리")
        if len(categories) == 0:



            st.write("없음")



        else:



            st.write(", ".join(categories))



        st.subheader("📚 참고한 설문")



        if len(documents) == 0:



            st.write("검색 결과 없음")



        else:



            for i, doc in enumerate(documents, start=1):



                with st.expander(f"{i}. {doc['category']}"):



                    st.write(doc["document"])



                    if doc.get("source") == "teacher":

                         st.success("👨‍🏫 관리자 정보")



                    else:

                         st.info("📝 설문 데이터")



                    if doc.get("image_path"):



                        st.image(

                            doc["image_path"],

                            use_container_width=True

                         )



                    if doc.get("pdf_path"):



                        with open(doc["pdf_path"], "rb") as file:



                            st.download_button(



                                "📄 PDF 다운로드",



                                file,



                                file_name=doc["pdf_path"].split("/")[-1]



                            )



                    st.caption(

                        f"유사도 거리 : {doc['distance']:.4f}"

                    )



    st.session_state.messages.append(



        {
            "role": "assistant",
            "content": answer
        }
    )

elif menu=="관리자":



    st.title("🔒 관리자 로그인")

    admin_id = st.text_input(
        "아이디"
    )

    admin_pw = st.text_input(
        "비밀번호",
        type="password"
    )

    if st.button("로그인"):

        if (
            admin_id == os.getenv("ADMIN_ID")
            and
            admin_pw == os.getenv("ADMIN_PASSWORD")
        ):

            st.session_state["admin_login"] = True

            st.success("로그인 성공!")

        else:

            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    if st.session_state.get("admin_login", False):

        admin_page()