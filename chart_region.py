# 지역별 거래 통계 TOP5 (주석처리 부분 folium 라이브러리 안되어서 못함)
import streamlit as st
import pandas as pd
from PIL import Image

def chart_region(data):
    df = pd.DataFrame(data)
    
    # 🔥 필수 컬럼 확인 (경고문 없이 조용히 종료)
    required_cols = ['address', 'cnt', 'percent']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.write("")
        return  # 조용히 종료
    
    # 🔥 데이터 타입 변환
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df['percent'] = pd.to_numeric(df['percent'], errors='coerce')
    
    # 🔥 NaN 제거
    df = df.dropna(subset=['address', 'cnt', 'percent'])
    
    # 🔥 빈 데이터 체크 (조용히 종료)
    if df.empty:
        st.write("")
        return

    # 1. 제목 (작게 + 볼드 + 아래 여백 최소화)
    st.markdown('<p style="font-size:14px; font-weight:bold; margin-bottom:0px;">지역별 거래 통계 TOP5</p>', unsafe_allow_html=True)

    # 2. 구분선 (위아래 여백 최소화)
    st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)

    col1, col2 = st.columns([1,2]) 
    with col1 :
        st.image("images/map.png", width=150)

    with col2 :
        for idx, row in df.iterrows():
            st.markdown(
                f"<p style='font-size:14px; margin:2px 0;'><b>{row['address']}</b> : {int(row['cnt'])}건 ({int(row['percent'])}%)</p>",
                unsafe_allow_html=True
            )