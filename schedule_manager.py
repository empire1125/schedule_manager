import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# 초기 데이터 로드 (지난 스케줄 데이터)
schedule_data = {
    "2024-12": {
        "2": "조서희", "3": "박연희", "4": "김철연", "5": "송재근", "6": "배수연", "7": "김재윤",
        "9": "Michael", "10": "이수정", "11": "홍지인", "12": "서상신", "13": "박가람", "14": "박연희",
        "16": "윤성로", "17": "캠벨", "18": "김재윤", "19": "김제이미", "20": "원서희", "21": "이수정",
        "23": "김종훈", "24": "송재근", "26": "우창호", "27": "남기영", "28": "조화영", "30": "정준호",
        "31": "조서희"
    },
    "2025-1": {
        "1": "서상신", "2": "정준호", "3": "배수연", "4": "서상신", "6": "박가람", "7": "김재윤",
        "8": "정준호", "9": "김제이미", "10": "캠벨", "11": "조화영", "13": "박연희", "14": "원서희",
        "15": "우창호", "16": "김종훈", "17": "남기영", "18": "정준호", "20": "캠벨", "21": "손종현",
        "22": "맷", "23": "조서희", "24": "박가람", "25": "우창호", "27": "조화영", "28": "배수연",
        "29": "김철연", "30": "송재근", "31": "이수정"
    }
}

# 데이터 저장 함수
def save_schedule(data, file_name="schedule_data.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 스케줄 생성 함수
def generate_schedule(month, unavailable, prev_schedule, names):
    year, month_num = map(int, month.split("-"))
    days_in_month = (datetime(year, month_num, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    day_count = days_in_month.day

    # 월~토만 포함
    valid_days = [i for i in range(1, day_count + 1) if datetime(year, month_num, i).weekday() < 6]
    idx = 0

    schedule = {}
    for day in valid_days:
        if str(day) in unavailable:
            idx += 1
            continue
        while names[idx % len(names)] in unavailable.get(str(day), []):
            idx += 1
        schedule[str(day)] = names[idx % len(names)]
        idx += 1

    return schedule

# 인터페이스 설정
st.title("당직 스케줄 관리 시스템")
st.sidebar.header("설정")

# 입력 데이터 받기
month = st.sidebar.text_input("스케줄링할 월 (예: 2025-2)", "2025-2")
names = st.sidebar.text_area("참여 인원 리스트 (줄바꿈으로 구분)").split("\n")
unavailable_days = st.sidebar.text_area("근무 불가능 날짜 (이름:날짜 형식, 예: 조서희:3,4)").split(",")

# 사용자 입력 변환
unavailable = {}
for entry in unavailable_days:
    if ":" in entry:
        name, days = entry.split(":")
        unavailable[name.strip()] = [d.strip() for d in days.split(",")]

# 스케줄 생성
prev_schedule = schedule_data.get("2025-1", {})
schedule = generate_schedule(month, unavailable, prev_schedule, names)

# 스케줄 표시
st.subheader(f"{month} 스케줄")
df_schedule = pd.DataFrame(list(schedule.items()), columns=["날짜", "당직자"])
edited_schedule = st.data_editor(df_schedule, key="current_schedule")

# 이전 두 달 스케줄 표시
st.subheader("이전 두 달 스케줄")
prev_months = ["2024-12", "2025-1"]
for prev_month in prev_months:
    if prev_month in schedule_data:
        st.text(f"{prev_month} 스케줄")
        prev_df = pd.DataFrame(list(schedule_data[prev_month].items()), columns=["날짜", "당직자"])
        edited_prev_df = st.data_editor(prev_df, key=f"prev_{prev_month}")

        # 수정된 데이터를 저장
        if st.button(f"{prev_month} 수정 내용 저장"):
            schedule_data[prev_month] = dict(zip(edited_prev_df["날짜"], edited_prev_df["당직자"]))
            save_schedule(schedule_data)
            st.success(f"{prev_month} 수정 내용이 저장되었습니다!")

# 확정 버튼
if st.button("스케줄 확정"):
    schedule_data[month] = dict(zip(edited_schedule["날짜"], edited_schedule["당직자"]))
    save_schedule(schedule_data)
    st.success("스케줄이 저장되었습니다!")
