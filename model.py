import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="💹 Trade Profit Reinvestment Calculator", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
/* Background and font */
body {
    background-color: #f9fafc;
    color: #222;
    font-family: 'Inter', sans-serif;
}
.main {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 18px;
    padding: 30px 50px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

/* Headings */
h1, h2, h3 {
    color: #2c3e50;
    font-weight: 700;
}

/* Buttons */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #00b09b, #96c93d);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 16px;
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #96c93d, #00b09b);
}

/* Cards for summary */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    transition: all 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: #27ae60;
}
.metric-label {
    font-size: 14px;
    color: #7f8c8d;
}

/* Table styling */
table {
    border-collapse: collapse;
    width: 100%;
}
thead {
    background-color: #00b09b !important;
    color: white !important;
}
tbody tr:hover {
    background-color: #f1fdf7 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align:center;'>💹 Trade Profit Reinvestment & Savings Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7f8c8d;'>Track your daily reinvested profits and savings growth effortlessly 📈</p>", unsafe_allow_html=True)

st.markdown("---")

# --- Inputs Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    principal = st.number_input("💵 Enter Principal Amount (₹)", min_value=100.0, value=10000.0, step=100.0)

with col2:
    days = st.number_input("📆 Number of Days", min_value=1, value=10, step=1)

with col3:
    daily_percent = st.number_input("📈 Daily Profit %", min_value=0.1, value=5.0, step=0.1)

st.markdown("")

# --- Calculation Button ---
center = st.columns([4, 1, 4])[1]
with center:
    calculate = st.button("🚀 Calculate Growth")

# --- Core Logic ---
if calculate:
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

    # --- Results Section ---
    st.markdown("---")
    st.subheader("📊 Daily Growth Table")
    st.dataframe(df, use_container_width=True, height=400)

    # 💾 Save to CSV Option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Save Table as CSV",
        data=csv,
        file_name="trade_growth_data.csv",
        mime="text/csv",
    )

    # --- Summary Section ---
    st.markdown("---")
    st.subheader("💼 Summary Overview")

    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{round(current_principal, 2):,}</div>
            <div class='metric-label'>Final Principal (after {int(days)} days)</div>
        </div>
        """, unsafe_allow_html=True)

    with colB:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{round(total_savings, 2):,}</div>
            <div class='metric-label'>Total Saved in Bank</div>
        </div>
        """, unsafe_allow_html=True)

    with colC:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{round(current_principal + total_savings, 2):,}</div>
            <div class='metric-label'>Total Combined Value</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Chart ---
    st.markdown("### 📈 Growth Visualization")
    st.line_chart(df.set_index("Day")[["New Principal (₹)", "Profit (₹)"]])

    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#95a5a6;'>👨‍💻 Created with ❤️ by <b>Yash Sharma</b></p>", unsafe_allow_html=True)
