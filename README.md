https://budgetanalyzere.streamlit.app/
# 💸 BudgetAnalyzer

A Python-based application to help users track their expenses, analyze spending patterns, and improve financial habits with data-driven insights.

---

## 🎯 Objective

To provide an intuitive and interactive way for users to record their income and expenses, categorize them, and visualize their budget utilization over time.

---

## 🧾 Features

- 📥 **Income & Expense Input**: Users can add transactions with category, amount, and date.
- 📊 **Category-Wise Analysis**: See how much you're spending on essentials, leisure, savings, etc.
- 📈 **Monthly Trend Graphs**: Visual charts to monitor your budgeting performance month over month.
- ⚙️ **Real-time Calculations**: Calculates net savings, total spending, and category percentages.
- 🔄 **Reset/Update Budget**: Easily reset or adjust your budget parameters as per changing goals.

---

## 🛠️ Tech Stack

- **Python** (Core logic and calculations)
- **Streamlit** (UI/UX interface)
- **Pandas** (Data handling and manipulation)
- **Matplotlib / Plotly** (for visual analytics)

---

## 🗂️ File Structure

- `app.py` – Main application file
- `data/` – Directory for saving transactions (if applicable)
- `requirements.txt` – Dependencies for setting up the app

---

```bash
pip install -r requirements.txt
streamlit run app.py
