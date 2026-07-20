import pandas as pd

from classifier import classify_text
from preprocessing import split_response
from database import save_result

# 설문 읽기
df = pd.read_excel("survey.xlsx")


print("=" * 60)
print("설문 문항 목록")
print("=" * 60)

for i, column in enumerate(df.columns):
    print(f"{i}. {column}")

print()

selected = int(input("분류할 열 번호를 입력하세요 : "))

question = df.columns[selected]


print("\n===== 자동 분류 시작 =====\n")


# ------------------------
# 통계 저장용
# ------------------------

category_count = {}

unclassified = []


# ------------------------
# 응답 처리
# ------------------------

for value in df.iloc[:, selected]:

    if pd.isna(value):
        continue

    items = split_response(str(value))

    for item in items:

        result = classify_text(item)
        save_result(question, result)

        print("=" * 60)
        print("문장 :", result["text"])
        print("분류 :", result["categories"])
        print("상태 :", result["status"])

        # ------------------------
        # 통계
        # ------------------------

        if result["status"] == "미분류":

            unclassified.append(result["text"])

        else:

            for category in result["categories"]:

                category_count[category] = category_count.get(category, 0) + 1


# ------------------------
# 결과 출력
# ------------------------

print("\n\n")
print("=" * 60)
print("분류 통계")
print("=" * 60)

for category, count in sorted(category_count.items()):

    print(f"{category} : {count}")

print(f"\n미분류 : {len(unclassified)}개")


print("\n")
print("=" * 60)
print("미분류 목록")
print("=" * 60)

for i, text in enumerate(unclassified, start=1):

    print(f"{i}. {text}")