import streamlit as st
from add_update_tab import add_update_tab
from analytics_ui import analytics_tab
from analytics_by_month import analytics_month_tab

APP_URL = "http://127.0.0.1:8000/"

st.title("Expense Tracking System (ETS)")
st.write("Created by Arun")
tb1, tab2, tab3 = st.tabs(["ADD/UPDATE", "ANALYTICS", "MONTH ANALYTICS"])

with tb1:
    add_update_tab()
with tab2:
    analytics_tab()
with tab3:
    analytics_month_tab()