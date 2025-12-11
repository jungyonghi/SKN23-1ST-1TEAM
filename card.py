# import streamlit as st
# import pandas as pd

# def card(data,selected_brand, selected_car, selected_year):
#     df = pd.dataframe(data)
       
#     row = df[
#         (df['carGradeNm'] == selected_grade) &
#         (df['carClassNm'] == selected_model) &
#         (df['yearType'] == selected_year)
#     ].iloc[0]
    
#     brand_row = df[df['carGradeNm'] == selected_grade].iloc[0]
    
#     st.markdown(f"""
#     <div style="display: flex; flex-wrap: wrap; gap: 10px; border:1px solid #ddd; padding:10px; border-radius:10px;">
#         <div style="flex: 1 1 150px; min-width:150px;">
#             <img src="{row['carClassRepImage']}" style="width:100%; border-radius:5px;">
#         </div>
#         <div style="flex: 2 1 200px; min-width:200px; display:flex; flex-direction: column; gap:10px;">
#             <div style="display:flex; gap:8px; align-items:center;">
#                 <div style="flex:1; max-width:60px;">
#                     <img src="{brand_row['brandImage']}" style="width:100%; border-radius:5px;">
#                 </div>
#                 <div style="flex:3; display:flex; align-items:center;">
#                     <p style='font-size:20px; font-weight:bold; margin:0; line-height:1.2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{selected_model}</p>
#                 </div>
#             </div>
#             <div>
#                 <p style='font-size:15px; font-weight:bold; margin:0'>중고시세: {carPrice}</p>
#             </div>
#             <div>
#                 <p style='font-size:15px; font-weight:bold; margin:0'>차량연식: {selected_year}</p>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd

st.markdown("""
<style>
@media screen and (max-width: 768px) {
    .mobileWrap {
        flex-wrap: wrap;
    }
}
</style>
""", unsafe_allow_html=True)

def card(data):
    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # 예외 처리: 데이터가 없으면 표시 안 함
    if df.empty:
        st.warning("선택된 데이터를 찾을 수 없습니다.")
        return
    
    row = df.iloc[0]

    # HTML 카드 출력
    st.markdown(f"""
    <div class="mobileWrap" style="display: flex; flex-wrap: wrap; gap: 10px; border:1px solid #ddd; padding:10px; border-radius:10px;">
        <div style="flex: 1 1 150px; min-width:150px;">
            <img src="{row.get('carClassRepImage','')}" style="width:90%; border-radius:5px; margin-left:0.8rem;">
        </div>
        <div style="flex: 2 1 200px; min-width:200px; display:flex; flex-direction: column; gap:10px; margin-left:1rem;">
            <div style="display:flex; gap:8px; align-items:center;">
                <div style="flex:1; max-width:60px;">
                    <img src="{row.get('brandImage','')}" style="width:100%; border-radius:5px;">
                </div>
                <div style="flex:3; display:flex; align-items:center;">
                    <p style='font-size:20px; font-weight:bold; margin:0; line-height:1.2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{row.get('carClassNm','')}</p>
                </div>
            </div>
            <div>
                <p style='font-size:15px; font-weight:normal; margin:0'>중고시세: {row.get('carPrice','')}</p>
            </div>
            <div>
                <p style='font-size:15px; font-weight:normal; margin:0'>차량연식: {row.get('yearType','')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
