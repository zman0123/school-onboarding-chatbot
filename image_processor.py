import mimetypes

from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

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

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            "이 사진을 학교 안내용으로 자세히 설명해줘.",
            image_part
        ]
    )

    return response.text


if __name__ == "__main__":

    print(
        analyze_image("photos/test.jpg")
    )