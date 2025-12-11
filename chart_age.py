# 연령별 거래 통계 막대그래프
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

def chart_age(data):
    rcParams['font.family'] = 'Malgun Gothic'
    rcParams['axes.unicode_minus'] = False

    df = pd.DataFrame(data)
    
    # 🔥 필수 컬럼 확인 (경고문 없이 조용히 종료)
    required_cols = ['AGE', 'percent']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.write("")
        return  # 조용히 종료
    
    # 🔥 데이터 타입 변환
    df['percent'] = pd.to_numeric(df['percent'], errors='coerce')
    
    # 🔥 NaN 제거
    df = df.dropna(subset=['AGE', 'percent'])
    
    # 🔥 빈 데이터 체크 (조용히 종료)
    if df.empty:
        st.write("")
        return
    
    # rn 컬럼이 있으면 정렬
    if 'rn' in df.columns:
        df = df.sort_values('rn')

    # 1. 제목 (작게 + 볼드 + 아래 여백 최소화)
    st.markdown('<p style="font-size:14px; font-weight:bold; margin-bottom:0px;">연령별 거래 통계</p>', unsafe_allow_html=True)

    # 2. 구분선 (위아래 여백 최소화)
    st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(7,3))  # 크기 조정
    
    colors = ['#1f77b4', '#4fa3e3', '#2c7bb6', '#a6cee3', '#70b0e0']

    bars = ax.bar(
        range(len(df)),
        df['percent'],
        color=colors[:len(df)],
        edgecolor=None,
        width=0.6,
        zorder=2
    )

    # 막대 안 퍼센트 레이블 (위쪽)
    for bar, pct in zip(bars, df['percent']):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,  # 막대 위쪽
            f"{pct}%",
            ha='center',
            va='bottom',
            fontsize=14,
            fontweight='bold'
        )

    # 가로 눈금선
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=1)

    # 테두리 제거 (가로축 제외)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # y축 눈금 숨기기
    ax.set_yticks([10, 20, 30, 40, 50, 60])
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)

    # x축 눈금 설정
    ax.set_xticks(range(len(df)))          # ✔ 눈금 위치 지정
    ax.set_xticklabels(df['AGE'])          # ✔ 해당 위치 레이블 설정

    return st.pyplot(fig)
