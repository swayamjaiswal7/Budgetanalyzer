import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
st.title("Expenses and Budget Analyzer")

# Add Expense Form
with st.form("expense_form"):
    st.write("Add New Expense")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Books", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0)
    date = st.date_input("Date")
    submit_button = st.form_submit_button("Add Expense")

# Store Expenses
if submit_button:
    new_expense = pd.DataFrame([{"Category": category, "Amount": amount, "Date": date}])
    if "expenses" not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date"])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    
    # Ensure the "Date" column is of datetime type
    st.session_state.expenses["Date"] = pd.to_datetime(st.session_state.expenses["Date"])
    
    st.success("Expense added successfully!")

# Display Expenses
if "expenses" in st.session_state:
    st.write("### Your Expenses")
    st.dataframe(st.session_state.expenses)

# Visualize Spending
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    st.write("### Spending by Category")
    category_totals = st.session_state.expenses.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# Budget Feature
budget = st.slider("Set Monthly Budget (₹)", min_value=0, max_value=100000, value=5000)
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    total_expenses = st.session_state.expenses["Amount"].sum()
    st.write(f"### Total Expenses: ₹{total_expenses}")
    if total_expenses > budget:
        st.error("You have exceeded your budget!")
    else:
        st.success(f"You are within your budget. Remaining: ₹{budget - total_expenses}")

# Save and Load Data
if st.button("Save Expenses to CSV"):
    st.session_state.expenses.to_csv("expenses.csv", index=False)
    st.success("Expenses saved to expenses.csv")

uploaded_file = st.file_uploader("Upload Expenses CSV", type=["csv"])
if uploaded_file is not None:
    st.session_state.expenses = pd.read_csv(uploaded_file)
    
    # Ensure the "Date" column is of datetime type after loading CSV
    st.session_state.expenses["Date"] = pd.to_datetime(st.session_state.expenses["Date"])
    
    st.success("Expenses loaded successfully!")
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    # Total and Average monthly expenses
    total_expenses = st.session_state.expenses["Amount"].sum()
    avg_expense = st.session_state.expenses.groupby(st.session_state.expenses["Date"].dt.month)["Amount"].mean().mean()
    st.write(f"### Total Expenses: ₹{total_expenses}")
    st.write(f"### Average Monthly Expense: ₹{avg_expense}")
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    st.write("### Expense Trend Over Time")
    st.session_state.expenses["Month"] = st.session_state.expenses["Date"].dt.to_period("M")
    monthly_expenses = st.session_state.expenses.groupby("Month")["Amount"].sum()
    
    fig, ax = plt.subplots()
    monthly_expenses.plot(kind="line", ax=ax)
    ax.set_title("Monthly Expenses Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    st.write("### Category-Based Spending Distribution")
    category_totals = st.session_state.expenses.groupby("Category")["Amount"].sum()
    st.write(category_totals)
    
    # Plotting
    fig, ax = plt.subplots()
    category_totals.plot(kind="bar", ax=ax)
    ax.set_title("Spending by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    st.write("### Category-wise Spending Per Month")
    selected_category = st.selectbox("Select Category", st.session_state.expenses["Category"].unique())
    category_monthly_spending = st.session_state.expenses[st.session_state.expenses["Category"] == selected_category].groupby("Month")["Amount"].sum()

    fig, ax = plt.subplots()
    category_monthly_spending.plot(kind="bar", ax=ax)
    ax.set_title(f"{selected_category} Spending Per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)
if "expenses" in st.session_state and not st.session_state.expenses.empty:
    st.write("### Outlier Detection (Expenses greater than 1.5 * IQR)")
    
    # Calculate IQR (Interquartile Range) to detect outliers
    Q1 = st.session_state.expenses["Amount"].quantile(0.25)
    Q3 = st.session_state.expenses["Amount"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = st.session_state.expenses[(st.session_state.expenses["Amount"] < lower_bound) | (st.session_state.expenses["Amount"] > upper_bound)]
    if not outliers.empty:
        st.write("Outliers detected:")
        st.write(outliers)
    else:
        st.write("No outliers detected.")

if "expenses" in st.session_state and not st.session_state.expenses.empty:
    total_expenses = st.session_state.expenses["Amount"].sum()
    spending_to_budget_ratio = total_expenses / budget
    st.write(f"### Spending-to-Budget Ratio: {spending_to_budget_ratio:.2f}")
    if spending_to_budget_ratio > 1:
        st.error("You have exceeded your budget!")
    else:
        st.success(f"You are within your budget. ({spending_to_budget_ratio * 100:.2f}% spent)")
