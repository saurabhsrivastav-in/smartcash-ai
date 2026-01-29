import os
import sys
from datetime import datetime

# --- PATH CONFIGURATION ---
# This ensures 'backend' can be imported regardless of execution context
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Core Backend Logic
from backend.engine import SmartMatchingEngine
from backend.compliance import ComplianceGuard
from backend.treasury import TreasuryManager
from backend.ai_agent import GenAIAssistant

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(
    page_title="SmartCash AI | Treasury Command", 
    page_icon="🏦", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark-Mode Banking UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #238636; color: white; border: none; font-weight: bold; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA INGESTION ENGINE ---
@st.cache_data
def load_data():
    try:
        inv = pd.read_csv('data/invoices.csv')
        bank = pd.read_csv('data/bank_feed.csv')
        
        # Format Processing
        inv['Due_Date'] = pd.to_datetime(inv['Due_Date'])
        inv['Month_Numeric'] = inv['Due_Date'].dt.month
        return inv, bank
    except FileNotFoundError:
        st.error("⚠️ Data Source Missing: Check 'data/invoices.csv' and 'data/bank_feed.csv'")
        return pd.DataFrame(), pd.DataFrame()

# --- 3. ANALYTICAL LAYER ---
def calculate_dso(inv_df):
    """Real-time calculation of Days Sales Outstanding"""
    ar_balance = inv_df[inv_df['Status'] == 'Open']['Amount'].sum()
    total_sales = inv_df['Amount'].sum()
    return (ar_balance / total_sales) * 365 if total_sales > 0 else 0

def get_dso_forecast(inv_df, stress):
    """Predictive trend modeling using Linear Regression"""
    x = np.array([1, 2, 3, 4, 5]) 
    y = np.array([45.2, 44.8, 46.1, 43.9, 42.5]) # Historical baseline
    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
    return slope, intercept, r_val**2

# --- 4. SESSION ORCHESTRATION ---
@st.cache_resource
def get_engine():
    """Caches the engine to keep fuzzy matching snappy for the demo"""
    return SmartMatchingEngine()

# Initialize session-based components
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

# Load Data and Engine
invoices, bank_feed = load_data()
engine = get_engine()

# --- 5. SIDEBAR NAVIGATION & CONTROLS ---
st.sidebar.image("https://img.icons8.com/fluency/96/shield-with-dollar.png", width=60)
st.sidebar.title("SmartCash AI")
st.sidebar.markdown("**Institutional Treasury Hub**")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation Center", 
    ["Executive Dashboard", "Analyst Workbench", "Risk & Governance", "Audit Ledger"]
)

st.sidebar.divider()
st.sidebar.subheader("🛠️ Macro Stress Controls")
stress_level = st.sidebar.slider(
    "Collection Latency (Days)", 0, 90, 0,
    help="Simulates a global slowdown in credit payment cycles using Numpy."
)

# Numpy-calculated collection efficiency haircut for the waterfall
liquidity_haircut = np.clip(1 - (stress_level / 200), 0.55, 1.0)

# --- 6. VIEW: EXECUTIVE DASHBOARD ---
if menu == "Executive Dashboard":
    st.title("📊 Global Cash & Liquidity Position")
    
    # KPIs with Real-time Stress Impact
    base_dso = calculate_dso(invoices)
    current_dso = base_dso + stress_level
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{current_dso:.1f} Days", f"+{stress_level} Stress", delta_color="inverse")
    m2.metric("Liquidity Buffer", f"{liquidity_haircut*100:.1f}%", f"{(liquidity_haircut-1)*100:.1f}%")
    m3.metric("Available Cash", f"${(1200000 * liquidity_haircut)/1e6:.2f}M", "-4.2% Volatility")
    m4.metric("AI Confidence", "94.8%", "Target >90%")

    st.divider()
    c1, c2 = st.columns([1.5, 1])

    with c1:
        st.subheader("📉 Liquidity Bridge (Stress-Adjusted)")
        opening_bal = 1200000
        new_inv = invoices[invoices['Status'] == 'Open']['Amount'].sum()
        actual_coll = invoices[invoices['Status'] == 'Paid']['Amount'].sum() * liquidity_haircut
        
        fig_waterfall = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "total", "relative", "total"],
            x = ["Opening Cash", "Expected AR", "Gross Liquidity", "Collections (Stressed)", "Net Position"],
            y = [opening_bal, new_inv, 0, -actual_coll, 0],
            connector = {"line":{"color":"#30363d"}},
            decreasing = {"marker":{"color":"#f85149"}},
            increasing = {"marker":{"color":"#2ea043"}},
            totals = {"marker":{"color":"#1f6feb"}}
        ))
        fig_waterfall.update_layout(template="plotly_dark", height=450, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_waterfall, use_container_width=True)
        

    with c2:
        st.subheader("🔮 Predictive DSO Drift")
        slope, intercept, r_sq = get_dso_forecast(invoices, stress_level)
        months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        forecast_x = np.arange(len(months))
        forecast_y = (intercept + slope * forecast_x) + stress_level
        
        fig_line = px.line(x=months, y=forecast_y, markers=True, template="plotly_dark")
        fig_line.add_vrect(x0="Jan", x1="Mar", fillcolor="#238636", opacity=0.1, annotation_text="Forecast Window")
        fig_line.update_traces(line_color='#2ea043', line_width=4)
        st.plotly_chart(fig_line, use_container_width=True)

# --- 7. VIEW: ANALYST WORKBENCH ---
elif menu == "Analyst Workbench":
    st.title("⚡ Smart Reconciliation Workbench")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)

    st.divider()
    col_sel, col_match = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Step 1: Focus Item")
        tx_id = st.selectbox("Select Transaction:", bank_feed.index, 
                            format_func=lambda x: f"{bank_feed.iloc[x]['Bank_TX_ID']} | {bank_feed.iloc[x]['Payer_Name']}")
        tx_data = bank_feed.iloc[tx_id]
        st.info(f"**Selected Amount:** {tx_data['Currency']} {tx_data['Amount_Received']:,.2f}")

    with col_match:
        st.subheader("Step 2: AI Match Execution")
        if st.button("Run Multi-Factor Match Engine"):
            matches = engine.run_match(tx_data['Amount_Received'], tx_data['Payer_Name'], tx_data['Currency'], invoices)
            if matches:
                top = matches[0]
                if top['confidence'] >= 0.95:
                    st.success(f"✅ STP MATCH CONFIRMED ({top['confidence']*100}%)")
                    st.balloons()
                    st.session_state.audit_engine.log_transaction(top['Invoice_ID'], "AUTO_STP")
                else:
                    st.warning(f"⚠️ EXCEPTION: Match Confidence {top['confidence']*100}%")
                    agent = GenAIAssistant()
                    st.text_area("AI Remittance Request Draft:", agent.generate_email(top['Customer'], tx_data['Amount_Received']), height=200)
            else:
                st.error("Critical Failure: No matching entities found.")

# --- 8. VIEW: RISK & AUDIT ---
elif menu == "Risk & Governance":
    st.title("🛡️ Institutional Risk Radar")
    fig_sun = px.sunburst(invoices, path=['Currency', 'Customer', 'ESG_Score'], 
                         values='Amount', template="plotly_dark", color='ESG_Score')
    st.plotly_chart(fig_sun, use_container_width=True)
    

elif menu == "Audit Ledger":
    st.title("🔐 SOC2 Compliance Vault")
    st.dataframe(st.session_state.audit_engine.get_logs(), use_container_width=True)

# Footer info
st.sidebar.divider()
st.sidebar.info(f"🟢 **Session Active**\n\n📅 **Date:** {datetime.now().strftime('%Y-%m-%d')}")
