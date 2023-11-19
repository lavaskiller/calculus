import pandas as pd

# 중간고사 & 기말고사 raw data 가져오기
mid = pd.read_csv("sum_data/grade.txt", names=["num", "class", "id", "grade"], sep=" ")
fin = pd.read_csv("sum_data/grade2.txt", names=["num", "class", "id", "grade"], sep=" ")


for index, row in mid.iterrows():
    grade = row["grade"]
    if pd.isna(grade):
        continue
    elif not str(grade).isdigit():
        find_me = fin.loc[(fin["class"] == row["class"]) & (fin["id"] == row["id"])]
        print(find_me["grade"], row["class"], row["id"])

        if find_me["grade"].empty:  # 중간은 있는데 기말은 없는 경우..?
            mid.at[index, "grade"] = -10
            continue

        # 기말 대체의 경우 평균값 * 반영비율로 추가
        if grade[-3] == "9":
            mid.at[index, "grade"] = float(find_me["grade"].iloc[0]) * 0.9
        elif grade[-3] == "0":
            mid.at[index, "grade"] = float(find_me["grade"].iloc[0])
        elif grade[-3] == "미":
            mid.at[index, "grade"] = "미응시"
        else:
            print(
                "Invalid data exists. Ignored data. This might make the result incorrect. => ",
                grade,
            )

for index, row in fin.iterrows():
    grade = row["grade"]

    find_me = mid.loc[(row["class"] == mid["class"]) & (row["id"] == mid["id"])]

    if pd.isna(grade):
        continue
    elif not str(grade).isdigit():
        print(find_me["grade"], row["class"], row["id"])

        if grade[-3] == "미":
            fin.at[index, "grade"] = "미응시"
        else:
            print(
                "Invalid data exists. Ignored data. This might make the result incorrect. => ",
                grade,
            )
    else:
        if find_me["grade"].iloc[0] == "미응시":
            fin.at[index, "grade"] = "미응시"
        else:
            try:
                fin.at[index, "grade"] = float(grade) + float(find_me["grade"].iloc[0])
            except:
                fin.at[index, "grade"] = "미응시"
                print(
                    "Cannot sum these values. This might make the result incorrect. => ",
                    grade,
                    " / ",
                    find_me["grade"].iloc[0],
                )

print(fin)
mid.to_csv("sum_data/grade_update.txt", sep=" ", header=False, index=False)
fin.to_csv("sum_data/final.txt", sep=" ", header=False, index=False)
