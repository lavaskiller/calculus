import pandas as pd
import numpy as np
from datetime import datetime
from pytz import timezone


# 값을 받아 숫자이면 참, 숫자가 아니면 거짓을 반환
def is_numberic(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# 경로를 받아 편리한 데이터 분석을 위해 pandas로
def mk_data(root):
    data = pd.read_table(root, names=["num", "class", "id", "grade"], sep=" ")
    return data


# 서버 로그에서 연산횟수를 추출
def visit():
    # 해당 함수의 코드는 비공개입니다.
    return 0


# 순서대로 분석을 진행할 데이터셋, 원점수, 미응시자 포함 여부, 전체/분반 기준인지를 입력받아 분석결과를 반환
def analysis(data, my_grade, abc, ran):
    overall_grade = np.array([])
    n_of_90, n_of_100, n_of_test, n_of_absence = 0, 0, 0, 0

    # overall_grade
    for i in data["grade"]:
        if pd.isna(i):  # nan 값 평균으로 처리
            n_of_100 += 1
        elif not is_numberic(i):  # 기말 대체의 경우 평균값 * 반영비율로 추가
            if i[-3] == "9":
                n_of_90 += 1
            elif i[-3] == "0":
                n_of_100 += 1

            if i[-3] == "미":  # 미응시 처리
                if abc == "abc":  # 미응시자 계산 결과에 포함하지 않음
                    if ran == "all":
                        n_of_absence += 1
                    continue

                overall_grade = np.append(overall_grade, np.array([0]))
                if ran == "all":
                    n_of_absence += 1
            # else:
            #     if ran == "all":
            #         # 처리할 수 없는 데이터를 보임 -> 코드를 작성하며 예외처리를 위함
            #         print("Invalid data exists. Ignored data. This might make result incorrect!\a", i)
        else:
            overall_grade = np.append(overall_grade, np.array([float(i)]))
            n_of_test += 1

    # 평균값으로 비정규 데이터 처리 (중간고사 데이터셋만 있는 경우)
    overall_mean = np.mean(overall_grade)
    for i in range(n_of_90):
        overall_grade = np.append(overall_grade, np.array([overall_mean * 0.9]))
    for i in range(n_of_100):
        overall_grade = np.append(overall_grade, np.array([overall_mean]))

    overall_mean = np.mean(overall_grade)

    std_deviation = np.std(overall_grade)  # 표준편차 산출
    # print("std_deviation: ",std_deviation)

    z_score = 10 * ((my_grade - overall_mean) / std_deviation) + 50  # z점수 산출
    # print("z_score: ", z_score)

    z_overall_grade = np.array([])

    # 표준 점수로 변환 (t score 사용)
    for i in overall_grade:
        z_overall_grade = np.append(
            z_overall_grade, np.array([10 * ((i - overall_mean) / std_deviation) + 50])
        )

    z_overall_grade = np.sort(z_overall_grade)  # 정렬

    total = z_overall_grade.size
    lower = 0
    same = 0

    for i in z_overall_grade:
        if i < z_score:
            lower += 1
        elif i == z_score:
            same += 1
        else:
            break

    my_pse = round((lower + same / 2) / total * 100, 2)  # 백분위

    # 전체 기준 분석에서는 추가적으로 응시인원과 미응시 인원을 반환
    if ran == "all":
        return (
            overall_grade,
            n_of_test,
            n_of_absence,
            overall_mean,
            std_deviation,
            total,
            lower,
            same,
            my_pse,
        )
    elif ran == "class":
        return overall_grade, overall_mean, std_deviation, lower, same, my_pse


# 가장 핵심이 되는 함수. 분반, 학번 뒷4자리, ip 주소, DB경로, 미응시자 포함 여부, 로그 기록 여부를 받아 클라이언트에게 보이기 위한 값들 반환받음
def calc(inp_cls, inp_id, ipad, root, abc, q):
    data = mk_data(root)

    inp_cls = int(inp_cls)  # 앞에 0을 입력하였을 경우 제거

    inp_cls = str(inp_cls)
    inp_id = str(inp_id)

    # 한자리 숫자일 경우 앞에 0을 붙여줌
    if len(inp_cls) == 1:
        inp_cls = "0" + inp_cls

    # 분반과 학번 뒷4자리가 일치하는 데이터 추출
    find_me = data.loc[
        (data["class"] == "AMTH1009-" + inp_cls) & (data["id"] == inp_id)
    ]

    # 분반이 일치하는 데이터 추출
    class_data = data.loc[(data["class"] == "AMTH1009-" + inp_cls)]

    my_grade = -10

    # if 케이스를 위한 구현 (77로 시작할 때 if문 만족)
    if int(inp_id) // 100 == 77:
        my_grade = int(inp_id) % 100
        if my_grade > 80:
            my_grade = -10

    # 찾은 내 점수가 숫자이면 my_grade에 원점수 할당
    for i in find_me["grade"]:
        if is_numberic(i):
            my_grade = float(i)

    # 올바른 조건을 만족하는 원점수를 찾지 못했을 경우
    if my_grade == -10:
        return (
            "미응시자 입니다.",
            0,
            -1,
            [1720, 51, 1576, 144],
            ["-", "-", "-", "-"],
            ["-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-"],
            q,
        )

    # 전체 기준 분석
    (
        overall_grade,
        n_of_test,
        n_of_absence,
        overall_mean,
        std_deviation,
        total,
        lower,
        same,
        my_pse,
    ) = analysis(data, my_grade, abc, "all")

    # 분반 기준 분석
    class_grade, class_mean, c_std_deviation, c_lower, c_same, my_cpse = analysis(
        class_data, my_grade, abc, "class"
    )

    # 분석 결과를 정렬하기 (이후 특정 %에 있는 점수 추출을 위함)
    overall_grade.sort()
    class_grade.sort()

    # 파라미터로 받은 q가 참이면 로그를 기록함
    if q:
        now = datetime.now(timezone("Asia/Seoul"))
        # 클라이언트의 이상행동 감지 및 대응을 위한 로그 축적하는 코드
        # 서버가 계산한 횟수를 카운팅 하기 위한 관련 코드
        # 로그를 축적하는 부분은 비공개입니다

    # sayings.txt의 첫번째 줄은 웹 결과조회 화면에서 보이고 두번째 줄부터 계산 수식 상세보기를 누른 경우 출력
    log_f = open("sayings.txt", "r", encoding="utf-8")
    buf = log_f.readlines()
    log = buf[0]
    logs = ""
    for i in buf:
        if i == buf[0]:
            continue
        logs += i

    log_f.close()

    # if 케이스인 경우 sayings.txt와 별개로 특정 멘트 출력
    if int(inp_cls) == 0 and int(inp_id) // 100 == 77:
        log = """<p style="color:red">이 결과는 실제 존재하지 않는 예시입니다. 계산에는 포함되지 않습니다.</p>"""

    # 총원(전체인원), 00분반 총원, 응시 인원, 미응시 인원
    info = [int(data.size / 4), int(class_data.size / 4), n_of_test, n_of_absence]

    # 원점수, 등수, 동점자, 백분위
    datas = [
        round(my_grade, 2),
        int(overall_grade.size - (lower + same / 2)) + 1,
        same,
        round(my_pse, 1),
    ]

    # 평균, 표준편차, 80%에 위치하는 점수, 50%에 위치하는 점수, 20%에 위치하는 점수
    datas2 = [
        round(overall_mean, 2),
        round(std_deviation, 2),
        overall_grade[int(total * 0.8)],
        overall_grade[int(total * 0.5)],
        overall_grade[int(total * 0.2)],
    ]

    # 분반기준 => 등수, 동점자, 백분위, 평균, 표준편차
    seps = [
        int(class_grade.size - (c_lower + c_same / 2)) + 1,
        c_same,
        round(my_cpse, 1),
        round(class_mean, 2),
        round(c_std_deviation, 2),
    ]

    # 예시 반환값 확인시 로그 때문에 가독성이 떨어질 경우 아래 주석을 활용할 것
    # return inp_cls, info, datas, datas2, seps, q
    return log, logs, inp_cls, info, datas, datas2, seps, q


# 예시 반환값 확인

# print(
#     calc(
#         "01",
#         "7749",
#         "ip 주소",
#         "C:/Users/lavaskiller/Desktop/Python Workspace/calculus/grade.txt",
#         "abc",
#         False,
#     ),
#     calc(
#         "01",
#         "7749",
#         "ip 주소",
#         "C:/Users/lavaskiller/Desktop/Python Workspace/calculus/grade2.txt",
#         "abc",
#         False,
#     ),
#     calc(
#         "01",
#         "7749",
#         "ip 주소",
#         "C:/Users/lavaskiller/Desktop/Python Workspace/calculus/final.txt",
#         "abc",
#         False,
#     ),
#     sep="\n",
# )
