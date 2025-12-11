# 도넛형 차트 : 성별 거래 통계

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

def chart_gender(data):
    # 한글폰트 설정
    rcParams['font.family'] = 'Malgun Gothic'
    rcParams['axes.unicode_minus'] = False

    df = pd.DataFrame(data)
    
    # 🔥 필수 컬럼 확인 (경고문 없이 조용히 종료)
    required_cols = ['GENDER', 'percent', 'CNT']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.write("")
        return  # 조용히 종료
    
    # 🔥 데이터 타입 변환
    df['percent'] = pd.to_numeric(df['percent'], errors='coerce')
    df['CNT'] = pd.to_numeric(df['CNT'], errors='coerce')
    
    # 🔥 NaN 제거
    df = df.dropna(subset=['GENDER', 'percent', 'CNT'])
    
    # 🔥 빈 데이터 체크 (조용히 종료)
    if df.empty:
        st.write("")
        return

    # 1. 제목 (작게 + 볼드 + 아래 여백 최소화)
    st.markdown('<p style="font-size:14px; font-weight:bold; margin-bottom:0px;">성별 거래 통계</p>', unsafe_allow_html=True)

    # 2. 구분선 (위아래 여백 최소화)
    st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)

    # 색상
    colors = {'남자': '#1f77b4', '여자': '#ff69b4', '법인및사업자': '#d3d3d3'}

    fig, ax = plt.subplots(figsize=(2,2))

    # 도넛형
    wedges, _ = ax.pie(
        df['percent'],
        startangle=90,
        colors=[colors.get(g, '#cccccc') for g in df['GENDER']],  # 🔥 .get()으로 안전하게
        wedgeprops={'width':0.3, 'edgecolor':'white'},
        radius = 0.8
    )

    # 데이터 레이블 + 선
    for i, p in enumerate(wedges):
        angle = (p.theta2 - p.theta1)/2. + p.theta1
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))
        
        horizontalalignment = 'left' if x > 0 else 'right'
        x_text = x * 1.2   # 레이블 위치 더 멀리
        y_text = y * 1.2
        
        ax.annotate(
            f"{df['GENDER'].iloc[i]}: {df['percent'].iloc[i]}%",  # 🔥 .iloc[] 사용
            xy=(x*0.8, y*0.8), xycoords='data',  # 🔥 radius 0.8 반영
            xytext=(x_text, y_text), textcoords='data',
            ha=horizontalalignment, va='center',
            fontsize=9, fontweight='bold',
            arrowprops=dict(arrowstyle="-", connectionstyle="angle,angleA=0,angleB=90", color='gray', lw=0.8)
        )

    # 범례: 성별 왼쪽, 건(%) 오른쪽처럼 보이게
    legend_labels = []
    max_len = max(len(row['GENDER']) for idx, row in df.iterrows())
    for idx, row in df.iterrows():
        # 공백으로 간격 맞춤 (monospace 느낌)
        spaces = " " * (max_len - len(row['GENDER']) + 3)
        label = f"{row['GENDER']}{spaces}{int(row['CNT']):,}건({int(row['percent'])}%)"  # 🔥 int() 변환
        legend_labels.append(label)

    ax.legend(
        wedges, legend_labels, 
        loc="center left", 
        bbox_to_anchor=(1.15, -0.5, 0.5, 1),  # 🔥 범례 위치 조정
        fontsize=9,  # 🔥 폰트 크기 축소
        frameon=False  # 🔥 테두리 제거
    )

    ax.axis('equal')

    return st.pyplot(fig)