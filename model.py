import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trade Profit Reinvestment Calculator", layout="centered")

st.title(" Trade Profit Reinvestment & Savings Tracker")

st.markdown("""
This app helps you calculate how your **principal grows** when you reinvest 90% of your daily profits 
and save 10% of them into another account.
""")

# --- Inputs ---
col1, col2, col3 = st.columns(3)

with col1:
    principal = st.number_input("Enter Principal Amount (₹)", min_value=100.0, value=10000.0, step=100.0)

with col2:
    days = st.number_input("Number of Days", min_value=1, value=10, step=1)

with col3:
    daily_percent = st.number_input("Daily Profit %", min_value=0.1, value=5.0, step=0.1)

if st.button("Calculate Growth"):
    data = []
    total_savings = 0
    current_principal = principal

    for day in range(1, int(days) + 1):
        starting_principal = current_principal
        profit = starting_principal * (daily_percent / 100)
        saved = profit * 0.10
        reinvested = profit * 0.90
        total_savings += saved
        current_principal += reinvested

        data.append({
            "Day": day,
            "Starting Principal (₹)": round(starting_principal, 2),
            "Profit (₹)": round(profit, 2),
            "Saved (10%) (₹)": round(saved, 2),
            "Reinvested (90%) (₹)": round(reinvested, 2),
            "New Principal (₹)": round(current_principal, 2)
        })

    df = pd.DataFrame(data)

    st.subheader("📊 Daily Growth Table")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Summary")
    st.markdown(f"""
    - **Final Principal (after {int(days)} days)**: ₹{round(current_principal, 2):,}  
    - **Total Saved in Bank**: ₹{round(total_savings, 2):,}  
    - **Total Combined Value**: ₹{round(current_principal + total_savings, 2):,}
    """)

    st.line_chart(df.set_index("Day")[["New Principal (₹)", "Profit (₹)"]])

st.markdown("""
---
👨‍💻 *Created by Yash Sharma*  
""")
