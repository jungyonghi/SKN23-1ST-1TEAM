import streamlit as st
import pandas as pd
import mysql.connector
import connector
import html

# ==========================================================
# 1. 데이터베이스 연결 및 DataFrame 생성
# ==========================================================
try:
    conn = connector.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)

    with open("sql/faqList.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    
    # 원본 DataFrame (FAQ 포함)
    df = pd.DataFrame(data) 
    
except Exception as e:
    st.error(f"데이터베이스 연결 또는 쿼리 실행 중 오류 발생: {e}")
    df = pd.DataFrame() 


# 💡 카드 출력용 DataFrame 생성 및 정렬
if not df.empty:
    # 중복 제거 기준: carClassNm과 yearType이 모두 같아야 중복으로 간주
    df_card_view = df.drop_duplicates(subset=['carClassNm', 'yearType'], keep='first') 
    
    # 출력 순서 정렬: carClassNm으로 1차 정렬 후, yearType을 내림차순(최신 연식부터)으로 정렬
    df_card_view = df_card_view.sort_values(by=['carClassNm', 'yearType'], ascending=[True, False])
    
    # 💡 검색을 위해 'car_name_display' 컬럼을 미리 생성합니다.
    # carClassNm에서 순수 모델명만 추출 (연식 제거)
    df_card_view['car_model_only'] = df_card_view['carClassNm'].str.replace(r'^\d{4}\s+', '', regex=True)
    df_card_view['car_name_display'] = df_card_view['yearType'].astype(str) + ' ' + df_card_view['car_model_only']
else:
    df_card_view = pd.DataFrame()


# ==========================================================
# 2. 검색창 및 필터링 로직 추가 ⭐
# ==========================================================
st.subheader("차량 FAQ")
search_query = st.text_input("", placeholder="차종 또는 연식을 입력하세요 (예: 아반떼, 2022)")
st.markdown('<hr style="margin:2px 0;">', unsafe_allow_html=True)

# 필터링할 DataFrame 초기화
df_filtered = df_card_view.copy()

if search_query:
    # 💡 필터링 기준: car_name_display 컬럼을 사용 (carname 변수에 할당되는 값)
    # 대소문자 구분 없이 검색어가 포함된 행을 필터링합니다.
    df_filtered = df_filtered[
        df_filtered['car_name_display'].str.contains(search_query, case=False, na=False)
    ]
    
# 검색 결과가 없을 경우 메시지 출력
if df_filtered.empty and search_query:
    st.info(f"'{search_query}'에 해당하는 차량이 없습니다.")





# ==========================================================
# 3. Streamlit 카드 및 FAQ 출력 (필터링된 데이터 사용)
# ==========================================================

# 💡 수정: 필터링된 df_filtered를 순회합니다.
for idx, row in df_filtered.iterrows():
    
    # 차량 카드 정보 추출 
    car_name_base = row['carClassNm']
    car_year_type = row.get('yearType', '연식 정보 없음')
    
    # 출력용 차량 이름 (FAQ 제목에 사용됨)
    car_name_display = row['car_name_display'] 
    
    car_image = row['carClassRepImage']
    brand_image = row['brandImage']
    car_price_range = row.get('carPrice', '가격 정보 없음') 
    
    # 💡 carname 변수 할당
    carname = car_name_display 
    
    # FAQ 제목 (카드 위에 출력)
    st.markdown(f"<h3 style='font-weight:bold'>{carname}</h3>", unsafe_allow_html=True)

    
    st.markdown(f"""
    <div style="display: flex; flex-wrap: wrap; gap: 20px; border:1px solid #ddd; padding:20px; border-radius:10px; margin-bottom:10px; align-items:center;">
        <div style="flex: 1 1 200px; min-width: 200px; max-width: 300px;">
            <img src="{car_image}" style="width:100%; height:auto; border-radius:5px; display:block;">
        </div>
        <div style="flex: 0 0 30px; min-width: 0;">
        </div>
        <div style="flex: 2 1 200px; min-width: 250px; display:flex; flex-direction: column; gap:10px;">
            <div style="display:flex; align-items:center; gap:15px; flex-wrap: wrap;">
                <img src="{brand_image}" style="width:40px; height:40px; border-radius:25px; flex-shrink:0;">
                <p style='font-size:clamp(16px, 2.2vw, 24px); font-weight:bold; margin:0; line-height:1.2; word-break:keep-all;'>{car_name_display}</p>
            </div>
            <div style="text-align:left;">
                <p style='font-size:clamp(14px, 3vw, 16px); font-weight:normal; margin:0 0 10px 0; color:#333; line-height:1.5;'>중고시세: {car_price_range}</p>
                <p style='font-size:clamp(14px, 3vw, 16px); font-weight:normal; margin:0; color:#333; line-height:1.5;'>차량연식: {car_year_type}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
# 💡 FAQ 필터링: carClassNm과 yearType이 모두 일치하는 FAQ만 추출
    df_faq = df[(df['carClassNm'] == car_name_base) & (df['yearType'] == car_year_type)]
    
    if not df_faq.empty:
        
        for _, faq_row in df_faq.iterrows():
            question = faq_row['question']
            answer = faq_row['answer']
            
            # 질문과 답변을 Streamlit의 Expander로 출력합니다.
            with st.expander(f"**Q.** {question}"):
                st.markdown(f"**A.** {answer}")
                
        st.markdown("---")