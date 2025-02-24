import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Streamlit App Title
st.title("📊 Student Budget Analyzer")
st.write("Manage your expenses efficiently and track your budget!")

# Initialize session state for expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount", "Date"])

# Add Expense Form
st.sidebar.header("➕ Add New Expense")
with st.sidebar.form("expense_form"):
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Books", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0, step=10)
    date = st.date_input("Date")
    submit_button = st.form_submit_button("Add Expense")

if submit_button:
    new_expense = pd.DataFrame([{"Category": category, "Amount": amount, "Date": date}])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    st.session_state.expenses["Date"] = pd.to_datetime(st.session_state.expenses["Date"])
    st.success("Expense added successfully!")

# Display Expenses & Delete Feature
st.write("### 📄 Your Expenses")
if not st.session_state.expenses.empty:
    expenses_df = st.session_state.expenses.copy()
    expenses_df.index = range(1, len(expenses_df) + 1)
    
    # Select expenses to delete
    delete_selection = st.multiselect("Select expenses to delete:", expenses_df.index.tolist())
    if st.button("🗑 Delete Selected Expenses") and delete_selection:
        st.session_state.expenses.drop(delete_selection, inplace=True)
        st.session_state.expenses.reset_index(drop=True, inplace=True)
        st.success("Selected expenses deleted!")
    
    st.dataframe(expenses_df)

# Budget Tracking
st.sidebar.header("💰 Budget Management")
budget = st.sidebar.slider("Set Monthly Budget (₹)", min_value=0, max_value=100000, value=5000)
total_expenses = st.session_state.expenses["Amount"].sum() if not st.session_state.expenses.empty else 0

st.write(f"### 💵 Total Expenses: ₹{total_expenses}")
if total_expenses > budget:
    st.error("⚠️ You have exceeded your budget!")
else:
    st.success(f"✅ You are within budget. Remaining: ₹{budget - total_expenses}")

# Visualizing Spending Patterns
if not st.session_state.expenses.empty:
    st.write("### 📊 Spending Breakdown")
    category_totals = st.session_state.expenses.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
    ax.axis("equal")
    st.pyplot(fig)

    # Expense Trend Over Time
    st.write("### 📈 Expense Trend Over Time")
    st.session_state.expenses["Month"] = st.session_state.expenses["Date"].dt.to_period("M")
    monthly_expenses = st.session_state.expenses.groupby("Month")["Amount"].sum()
    
    fig, ax = plt.subplots()
    monthly_expenses.plot(kind="line", marker="o", ax=ax, color="blue")
    ax.set_title("Monthly Expenses Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)

# Save & Load Data
st.sidebar.header("📂 Save & Load Data")
if st.sidebar.button("💾 Save Expenses to CSV"):
    st.session_state.expenses.to_csv("expenses.csv", index=False)
    st.sidebar.success("Expenses saved successfully!")

uploaded_file = st.sidebar.file_uploader("📤 Upload Expenses CSV", type=["csv"])
if uploaded_file is not None:
    st.session_state.expenses = pd.read_csv(uploaded_file)
    st.session_state.expenses["Date"] = pd.to_datetime(st.session_state.expenses["Date"])
    st.sidebar.success("Expenses loaded successfully!")

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
