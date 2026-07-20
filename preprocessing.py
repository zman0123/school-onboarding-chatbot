import re


def split_response(text):
    """
    하나의 응답을 정보 단위로 분리한다.
    """

    if text is None:
        return []

    text = str(text).strip()

    if text == "":
        return []

    # 줄바꿈 통일
    text = text.replace("\r\n", "\n")

    # 번호 앞에 줄바꿈 추가
    # 예: 1. -> \n1.
    text = re.sub(r'(?<!^)(\d+\.)', r'\n\1', text)

    # 줄바꿈 기준으로만 분리
    parts = text.split("\n")


    result = []

    for part in parts:

        part = part.strip()

        # 앞 번호 제거
        part = re.sub(r'^\d+\.\s*', '', part)

        if part != "":
            result.append(part)

    return result


# ----------------------------
# 테스트 코드
# ----------------------------
if __name__ == "__main__":

    samples = [

        """
1. 시험 수업: 김준만 선생님 기출 위주
2. 기숙사: 세탁기 부족
3. 동아리: 프로그래밍부 추천
""",

        """
선생님, 중국어는 어떻게 하나요
""",

        """
모의 고사 학력평가 학교 생활

기숙사: 세탁기 부족

동아리: 프로그래밍부 추천
""",

        """
선생님, 탁구실이 어딘가요
"""
    ]

    for sample in samples:

        print("=" * 50)
        print("원본")
        print(sample)

        print("\n분리 결과")

        items = split_response(sample)

        for item in items:
            print(item)

        print()