import mimetypes
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_image(image_path):

    mime_type, _ = mimetypes.guess_type(image_path)

    with open(image_path, "rb") as f:
        image_data = f.read()

    image_part = types.Part.from_bytes(
        data=image_data,
        mime_type=mime_type
    )

    # 최대 3번 재시도
    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model="gemini-3.5-flash",

                contents=[
                    """
                    당신은 학교 온보딩 챗봇의 관리자입니다.

                    이 사진을 학교 안내용 데이터베이스에 저장하기 위한 설명으로 작성하세요.

                    규칙
                    1. 사진 속 시설의 이름을 먼저 설명한다.
                    2. 시설의 용도와 특징을 설명한다.
                    3. 학생이 질문했을 때 검색될 수 있도록 핵심 키워드를 포함한다.
                    4. 불필요한 수식어나 광고 문구는 쓰지 않는다.
                    5. 3~6문장 정도로 작성한다.
                    """,
                    image_part
                ]

            )

            return response.text

        except ServerError:

            print(f"Gemini 서버 혼잡... ({attempt+1}/3)")

            time.sleep(5)

        except Exception as e:

            print(e)

            return f"사진 설명 생성 실패 : {e}"

    return "사진 설명 생성 실패 (Gemini 서버가 응답하지 않았습니다.)"


if __name__ == "__main__":

    print(analyze_image("photos/test.jpg"))