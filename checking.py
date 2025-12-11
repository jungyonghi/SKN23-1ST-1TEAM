import streamlit as st
from chart_future import chart_future  # 함수 import(꺽은선)
from chart_mileage import chart_mileage # 함수 import(히스토그램+꺽은선)
from chart_age import chart_age # 함수 import(막대그래프)
from chart_gender import chart_gender # 함수 import(도넛형)
from chart_region import chart_region # 함수 import(지역)
from rating import rating # 함수 import(등급)
from card import card # 함수 import(카드)
import pandas as pd
import ast
import mysql.connector
import connector
# ===================== 모바일 반응형 CSS ===========================
st.markdown("""
<style>
/* 기본 레이아웃 설정 */
.block-container {
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 20px;
    padding-bottom: 20px;
    max-width: 80%;
}

/* 모바일 화면 (폭 768px 이하) */
@media (max-width: 768px) {
    /* 페이지 전체 폭 사용 */
    .block-container {
        padding-left: 15px !important;
        padding-right: 15px !important;
        max-width: 100% !important;
    }
    
    /* 컬럼을 세로로 쌓이게 */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    
    /* 컬럼 컨테이너를 세로 배치로 */
    [data-testid="stHorizontalBlock"] {
        #flex-direction: column !important;
    }
    
    /* 선택박스와 입력 요소 폭 100% */
    .stSelectbox, .stNumberInput, .stTextInput {
        width: 100% !important;
    }
    
    /* 선택박스 내부 요소도 100% */
    .stSelectbox > div, .stNumberInput > div, .stTextInput > div {
        width: 100% !important;
    }
    
    /* 차트 컨테이너 폭 100% */
    .element-container {
        width: 100% !important;
    }
    
    /* 텍스트 중앙 정렬 */
    h1, h2, h3, p {
        text-align: center !important;
    }
    
    /* 라벨 정렬 */
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        text-align: center !important;
        width: 100% !important;
    }
    
    /* 마진 조정 */
    div[data-testid="column"] > div {
        margin-bottom: 10px !important;
    }
    .st-emotion-cache-1s2v671.e1gk92lc0 {
        display:none !important;
    }
    h1, h2, h3, p {
        text-align: left !important;
    }
    .block-container {
        padding-left: 10px;
        padding-right: 10px;
        max-width: 80% !important;
    }
}

/* 태블릿 화면 (폭 769px ~ 1024px) */
@media (min-width: 769px) and (max-width: 1024px) {
    .block-container {
        max-width: 95% !important;
    }
    .st-emotion-cache-1s2v671.e1gk92lc0 {
        display:none !important;
    }
    .st-emotion-cache-st-emotion-cache-1s2v671.e1gk92lc0{
        gap : 0rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ===================== UI 구성 ===========================
col1, col2, col3 = st.columns([1,1,1])

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

    col11, col12 = st.columns([0.9, 4.1])
    with col11:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>브랜드</p>",
                    unsafe_allow_html=True)
    with col12:
        options_brand = {row["brandNm"]: row["brandNbr"] for _, row in df_brand.iterrows()}

        selected_brandNm = st.selectbox(" ", list(options_brand.keys()), key="brand_select")
        selected_brandNbr = options_brand[selected_brandNm]  


# =========================================================
# 2) 차종(대표모델) 선택
# =========================================================
with col2:
    conn = connector.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)

    with open("sql/carClassList.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cur.execute(sql, (selected_brandNbr,))
    data = cur.fetchall()
    cur.close()
    conn.close()

    df_car = pd.DataFrame(data)

    col21, col22 = st.columns([0.7, 4.3])
    with col21:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>차종</p>",
                    unsafe_allow_html=True)
    # 차종 선택 옵션 (이름 → 번호)
    with col22:
        options_car = {row["repCarClassNm"]: row["repCarClassNbr"] for _, row in df_car.iterrows()}
        selected_carNm = st.selectbox(" ", list(options_car.keys()), key="car_select")
        selected_carNbr = options_car[selected_carNm]  # 실제 사용할 번호! ⭐


# =========================================================
# 3) 연식 + 세부 차종 선택 (ex: 2022 아반떼)
# =========================================================
with col3:
    conn = connector.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)

    with open("sql/carClassDtlList.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cur.execute(sql, (selected_carNbr,))
    data = cur.fetchall()
    cur.close()
    conn.close()

    df_yearcar = pd.DataFrame(data)
    col31, col32 = st.columns([0.7, 4.3])
    with col31:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:16px; font-weight:700; margin-top:9px;'>연식</p>",
                    unsafe_allow_html=True)
        
    with col32:        
        options_yearcar = {row["carClassNm"]: row["carClassNbr"] for _, row in df_yearcar.iterrows()}
        selected_yearcarNm = st.selectbox(" ", list(options_yearcar.keys()), key="yearcar_select")
        selected_yearcarNbr = options_yearcar[selected_yearcarNm]  # 실제 사용할 번호! ⭐


# ============ 아래 부분 ================
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    # =========== card() & rating() ================================
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr 
    with open("sql/car_grade_data.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.execute(sql, (keyword, keyword, keyword))
    data = cursor.fetchall()
    cursor.close()
    connection.close() 

    card(data)
    st.markdown("<br>", unsafe_allow_html=True)   
    
    selected_id=rating(data)
    print(selected_id)
with col2:  
    
    # =========== chart_future() ================================
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr 
    with open("sql/selectPrice.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql, (keyword,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    data = pd.DataFrame(data)    
    chart_future(data, selected_id)  # 꺽은선 그래프  ====> 주행거리별 셀렉트 박스 넣을때 if문 사용해서 차트를 다 만들어 놓은 것을 불러오는 형식으로 할까 고민중
    
    # 차트 사이 개행 1번
    st.markdown("<br>", unsafe_allow_html=True)
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr   # ★ LIKE 검색은 이렇게 해야 함
    with open("sql/selectDistancePrice.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql, (keyword,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    data = pd.DataFrame(data)    

    chart_mileage(data) # 주행거리별 가격
with col3:  
    # =========== chart_age() ================================
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr   # ★ LIKE 검색은 이렇게 해야 함
    with open("sql/selectAge.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql, (keyword,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    
    chart_age(data)  # 나이별 통계량
    st.markdown("<br>", unsafe_allow_html=True)
    # =========== chart_gender() ================================
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr   # ★ LIKE 검색은 이렇게 해야 함
    with open("sql/selectGender.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql, (keyword,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    
    chart_gender(data)
    st.markdown("<br>", unsafe_allow_html=True)
    # =========== chart_region() ================================
    connection = connector.get_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    keyword = selected_yearcarNbr   # ★ LIKE 검색은 이렇게 해야 함
    with open("sql/selectRegion.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql, (keyword,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    chart_region(data)
    


