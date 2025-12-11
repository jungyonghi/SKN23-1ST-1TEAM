import streamlit as st
import pandas as pd
import altair as alt
import requests 
# import pymysql
import connector
connection = connector.get_connection()

# =============================================================================
# 1. 설정 및 CSS 주입
# =============================================================================
st.set_page_config(page_title="비교 분석", layout="wide")

st.markdown("""
<style>
    @media (max-width: 768px) {
        .block-container h1, .block-container h2, .block-container h3, .block-container p { text-align: center; }
        div[data-testid="stMetric"] { display: flex; flex-direction: column; align-items: center; }
        div[data-testid="column"] { text-align: center; }
        .stTextInput label, .stNumberInput label, .stSelectbox label { justify-content: center; display: flex; }
    }
</style>
""", unsafe_allow_html=True)

#############################################################################
# 연료 가격 API 설정
API_KEY = "F251208231"
API_URL = "https://www.opinet.co.kr/api/avgAllPrice.do"

# 기본 연료 가격 프리셋
DEFAULT_PRICES = {
    'Gasoline': 1745.0, 
    'Diesel': 1659.0, 
    'LPG': 997.0,
    'Electric': 313.0, 
    'Hydrogen': 10000.0
}

# ---------------------------------------------------------------------------
# API 호출 함수
# ---------------------------------------------------------------------------
def fetch_opinet_prices():
    try:
        params = {'code': API_KEY, 'out': 'json'}
        response = requests.get(API_URL, params=params, timeout=3)
        data = response.json()
        
        if 'RESULT' in data and 'OIL' in data['RESULT']:
            new_prices = {}
            for oil in data['RESULT']['OIL']:
                prod_cd = oil.get('PRODCD')
                price = float(oil.get('PRICE', 0))
                
                # 제품 코드 매핑
                # B027: 휘발유, D047: 경유, K015: 자동차부탄
                if prod_cd == 'B027': new_prices['Gasoline'] = price
                elif prod_cd == 'D047': new_prices['Diesel'] = price
                elif prod_cd == 'K015': new_prices['LPG'] = price
            return new_prices
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

#############################################################################
# [수정됨] DB 연결 및 데이터 로드 함수
#############################################################################
@st.cache_data
def load_data():
    try:
        # 1. DB 연결 설정 (사용자 환경에 맞게 비밀번호 등 확인 필요)

        
        # 2. Pandas read_sql을 사용하여 테이블 전체 가져오기
        # (DB에 car, grade, price 테이블이 존재해야 함)
        df_car = pd.read_sql("SELECT * FROM car", connection)
        df_grade = pd.read_sql("SELECT * FROM grade", connection)
        df_price = pd.read_sql("SELECT * FROM price", connection)
        
        # 3. 데이터 로드 후 연결 종료
        connection.close()

        ################# 데이터 전처리 및 타입 변환 ###########################
        # ID 값들이 문자열로 매칭되어야 하므로 타입 변환
        df_grade['carClassNbr'] = df_grade['carClassNbr'].astype(str)
        df_grade['carGradeNbr'] = df_grade['carGradeNbr'].astype(str)
        df_car['carClassNbr'] = df_car['carClassNbr'].astype(str)
        df_price['carGradeNbr'] = df_price['carGradeNbr'].astype(str)

        # 가격 데이터 중복 제거 (가격 높은 순 정렬 후 첫 번째 값 유지)
        df_price_clean = df_price.sort_values('gradeUsedCarPrice', ascending=False).drop_duplicates('carGradeNbr')
        
        # 테이블 병합 (Grade + Car + Price)
        df_merged = pd.merge(df_grade, df_car[['carClassNbr', 'carClassNm', 'brandNm']], on='carClassNbr', how='inner')
        df_final = pd.merge(df_merged, df_price_clean[['carGradeNbr', 'gradeUsedCarPrice']], on='carGradeNbr', how='inner')
        
        # 검색용 Full Name 컬럼 생성
        df_final['Full_Name'] = df_final['brandNm'] + " " + df_final['carClassNm'] + " " + df_final['carGradeNm']
        
        return df_final
        

    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()

################# 연료 타입에 따른 가격 반환 함수 ###############################
def get_current_price(fuel_type, price_dict):
    f = str(fuel_type).strip()
    if 'Hybrid' in f or 'Gasoline' in f: return price_dict['Gasoline']
    if 'Diesel' in f: return price_dict['Diesel']
    if 'LPG' in f: return price_dict['LPG']
    if 'Electric' in f: return price_dict['Electric']
    if 'Hydrogen' in f: return price_dict['Hydrogen']
    return price_dict['Gasoline']

# =============================================================================
# 2. 메인 로직 
# =============================================================================
def main(grade_a, grade_b):
    print("=== Streamlit App Started ===")
    # 데이터 매개변수로 입력
    # -------------------------------------------------------------------------
    # 초기화 로직: 앱 실행 시 최초 1회만 API 호출 및 세션 설정
    # -------------------------------------------------------------------------
    if 'input_gas' not in st.session_state:
        
        # 1. 기본값
        init_prices = DEFAULT_PRICES.copy()
        
        # 2. API 호출
        api_data = fetch_opinet_prices()
        
        # 3. API 성공 시 값 덮어쓰기
        if api_data:
            init_prices.update(api_data)
        
        # 4. 세션 스테이트에 저장 (위젯 Key와 매칭)
        st.session_state['input_gas'] = float(init_prices['Gasoline'])
        st.session_state['input_diesel'] = float(init_prices['Diesel'])
        st.session_state['input_lpg'] = float(init_prices['LPG'])
        st.session_state['input_elec'] = float(init_prices['Electric'])
        st.session_state['input_hydro'] = float(init_prices['Hydrogen'])
    
    # 데이터 로드 (DB 연결은 load_data 내부에서 처리됨)
    df = load_data()
    if df.empty: return



    ######################################## ---  ID 입력 --###############################################
    col1, col2 = st.columns(2)

    def get_car_by_id(input_id):
        if not input_id: return None
        found = df[df['carGradeNbr'] == str(input_id)]
        if found.empty: return None
        return found.iloc[0]

    with col1:
        id_a = grade_a
        row_a = get_car_by_id(id_a)
        if row_a is not None:
            # st.success(f"{row_a['Full_Name']}")
            st.caption(f"연료: {row_a['fuel']} | 연비: {row_a['gradeFuelRate']} ")
        else:
            st.error("ID를 찾을 수 없습니다.")

    with col2:
        id_b = grade_b
        row_b = get_car_by_id(id_b)
        if row_b is not None:
            # st.success(f"{row_b['Full_Name']}")
            st.caption(f"연료: {row_b['fuel']} | 연비: {row_b['gradeFuelRate']} ")
        else:
            st.error("ID를 찾을 수 없습니다.")
    
    # 연비 예측 위치
    st.subheader(f"20년 연비 예측")
    graph_area = st.empty()

    if row_a is None or row_b is None: return
    # st.markdown("### 2. 운행 조건 설정")
    annual_km = st.slider("연간 주행거리 (km)", 5000, 50000, 20000, step=1000)

        # -------------------------------------------------------------------------
    # 상단 유가 세팅 
    # -------------------------------------------------------------------------
    with st.expander("연료비 설정 조절", expanded=False):
        cols = st.columns(5)
       
        prices = {}

        # 유가 세팅 파트      
        with cols[0]:
            prices['Gasoline'] = st.number_input("휘발유 (원/L)", key="input_gas", format="%.0f", step=1.0)
        with cols[1]:
            prices['Diesel'] = st.number_input("경유 (원/L)", key="input_diesel", format="%.0f", step=1.0)
        with cols[2]:
            prices['LPG'] = st.number_input("LPG (원/L)", key="input_lpg", format="%.0f", step=1.0)
        with cols[3]:
            prices['Electric'] = st.number_input("전기 (원/kWh)", key="input_elec", format="%.0f", step=1.0)
        with cols[4]:
            prices['Hydrogen'] = st.number_input("수소 (원/kg)", key="input_hydro", format="%.0f", step=1.0)
    # -------------------------------------------------------------------------
    # 비용 계산 로직
    # -------------------------------------------------------------------------
    eff_a = float(row_a['gradeFuelRate'])
    price_a = float(row_a['gradeUsedCarPrice'])
    cost_a = (annual_km / eff_a) * get_current_price(row_a['fuel'], prices)

    try : 
        eff_b = float(row_b['gradeFuelRate'])
    except : 
        eff_b = 1
    price_b = float(row_b['gradeUsedCarPrice'])
    try :
        cost_b = (annual_km / eff_b) * get_current_price(row_b['fuel'], prices)
    except:
        cost_b = (annual_km / 1) * get_current_price(row_b['fuel'], prices)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("차값 (A)", f"{int(price_a/10000):,} 만원")
    m2.metric("연 유지비 (A)", f"{int(cost_a/10000):,} 만원")
    m3.metric("차값 (B)", f"{int(price_b/10000):,} 만원", delta=f"{int((price_b-price_a)/10000):,} 만원")
    m4.metric("연 유지비 (B)", f"{int(cost_b/10000):,} 만원", delta=f"{int((cost_b-cost_a)/10000):,} 만원", delta_color="inverse")


    # -------------------------------------------------------------------------
    # 리포트 출력
    # -------------------------------------------------------------------------
    # st.markdown("### 분석 리포트")
    name_a_short = f"{row_a['brandNm']} {row_a['carClassNm']}"
    name_b_short = f"{row_b['brandNm']} {row_b['carClassNm']}"
    if name_a_short == name_b_short:
        name_a_short += f"({row_a['fuel']})"
        name_b_short += f"({row_b['fuel']})"

    # st.markdown(f"**A (기준):** :blue[{name_a_short}]")
    # st.markdown(f"**B (비교):** :orange[{name_b_short}]")
    # st.divider() 

    # 연비 예측 파트
    FORECAST_YEARS = 20
    chart_data = []
    for y in range(FORECAST_YEARS + 1):
        chart_data.append({"Year": y, "Car": f"A: {row_a['Full_Name']}", "Total Cost": price_a + (cost_a * y)})
        chart_data.append({"Year": y, "Car": f"B: {row_b['Full_Name']}", "Total Cost": price_b + (cost_b * y)})
    chart_df = pd.DataFrame(chart_data)
    
    chart = alt.Chart(chart_df).mark_line(point=alt.OverlayMarkDef(size=120, filled=True), strokeWidth=4).encode(
        x=alt.X("Year", title="운행 년수", axis=alt.Axis(tickMinStep=1)),
        y=alt.Y("Total Cost", title="누적 총 비용 (원)", axis=alt.Axis(format="~s"), scale=alt.Scale(zero=False, padding=20)),
        color=alt.Color("Car", legend=alt.Legend(orient="bottom", direction="vertical", title=None)),
        tooltip=["Year", "Car", alt.Tooltip("Total Cost", format=",")]
    ).interactive()

    graph_area.altair_chart(chart, use_container_width=True)
    # -------------------------------------------------------------------------
    # 결과 메시지 생성
    # -------------------------------------------------------------------------
    diff_price = price_a - price_b
    diff_cost = cost_a - cost_b
    abs_cost_val = int(abs(diff_cost) / 10000)
    abs_price_val = int(abs(diff_price) / 10000)

    style_css = """
    <style>
        .result-box { background-color: rgba(255, 255, 255, 0.05);  solid rgba(255, 255, 255, 0.2); border-radius: 12px; padding: 0px; line-height: 1.8; font-size: 16px;  margin-top: 10px; }
        .highlight-a { color: #4FC3F7; font-weight: 700; }
        .highlight-b { color: #FFB74D; font-weight: 700; }
        .val-good { color: #69F0AE; font-weight: 700; }
        .val-bad { color: #FF5252; font-weight: 700; }
        .val-time { color: #FFD740; font-weight: 700; }
    </style>
    """

    st.markdown(style_css, unsafe_allow_html=True)
    
    def make_html(main_msg, sub_msg):
        return f"""<div class="result-box"><div style="margin-bottom: 8px;">{main_msg}</div><div>{sub_msg}</div></div>"""
    
    txt_a = f"<span class='highlight-a'>{name_a_short}</span>"
    txt_b = f"<span class='highlight-b'>{name_b_short}</span>"
    final_html = ""
    
    if diff_cost < 0:
        msg_fuel = f"{txt_a}를 타시면 매년 <span class='val-good'>{abs_cost_val:,}만원</span>씩 연료비를 절약합니다."
        if diff_price <= 0: msg_concl = f"결론: {txt_a}은(는) 차값도 <span class='val-good'>{abs_price_val:,}만원</span> 더 저렴하고 유지비도 적게 드는 <span class='val-good'>경제적인 선택</span>입니다."
        else:
            bep = diff_price / abs(diff_cost)
            msg_concl = f"결론: {txt_a}의 차값이 <span class='val-bad'>{abs_price_val:,}만원</span> 더 비싸지만, 연료비 절감으로 <span class='val-time'>약 {bep:.1f}년</span> 후에는 총 비용이 역전됩니다."
        final_html = make_html(msg_fuel, msg_concl)
    elif diff_cost > 0:
        msg_fuel = f"{txt_a}를 타시면 매년 <span class='val-bad'>{abs_cost_val:,}만원</span>씩 연료비가 더 발생합니다."
        if diff_price >= 0: msg_concl = f"결론: {txt_a}은(는) 차값도 <span class='val-bad'>{abs_price_val:,}만원</span> 더 비싸고, 유지비도 더 많이 드는 선택입니다."
        else:
            bep = abs(diff_price) / diff_cost
            msg_concl = f"결론: {txt_a}의 차값은 <span class='val-good'>{abs_price_val:,}만원</span> 더 저렴하지만, 연료비 과다로 <span class='val-time'>약 {bep:.1f}년</span> 후에는 {txt_b}가 더 유리해집니다."
        final_html = make_html(msg_fuel, msg_concl)
    else:
        msg_fuel = "두 차량의 연간 연료비가 동일합니다."
        if diff_price < 0: msg_concl = f"결론: {txt_a}의 차값이 <span class='val-good'>{abs_price_val:,}만원</span> 저렴하여 경제적입니다."
        elif diff_price > 0: msg_concl = f"결론: {txt_a}의 차값이 <span class='val-bad'>{abs_price_val:,}만원</span> 비싸서 비경제적입니다."
        else: msg_concl = "결론: 두 차량의 차값과 유지비가 완전히 동일합니다."
        final_html = make_html(msg_fuel, msg_concl)
        
    st.markdown(final_html, unsafe_allow_html=True)
    st.write("")
    st.write("")

if __name__ == "__main__":
    main()