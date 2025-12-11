import streamlit as st


# ========== 네비게이션 (사이드바) ==================
pages = {
    "시세조회": [
        st.Page("checking.py", title="차량 시세조회"),
        st.Page("comparison.py", title="차량 비교"),
    ],
    "FAQ": [
        st.Page("faq.py", title="차량 FAQ"),
    ],
}

pg = st.navigation(pages, position="sidebar")

# 네비게이션 색상 수정 (상단 메뉴 + 사이드바)
st.markdown("""
    <style>
        /* 🔵 상단 메뉴(네비게이션) 전체 배경색 */
        header {background-color: #0047AB !important;}

        /* 🔵 사이드바 배경색 */
        section[data-testid="stSidebar"] {
            background-color: #0047AB !important;
        }

        /* 🌟 사이드바 글씨 색 */
        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* 🎯 사이드바 메뉴 hover 효과 */
        section[data-testid="stSidebar"] div:hover {
            background-color: #1565C0 !important;
            border-radius: 8px;
        }

        /* 🖤 상단 로고/텍스트 색 */
        header * {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)


pg.run()
# =================== 로 고 =======================
car_logo = "images/Car_value.png"
st.logo(car_logo, size="large", icon_image= car_logo)
# =================================================

