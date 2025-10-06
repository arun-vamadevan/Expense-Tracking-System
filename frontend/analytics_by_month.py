import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import calendar

APP_URL = "http://127.0.0.1:8000/"

def analytics_month_tab():
    st.write("Monthly Analytics")
    response = requests.get(f"{APP_URL}/analytics/month")
    response = response.json()

    data = {
        "month": [calendar.month_name[item['month']] for item in response],
        "Expenditure": [item['total_amount'] for item in response]
    }
    df = pd.DataFrame(data)
    df['month'] = pd.Categorical(df["month"], categories=df["month"].unique(), ordered=True)
    st.bar_chart(df.set_index('month')['Expenditure'])
    
    st.table(df)