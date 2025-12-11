import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

def chart_mileage(data):
    rcParams['font.family'] = 'Malgun Gothic'
    rcParams['axes.unicode_minus'] = False

    df = pd.DataFrame(data)
    
    # 🔥 필수 컬럼 확인
    required_cols = ['trvlDstnc', 'CNT', 'avgPrice']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        # st.error(f"필수 컬럼이 없습니다: {missing_cols}")
        st.write("")
        return
    
    # 숫자로 변환 (변환 불가 값은 NaN으로 처리)
    df["trvlDstnc"] = pd.to_numeric(df["trvlDstnc"], errors="coerce")
    df['CNT'] = pd.to_numeric(df['CNT'], errors="coerce")
    df['avgPrice'] = pd.to_numeric(df['avgPrice'], errors="coerce")

    # NaN → 0으로 대체
    df["trvlDstnc"] = df["trvlDstnc"].fillna(0)
    
    # 음수 같은 이상한 값이 있다면 → 0으로 처리
    df.loc[df["trvlDstnc"] < 0, "trvlDstnc"] = 0

    # int 변환
    df["trvlDstnc"] = df["trvlDstnc"].astype(int)
    
    # 🔥 NaN 제거
    df = df.dropna(subset=['CNT', 'avgPrice'])

    # x축 최대값 제한
    df_plot = df[df['trvlDstnc'] <= 30].copy()
    
    # 🔥 데이터 확인
    if df_plot.empty:
        # st.warning("표시할 데이터가 없습니다. (주행거리 30만km 이하 데이터 없음)")
        st.write("")
        return

    # x축 눈금
    x_ticks = list(range(0, 31, 2))

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # 히스토그램: 거래건수
    ax1.bar(df_plot['trvlDstnc'], df_plot['CNT'], color='skyblue', alpha=0.7, label='거래건수(cnt)', width=0.8)
    ax1.set_xlabel('주행거리 (만km)', fontsize=12)
    ax1.set_ylabel('거래건수', fontsize=12)
    ax1.set_ylim(0, max(df_plot['CNT']) * 1.1)  # 🔥 동적 y축
    ax1.set_xticks(x_ticks)
    ax1.grid(True, axis='y', alpha=0.3)

    # 두 번째 y축: avgPrice
    ax2 = ax1.twinx()
    ax2.plot(df_plot['trvlDstnc'], df_plot['avgPrice'], color='red', marker='o', 
             label='평균 시세(avgPrice)', linewidth=2, markersize=6)
    ax2.set_ylabel('금액(만원)', fontsize=12)
    ax2.set_ylim(0, max(df_plot['avgPrice']) * 1.1)  # 🔥 동적 y축

    # 범례
    ax1.legend(loc='upper left', fontsize=7)
    ax2.legend(loc='upper right', fontsize=7)

    st.markdown('<p style="font-size:12px; font-weight:bold; margin-bottom:0px;">주행거리별 거래 통계</p>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)
    st.pyplot(fig)