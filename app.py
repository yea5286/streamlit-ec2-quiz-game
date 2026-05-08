import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="streamlit quiz",
    layout="centered"
)


USER_ID = "ossstudent"
USER_PW = "2026"


if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "selected_line" not in st.session_state:
    st.session_state.selected_line = None

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "is_correct" not in st.session_state:
    st.session_state.is_correct = None



@st.cache_data
def load_quiz_data():
    quiz_data = {
        "1호선": [
            {
                "question": "1호선 인천행일 때, 동묘앞역 다음 정거장은 동대문역이다.",
                "answer": True,
                "explanation": "인천행 방향에서 동묘앞역 다음 정거장은 동대문역이다."
            },
            {
                "question": "1호선 광운대행일 때, 금정역 다음 정거장은 군포역이다.",
                "answer": False,
                "explanation": "광운대행 방향에서 금정역 다음 정거장은 명학역이다."
            },
            {
                "question": "1호선 서동탄행일 때, 화서역 다음 정거장은 수원역이다.",
                "answer": True,
                "explanation": "서동탄행 방향에서 화서역 다음 정거장은 수원역이다."
            }
        ],
        "4호선": [
            {
                "question": "4호선 오이도행일 때, 중앙역 다음 정거장은 고잔역이다.",
                "answer": True,
                "explanation": "오이도행 방향에서 중앙역 다음 정거장은 고잔역이다."
            },
            {
                "question": "4호선 당고개행일 때, 사당역 다음 정거장은 남태령역이다.",
                "answer": False,
                "explanation": "당고개행 방향에서 사당역 다음 정거장은 총신대입구(이수)역이다."
            },
            {
                "question": "4호선 사당행일 때, 삼각지역 다음 정거장은 신용산역이다.",
                "answer": True,
                "explanation": "사당행 방향에서 삼각지역 다음 정거장은 신용산역이다."
            }
        ],
        "6호선": [
            {
                "question": "6호선 봉화산행일 때, 돌곶이역 다음 정거장은 석계역이다.",
                "answer": True,
                "explanation": "봉화산행 방향에서 돌곶이역 다음 정거장은 석계역이다."
            },
            {
                "question": "6호선 응암행일 때, 이태원역 다음 정거장은 한강진역이다.",
                "answer": False,
                "explanation": "응암행 방향에서 이태원역 다음 정거장은 녹사평역이다."
            },
            {
                "question": "6호선 대흥행일 때, 삼각지역 다음 정거장은 효창공원앞역이다.",
                "answer": True,
                "explanation": "대흥행 방향에서 삼각지역 다음 정거장은 효창공원앞역이다."
            }
        ]
    }

    return quiz_data


def reset_quiz():
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.is_correct = None


if not st.session_state.login:

    st.title("지하철 정거장 맞추기 퀴즈게임")

    st.subheader("1호선, 4호선, 6호선")

    st.info("학번: 2023204055 / 이름: 이예준")

    st.write("간단한 지하철 역 참, 거짓 퀴즈입니다.")

    st.markdown("---")
    st.header("로그인")

    with st.form("login_form"):
        input_id = st.text_input("아이디")
        input_pw = st.text_input("비밀번호", type="password")

        login_button = st.form_submit_button("로그인")

    if login_button:
        if input_id == USER_ID and input_pw == USER_PW:
            st.session_state.login = True
            st.session_state.username = input_id
            st.rerun()
        else:
            st.error("로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다.")


# 로그인 성공 후 화면
else:
    st.success("로그인 성공, "f"{st.session_state.username}님, 환영합니다.")

    st.title("지하철 정거장 맞추기 퀴즈게임")

    # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.selected_line = None
        reset_quiz()
        st.rerun()

    st.markdown("---")

    # 캐싱된 퀴즈 데이터 불러오기
    quiz_data = load_quiz_data()

    st.header("호선 선택")

    st.write("퀴즈를 풀 호선을 선택하세요.")

    # 호선 선택 버튼
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("1호선"):
            st.session_state.selected_line = "1호선"
            reset_quiz()
            st.rerun()

    with col2:
        if st.button("4호선"):
            st.session_state.selected_line = "4호선"
            reset_quiz()
            st.rerun()

    with col3:
        if st.button("6호선"):
            st.session_state.selected_line = "6호선"
            reset_quiz()
            st.rerun()


    st.markdown("---")

    if st.session_state.selected_line is None:
        st.warning("먼저 퀴즈를 풀 호선을 선택하세요.")

    else:
        selected_line = st.session_state.selected_line
        questions = quiz_data[selected_line]
        total_questions = len(questions)

        st.header(f"{selected_line} 퀴즈")

        if st.session_state.question_index >= total_questions:
            st.subheader("최종 결과")

            st.success(
                f"총 {total_questions}문제 중 {st.session_state.score}문제를 맞췄습니다."
            )

            result_df = pd.DataFrame({
                "구분": ["정답", "오답"],
                "개수": [
                    st.session_state.score,
                    total_questions - st.session_state.score
                ]
            })

            st.dataframe(result_df, use_container_width=True)

            fig = px.bar(
                result_df,
                x="구분",
                y="개수",
                title="퀴즈 결과"
            )

            st.plotly_chart(fig, use_container_width=True)

            if st.button("다시 풀기"):
                reset_quiz()
                st.rerun()

        else:
            current_question = questions[st.session_state.question_index]

            st.write(
                f"문제 {st.session_state.question_index + 1} / {total_questions}"
            )

            st.subheader(current_question["question"])

            user_answer = st.radio(
                "정답을 선택하세요.",
                ["참", "거짓"],
                key=f"answer_{selected_line}_{st.session_state.question_index}"
            )

            if not st.session_state.answered:
                if st.button("정답 확인"):
                    if user_answer == "참":
                        user_answer_bool = True
                    else:
                        user_answer_bool = False

                    if user_answer_bool == current_question["answer"]:
                        st.session_state.score += 1
                        st.session_state.is_correct = True
                    else:
                        st.session_state.is_correct = False

                    st.session_state.answered = True
                    st.rerun()

            else:
                if st.session_state.is_correct:
                    st.success("정답입니다.")
                else:
                    st.error("오답입니다.")

                st.write(current_question["explanation"])

                st.write(
                    f"현재 점수: {st.session_state.score} / {total_questions}"
                )

                if st.button("다음 문제"):
                    st.session_state.question_index += 1
                    st.session_state.answered = False
                    st.session_state.is_correct = None
                    st.rerun()