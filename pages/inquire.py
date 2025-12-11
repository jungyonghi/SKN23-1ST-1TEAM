import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pages.admin import admin_page
from pages.admin import inquiry_page


page = st.sidebar.radio("이동", ["문의하기", "관리자(문의 리스트)"])

if page == "문의하기":
    inquiry_page()
elif page == "관리자(문의 리스트)":
    admin_page()