# 문의하기 inquire.py 에서 고객 문의 받은 리스트 받기

import streamlit as st
import pandas as pd
import os

def admin_page():
    st.title("📋 문의 리스트 확인")

    if os.path.exists("inquiries.csv"):
        df = pd.read_csv("inquiries.csv")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("❗ 아직 접수된 문의가 없습니다.")


def inquiry_page():
    st.title("📨 문의하기")

    with st.form("contact_form"):
        name = st.text_input("이름")
        email = st.text_input("이메일")
        message = st.text_area("문의 내용")

        submitted = st.form_submit_button("제출하기")

        if submitted:
            if name and email and message:
                data = {
                    "시간": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                    "이름": [name],
                    "이메일": [email],
                    "문의내용": [message],
                }

                df = pd.DataFrame(data)

                # 파일 없으면 생성, 있으면 append
                if not os.path.exists("inquiries.csv"):
                    df.to_csv("inquiries.csv", index=False)
                else:
                    df.to_csv("inquiries.csv", mode="a", header=False, index=False)

                st.success("문의가 접수되었습니다! 📩")
            else:
                st.warning("모든 항목을 입력해주세요.")
