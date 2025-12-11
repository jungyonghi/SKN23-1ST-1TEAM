import streamlit as st
import pandas as pd
import mysql.connector
import connector
from card import card
import comparison_data


# ===================== PAGE CONFIG =======================
st.set_page_config(
    page_title="중고차 비교 분석",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
/* 전체 컨테이너 폭 늘리기 */
.block-container {
    padding-left: 10px;   /* 좌측 여백 */
    padding-right: 10px;  /* 우측 여백 */
    max-width: 80%;       /* 최대폭 제한 해제 */
}
</style>
<style>
.block-container {
    padding-top: 20px;     /* 상단 여백 */
    padding-bottom: 20px;  /* 하단 여백 */
}
@media screen and (max-width: 768px) {
    .st-emotion-cache-1s2v671.e1gk92lc0 {
        display:none !important;
    }
    .st-emotion-cache-1permvm{
        gap : 0.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


col_l, col_space, col_r = st.columns([1,0.1,1])
with col_l:
    st.write("")
    st.markdown("### 기준 차량")

    # ===================== UI 구성 ===========================
    col1_l, col2_l = st.columns([1,1])

    # =========================================================
    # 1) 브랜드 선택
    # =========================================================
    with col1_l:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/brandList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_brand = pd.DataFrame(data)

        col11_l, col12_l = st.columns([1.2, 3.8])
        with col11_l:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>브랜드</p>",unsafe_allow_html=True)
        with col12_l:
            # 브랜드 선택 옵션 (이름 → 번호)
            options_brand = {row["brandNm"]: row["brandNbr"] for _, row in df_brand.iterrows()}

            selected_brandNm1 = st.selectbox(" ", list(options_brand.keys()), key="brand_select1")
            selected_brandNbr1 = options_brand[selected_brandNm1] 
    # =========================================================
    # 2) 차종(대표모델) 선택
    # =========================================================
    with col2_l:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/carClassList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql, (selected_brandNbr1,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_car = pd.DataFrame(data)

        col21_l, col22_l = st.columns([0.7, 3.3])
        with col21_l:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>차종</p>", unsafe_allow_html=True)
        # 차종 선택 옵션 (이름 → 번호)
        with col22_l:
            options_car = {row["repCarClassNm"]: row["repCarClassNbr"] for _, row in df_car.iterrows()}
            selected_carNm1 = st.selectbox(" ", list(options_car.keys()), key="car_select1")
            selected_carNbr1 = options_car[selected_carNm1] 


    # =========================================================
    # 3) 연식 + 세부 차종 선택 (ex: 2022 아반떼)
    # =========================================================
    col3_l, col4_l = st.columns([1,1])
    with col3_l:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/carClassDtlList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql, (selected_carNbr1,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_yearcar = pd.DataFrame(data)
        col31_l, col32_l = st.columns([0.7, 3.3])
        with col31_l:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>연식</p>",
                        unsafe_allow_html=True)
            
        with col32_l:        
            # 연식+세부차 선택 옵션 (이름 → 번호)
            options_yearcar = {row["carClassNm"]: row["carClassNbr"] for _, row in df_yearcar.iterrows()}
            selected_yearcarNm1 = st.selectbox(" ", list(options_yearcar.keys()), key="yearcar_select1")
            selected_yearcarNbr1 = options_yearcar[selected_yearcarNm1]

    with col4_l:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/competList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql, (selected_yearcarNbr1,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_grade = pd.DataFrame(data)
        col41_l, col42_l = st.columns([0.7, 3.3])
        with col41_l:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>등급</p>", unsafe_allow_html=True)
            
        with col42_l:        
            # 등급 선택: selectbox에는 이름(carGradeNm)을 보여줌
            options_grade = {row["carGradeNm"]: row["carGradeNbr"] for _, row in df_grade.iterrows()}

            selected_gradeNm1 = st.selectbox(" ", list(options_grade.keys()), key="grade_select1")
            
            # 실제 사용할 ID
            selected_gradeNbr1 = options_grade[selected_gradeNm1]
    
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr1  
    with open("sql/car_grade_data.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.execute(sql, (keyword, keyword, keyword))
    data = cursor.fetchall()
    cursor.close()
    connection.close() 

    card(data)
    st.markdown("<br>", unsafe_allow_html=True)  

            
with col_space:
    st.markdown(" ")


with col_r:
    st.write("")
    st.markdown("### 비교 차량")
    # ===================== UI 구성 ===========================
    col1, col2 = st.columns([1,1])

    # =========================================================
    # 1) 브랜드 선택
    # =========================================================
    with col1:

        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/brandList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_brand = pd.DataFrame(data)

        col11, col12 = st.columns([1.2, 3.8])
        with col11:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>브랜드</p>",
                        unsafe_allow_html=True)
        with col12:
            # 브랜드 선택 옵션 (이름 → 번호)
            options_brand = {row["brandNm"]: row["brandNbr"] for _, row in df_brand.iterrows()}

            selected_brandNm2 = st.selectbox(" ", list(options_brand.keys()), key="brand_select2")
            selected_brandNbr2 = options_brand[selected_brandNm2] 

    # =========================================================
    # 2) 차종(대표모델) 선택
    # =========================================================
    with col2:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/carClassList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql, (selected_brandNbr2,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_car = pd.DataFrame(data)

        col21, col22 = st.columns([0.7, 3.3])
        with col21:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>차종</p>",unsafe_allow_html=True)
        # 차종 선택 옵션 (이름 → 번호)
        with col22:
            options_car = {row["repCarClassNm"]: row["repCarClassNbr"] for _, row in df_car.iterrows()}
            selected_carNm2 = st.selectbox(" ", list(options_car.keys()), key="car_select2")
            selected_carNbr2 = options_car[selected_carNm2]  


    # =========================================================
    # 3) 연식 + 세부 차종 선택 (ex: 2022 아반떼)
    # =========================================================
    col3, col4 = st.columns([1,1])
    with col3:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/carClassDtlList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql, (selected_carNbr2,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_yearcar = pd.DataFrame(data)
        col31, col32 = st.columns([0.7, 3.3])
        with col31:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>연식</p>",
                        unsafe_allow_html=True)
            
        with col32:        
            # 연식+세부차 선택 옵션 (이름 → 번호)
            options_yearcar = {row["carClassNm"]: row["carClassNbr"] for _, row in df_yearcar.iterrows()}
            selected_yearcarNm2 = st.selectbox(" ", list(options_yearcar.keys()), key="yearcar_select2")
            selected_yearcarNbr2 = options_yearcar[selected_yearcarNm2]  
            
    with col4:
        conn = connector.get_connection()
        cur = conn.cursor(dictionary=True, buffered=True)

        with open("sql/competList.sql", "r", encoding="utf-8") as f:
            sql = f.read()

        cur.execute(sql, (selected_yearcarNbr2,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        df_grade = pd.DataFrame(data)
        col41, col42 = st.columns([0.7, 3.3])
        with col41:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>등급</p>", unsafe_allow_html=True)
        
        with col42:        
            # 등급 선택: selectbox에는 이름(carGradeNm)을 보여줌
            options_grade = {row["carGradeNm"]: row["carGradeNbr"] for _, row in df_grade.iterrows()}

            selected_gradeNm2 = st.selectbox(
                " ", 
                list(options_grade.keys()), key="grade_select2")
            
            # 실제 사용할 ID
            selected_gradeNbr2 = options_grade[selected_gradeNm2]
            
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr2  
    with open("sql/car_grade_data.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.execute(sql, (keyword, keyword, keyword))
    data = cursor.fetchall()
    cursor.close()
    connection.close() 

    card(data)
    st.markdown("<br>", unsafe_allow_html=True) 


# ===================================================================
comparison_data.main(selected_gradeNbr1, selected_gradeNbr2)