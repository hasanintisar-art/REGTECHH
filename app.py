# app.py
import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Personal Budget", layout="centered")

st.title("Personal Budget Tracker")

# Sidebar: monthly settings
st.sidebar.header("Settings")
month = st.sidebar.selectbox("Month", ["January","February","March","April","May","June",
                                       "July","August","September","October","November","December"])
year = st.sidebar.number_input("Year", min_value=2000, max_value=2100, value=2026, step=1)

# Income inputs
st.header("Income")
base_salary = st.number_input("Salary (base)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
other_income = st.number_input("Other income (freelance, interest...)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
total_income = base_salary + other_income
st.markdown(f"**Total Income:** ${total_income:,.2f}")

# Expenses entry form
st.header("Expenses")
with st.form(key="expense_form", clear_on_submit=True):
    col1, col2 = st.columns([2,1])
    with col1:
        desc = st.text_input("Description (e.g., Groceries, Dine-out, Rent)")
    with col2:
        category = st.selectbox("Category", ["Groceries", "Food", "Dine-outs", "Transport", "Rent", "Utilities", "Other"])
    amount = st.number_input("Amount ($)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    submitted = st.form_submit_button("Add expense")
    if submitted and desc and amount > 0:
        if "expenses" not in st.session_state:
            st.session_state.expenses = []
        st.session_state.expenses.append({"description": desc, "category": category, "amount": float(amount)})
        st.success("Expense added")

# Initialize session state if empty
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Display expenses table and totals
st.subheader(f"Expenses for {month} {year}")
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df.style.format({"amount":"${:,.2f}"}), height=250)

    # Totals by category and overall
    totals_by_cat = df.groupby("category", as_index=False)["amount"].sum()
    total_expenses = totals_by_cat["amount"].sum()
    st.markdown(f"**Total Expenses:** ${total_expenses:,.2f}")
    st.markdown(f"**Net Savings (Income - Expenses):** ${total_income - total_expenses:,.2f}")

    # Chart
    st.subheader("Spending by Category")
    st.bar_chart(data=totals_by_cat.set_index("category"))

    # Download CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_str = csv_buffer.getvalue()
    st.download_button("Download expenses CSV", csv_str, file_name=f"expenses_{month}_{year}.csv", mime="text/csv")
else:
    st.info("No expenses added yet. Use the form above to add items.")

# Quick reset
if st.button("Clear all expenses"):
    st.session_state.expenses = []
    st.success("Expenses cleared")
