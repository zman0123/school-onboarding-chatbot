from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

from vector_search import search_documents



# -----------------------
# API Key
# -----------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------
# Gemini 답변 생성
# -----------------------

def ask_chatbot(question):

    # 카테고리 + 검색문서 가져오기
    categories, docs = search_documents(question)

    if len(docs) == 0:

        return {
            "answer": "관련된 정보를 찾지 못했습니다.",
            "categories": categories,
            "documents": []
        }
    
    image_paths = []
    seen = set()

    for doc in docs:

        path = doc.get("image_path")

        if path and path not in seen:

            seen.add(path)

            image_paths.append(path)

    # Gemini에게 전달할 Context 생성
    context = ""

    for i, doc in enumerate(docs, start=1):

        if doc["source"] == "pdf":

            context += (
                f"[학교 규정 PDF]\n"
                f"{doc['document']}\n\n"
            )

        elif doc["source"] == "teacher":

            context += (
                f"[관리자 입력]\n"
                f"{doc['document']}\n\n"
            )

        else:

            context += (
                f"[학생 설문]\n"
                f"{doc['document']}\n\n"
            )

    prompt = f"""
당신의 역할은
학교생활에 대해 쉽고 친절하게 설명하는 것입니다.

당신은 우리 학교를 잘 아는 선배입니다.

신입생이 이해하기 쉽게
친절하게 설명해 주세요.

너무 딱딱한 말투는 사용하지 않습니다.
=====================
참고 자료
=====================

{context}

=====================
학생 질문
=====================

{question}

=====================
답변 규칙
=====================

1.
학교 규정(PDF)이 있으면 가장 우선적으로 사용한다.

2.
관리자 입력 정보가 있으면 두 번째로 참고한다.

3.
학생 설문은 실제 경험 사례로만 참고한다.

4.
자료에 없는 내용은 절대로 추측하지 않는다.

5.
답을 모르면
"현재 제공된 자료에서는 확인되지 않습니다."
라고 답한다.

6.
학생이 이해하기 쉬운 말로 설명한다.

7.
학교 규정을 그대로 복사하지 말고
자연스럽게 요약해서 설명한다.

8.
필요하면
"학교생활 안내 PDF를 참고했습니다."
처럼 출처를 자연스럽게 언급한다.

9.
답변은 3~8문장 정도로 작성한다.

10.
인사말이나 불필요한 문장은 생략하고
질문에 바로 답한다.

여러 자료가 서로 다를 경우

학교 규정(PDF)>관리자 입력>학생 설문

순으로 신뢰한다.

질문이 너무 짧거나 모호하면
답을 추측하지 말고
학생에게 다시 질문한다.
"""

    response = client.models.generate_content(

        model="gemini-3.5-flash",

        contents=prompt,

        config=types.GenerateContentConfig(
            temperature=0.2
        )

    )

    return {

        "answer": response.text,

        "categories": categories,

        "documents": docs,

        "image_paths": image_paths

    }


# -----------------------
# 테스트용
# -----------------------

if __name__ == "__main__":

    question = input("질문 : ")

    result = ask_chatbot(question)

    print("\n" + "=" * 60)
    print("예상 카테고리")
    print("=" * 60)

    if len(result["categories"]) == 0:
        print("없음")
    else:
        print(", ".join(result["categories"]))

    print("\n" + "=" * 60)
    print("참고한 설문")
    print("=" * 60)

    for i, doc in enumerate(result["documents"], start=1):

        print(f"[{i}]")
        print(doc["document"])
        print(f"(카테고리 : {doc['category']})")
        print()

    print("=" * 60)
    print("AI 답변")
    print("=" * 60)
    print(result["answer"])