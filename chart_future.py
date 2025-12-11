import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import numpy as np
import math

def chart_future(data, selected_id):
    rcParams['font.family'] = 'Malgun Gothic'
    rcParams['axes.unicode_minus'] = False

    df = pd.DataFrame(data)
    df['trvlDstnc'] = df['trvlDstnc'].astype(int)
    df['gradeUsedCarPrice'] = df['gradeUsedCarPrice'].astype(int)
    df['grade1yearLaterPrice'] = df['grade1yearLaterPrice'].astype(int)
    df['grade2yearLaterPrice'] = df['grade2yearLaterPrice'].astype(int)
    df['grade3yearLaterPrice'] = df['grade3yearLaterPrice'].astype(int)

    # 🔥 선택된 등급으로 필터링
    df_filtered = df[df["carGradeNbr"] == selected_id].copy()
    
    if df_filtered.empty:
        st.warning("선택된 등급에 해당하는 데이터가 없습니다.")
        return

    # 🔥 해당 등급의 주행거리 옵션만 표시
    trvl_options = sorted(df_filtered["trvlDstnc"].unique().tolist())
    
    # 🔥 기본값: 첫 번째 주행거리
    default_trvl = trvl_options[0]
    
    # 변경
    default_trvl = 50000 if 50000 in trvl_options else trvl_options[0]

    # 🔥 session_state로 주행거리 값 관리 (등급 변경 시 초기화)
    state_key = f"trvl_value_{selected_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_trvl
    
    selected_trvl = st.session_state[state_key]

    # 제목 + 구분선
    st.markdown('<p style="font-size:14px; font-weight:bold; margin-bottom:0px;">시세 예측</p>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)

    # 🔥 선택된 등급 + 주행거리 데이터 추출
    row = df_filtered[df_filtered['trvlDstnc'] == selected_trvl].iloc[0]

    years = ['2025', '2026', '2027', '2028']
    prices = [
        row['gradeUsedCarPrice'] // 10000,
        row['grade1yearLaterPrice'] // 10000,
        row['grade2yearLaterPrice'] // 10000,
        row['grade3yearLaterPrice'] // 10000
    ]

    fig, ax = plt.subplots(figsize=(8, 4))

    # 꺾은선 그래프
    ax.plot(years, prices, marker='o', color='crimson', linewidth=2, markersize=8)

    # 값 표시
    for i, price in enumerate(prices):
        ax.text(i, price + 20, f"{price:,}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

    # 음영
    ax.fill_between(years, prices, y2=0, color='lightgrey', alpha=0.3)

    # Grid / 테두리
    ax.grid(True, axis='y', color='gray', linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # 축 자동 설정
    data_min = min(prices)
    data_max = max(prices)
    unit = 200

    y_min = math.floor(data_min / unit) * unit
    y_max = math.ceil(data_max / unit) * unit

    if y_min == y_max:
        y_max = y_min + unit

    ax.set_yticks(np.arange(y_min, y_max + unit, unit))
    ax.set_ylim(y_min, y_max)

    ax.set_xlabel('Year')
    ax.set_ylabel('금액(만원)')

    st.pyplot(fig)
    col_l, col_r = st.columns([1,2])
    with col_l :
        _, col_right = st.columns([0.3,1.7])
        with col_right :
            st.markdown('<p style="font-size:14px; font-weight:bold; margin-bottom:0px; margin-top:8px;">주행거리(Km)</p>', unsafe_allow_html=True)
        
    with col_r :
        col_left, _ = st.columns([1.7,0.3])
        with col_left:
            # 🔽 그래프 아래에 selectbox 배치
            new_trvl = st.selectbox(
                " ",
                trvl_options,
                index=trvl_options.index(selected_trvl),
                key=f"trvl_select_{selected_id}",
                label_visibility="collapsed"  # label 숨기기
            )
            
            # 값이 변경되면 session_state 업데이트 → 페이지 재실행
            if new_trvl != selected_trvl:
                st.session_state[state_key] = new_trvl
                st.rerun()
    st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)