import streamlit as st
from datetime import datetime
import requests

APP_URL = "http://127.0.0.1:8000/"

def add_update_tab():
    selected_date = st.date_input("Enter date: ", datetime(2024, 8, 1), label_visibility="collapsed")
    response = requests.get(f"{APP_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_response = response.json()
        # st.write(existing_response)
    else:
        st.write("failed to retrieve expenses")
        existing_response = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
    in_expenses = []
    with st.form(key="Expense_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        for i in range(5):

            if i < len(existing_response):
                amount = existing_response[i]["amount"]
                category = existing_response[i]["category"]
                notes = existing_response[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            with col1:
                amount_input = st.number_input(label="Amount", value=amount, min_value=0.0, step=1.0,
                                               key=f"{selected_date}_amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"{selected_date}_category_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", key=f"{selected_date}_notes_{i}", value=notes,
                                            label_visibility="collapsed")

            in_expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })
        submit_button = st.form_submit_button()
        if submit_button:
            filtered_exp = [item for item in in_expenses if item['amount'] > 0]

            response = requests.post(f"{APP_URL}/expenses/{selected_date}", json=filtered_exp)

            if response.status_code == 200:
                st.success("Expenses updated successfully!")
                st.balloons()
            else:
                st.error("Failed to update expense...")

            pass
