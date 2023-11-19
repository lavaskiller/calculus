from flask import Flask, request, render_template
from calc import calc, visit

# from rank import prints, find_howmx, prints2, find_howm -> 조회된 학번 수 등을 로그에서 확인하기 위한 함수들이 rank.py에 저장되어 있으나 비공개입니다.

app = Flask(__name__)
app.config["DEBUG"] = True

logs = ""
service = True


@app.route("/", methods=["GET", "POST"])
def adder_page():
    global service
    ipad = request.remote_addr
    errors = ""
    if request.method == "POST" and service:
        number1 = None
        number2 = None
        abc = None

        try:
            number1 = str(request.form["number1"])
        except:
            errors += "<p>{!r} 는 올바른 입력이 아닙니다.</p>\n".format(request.form["number1"])
        try:
            number2 = str(request.form["number2"])
        except:
            errors += "<p>{!r} 는 올바른 입력이 아닙니다.</p>\n".format(request.form["number2"])

        if "abc" in request.form:
            abc = str(request.form["abc"])
        else:
            abc = "not"

        if errors == "":
            if not number1.isdigit():
                errors += "<p>숫자를 입력해주세요.</p>\n"
            elif int(number1) < 0 or int(number1) > 33:
                errors += "<p>분반으로 0이상 33이하의 정수를 입력하여야 합니다.</p>\n"
            elif len(number2) != 4:
                errors += "<p>학번 4자리를 입력하세요. Invalid.</p>\n"

        try:
            number1 = int(number1)
        except ValueError:
            number1 = None

        if (
            number1 is not None
            and number2 is not None
            and int(number1) >= 0
            and int(number1) <= 33
            and len(number2) == 4
        ):
            global logs
            q3, q4, nm3, m_info, m_datas, m_datas2, m_seps, q = calc(
                number1, number2, ipad, "grade.txt", abc, 1
            )
            q1, q2, nm2, f_info, f_datas, f_datas2, f_seps, q = calc(
                number1, number2, ipad, "grade2.txt", abc, q
            )
            log, logs, nm, info, datas, datas2, seps, q = calc(
                number1, number2, ipad, "final.txt", abc, q
            )

            if (nm == -1) & (nm2 == -1) & (nm3 == -1):
                errors += "<p>조회되는 정보가 없습니다. 분반과 학번 마지막 4자리를<br>올바르게 입력하였는지 확인하십시오.</p>\n<p>Failed to load data. Please check your division number and last 4 digit of Student ID.</p>\n"
            else:
                errors = ""
                # all_peos = [find_howmx(), round(find_howmx() / f_info[0] * 100, 2)]
                all_peos = [0, 0]

                return render_template(
                    "result.html",
                    log=log,
                    m_info=m_info,
                    nm=nm,
                    m_datas=m_datas,
                    m_datas2=m_datas2,
                    m_seps=m_seps,
                    f_info=f_info,
                    f_datas=f_datas,
                    f_datas2=f_datas2,
                    f_seps=f_seps,
                    info=info,
                    datas=datas,
                    datas2=datas2,
                    seps=seps,
                    all_peos=all_peos,
                )

    vst = visit()

    if service is False and request.method == "POST":
        errors = "서비스가 종료되었습니다.<br>Service Ended."
    return render_template("main.html", errors=errors, vst=vst)


# 로컬에서 테스트
# if __name__ == "__main__":
#     app.run("0.0.0.0", port=5000, debug=True)


@app.route("/logs")
def start():
    global logs
    return """
        <html>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no", />
            <body style="background-color: #ededed;padding: 7; margin:0 auto;">
                {logs}
            </body>
        </html>
    """.format(
        logs=logs
    )
