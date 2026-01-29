import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from datetime import datetime

# Import custom backend modules 
# (Ensure these files exist in your /backend directory)
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

# Professional Banking UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #238636; color: white; border: none; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENT DATA INGESTION ---
@st.cache_data
def load_data():
    # Load primary datasets
    inv = pd.read_csv('data/invoices.csv')
    bank = pd.read_csv('data/bank_feed.csv')
    
    # Date Preprocessing
    inv['Due_Date'] = pd.to_datetime(inv['Due_Date'])
    inv['Month_Year'] = inv['Due_Date'].dt.strftime('%b %Y')
    inv['Month_Numeric'] = inv['Due_Date'].dt.month
    
    return inv, bank

# --- 3. ANALYTICAL FUNCTIONS ---
def calculate_dso(inv_df):
    """Calculates Days Sales Outstanding (AR / Total Sales * 365)"""
    ar_balance = inv_df[inv_df['Status'] == 'Open']['Amount'].sum()
    total_sales = inv_df['Amount'].sum()
    return (ar_balance / total_sales) * 365 if total_sales > 0 else 0

def get_dso_forecast(inv_df):
    """Uses Scipy to project DSO drift using Linear Regression"""
    # Create a historical trend (mocked x-axis for months)
    x = np.array([1, 2, 3, 4, 5]) 
    y = np.array([45.2, 44.8, 46.1, 43.9, 42.5]) # Sample historical DSO data
    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
    return slope, intercept, r_val**2

# --- 4. SESSION STATE & ORCHESTRATION ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

invoices, bank_feed = load_data()
engine = SmartMatchingEngine()

# --- 5. SIDEBAR NAVIGATION & CONTROLS ---
st.sidebar.image("https://img.icons8.com/fluency/96/shield-with-dollar.png", width=60)
st.sidebar.title("SmartCash AI")
st.sidebar.markdown("**Institutional Treasury Hub**")
st.sidebar.divider()

# Navigation
menu = st.sidebar.radio(
    "Navigation Center", 
    ["Executive Dashboard", "Analyst Workbench", "Risk & Governance", "Audit Ledger"]
)

st.sidebar.divider()

# --- STRESS TEST SLIDER ---
st.sidebar.subheader("🛠️ Macro Stress Controls")
stress_level = st.sidebar.slider(
    "Collection Latency (Days)", 
    0, 90, 0,
    help="Simulates global payment slowdowns using Numpy."
)

# Numpy-calculated collection efficiency haircut
# 0 days = 1.0 (100% efficient), 90 days = 0.55 (55% efficiency)
liquidity_haircut = np.clip(1 - (stress_level / 200), 0.55, 1.0)

st.sidebar.info(f"🟢 **System:** Operational\n\n📅 **Date:** {datetime.now().strftime('%Y-%m-%d')}")

# --- 6. EXECUTIVE DASHBOARD ---
if menu == "Executive Dashboard":
    st.title("📊 Global Cash & Liquidity Position")
    
    # Real-time Metrics
    base_dso = calculate_dso(invoices)
    current_dso = base_dso + stress_level
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{current_dso:.1f} Days", f"+{stress_level} Stress" if stress_level > 0 else "Optimal", delta_color="inverse")
    m2.metric("Liquidity Buffer", f"{liquidity_haircut*100:.1f}%", f"{(liquidity_haircut-1)*100:.1f}%")
    m3.metric("Cash Position", f"${(1200000 * liquidity_haircut)/1e6:.2f}M", "-4.2% Volatility")
    m4.metric("AI Match Rate", "94.8%", "+0.5%")

    st.divider()

    c1, c2 = st.columns([1.5, 1])

    with c1:
        st.subheader("📉 Liquidity Bridge (Stress-Adjusted)")
        
        # Dynamic Waterfall logic based on Haircut
        opening_bal = 1200000
        new_inv = invoices[invoices['Status'] == 'Open']['Amount'].sum()
        actual_collections = invoices[invoices['Status'] == 'Paid']['Amount'].sum() * liquidity_haircut
        
        fig_waterfall = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "total", "relative", "total"],
            x = ["Opening Cash", "New Receivables", "Gross Liquidity", "Collections (Adj)", "Net Position"],
            y = [opening_bal, new_inv, 0, -actual_collections, 0],
            connector = {"line":{"color":"#30363d"}},
            decreasing = {"marker":{"color":"#f85149"}},
            increasing = {"marker":{"color":"#2ea043"}},
            totals = {"marker":{"color":"#1f6feb"}}
        ))
        fig_waterfall.update_layout(template="plotly_dark", height=450, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_waterfall, use_container_width=True)
        

    with c2:
        st.subheader("🔮 Predictive DSO Drift")
        slope, intercept, r_sq = get_dso_forecast(invoices)
        
        months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        forecast_x = np.arange(len(months))
        # Project line: y = mx + c (plus the stress level drift)
        forecast_y = (intercept + slope * forecast_x) + stress_level
        
        fig_forecast = px.line(x=months, y=forecast_y, markers=True, template="plotly_dark")
        fig_forecast.add_vrect(x0="Jan", x1="Mar", fillcolor="#238636", opacity=0.1, annotation_text="AI Forecast")
        fig_forecast.update_traces(line_color='#2ea043', line_width=4)
        st.plotly_chart(fig_forecast, use_container_width=True)
        st.caption(f"Statistical Confidence ($R^2$): {r_sq:.4f}")

# --- 7. ANALYST WORKBENCH ---
elif menu == "Analyst Workbench":
    st.title("⚡ Smart Reconciliation Workbench")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)

    st.divider()
    col_sel, col_match = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Step 1: Focus Item")
        tx_id = st.selectbox(
            "Select Transaction:",
            bank_feed.index,
            format_func=lambda x: f"{bank_feed.iloc[x]['Bank_TX_ID']} | {bank_feed.iloc[x]['Payer_Name']}"
        )
        tx_data = bank_feed.iloc[tx_id]
        st.info(f"**Amount:** {tx_data['Currency']} {tx_data['Amount_Received']:,.2f}")

    with col_match:
        st.subheader("Step 2: AI Execution")
        if st.button("Run Multi-Factor Match"):
            matches = engine.run_match(tx_data['Amount_Received'], tx_data['Payer_Name'], tx_data['Currency'], invoices)
            if matches:
                top_match = matches[0]
                if top_match['confidence'] >= 0.95:
                    st.success(f"STP MATCH CONFIRMED ({top_match['confidence']*100}%)")
                    st.balloons()
                    st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "AUTO_STP")
                else:
                    st.warning("Low Confidence Exception. Drafting AI Email...")
                    agent = GenAIAssistant()
                    st.text_area("Draft:", agent.generate_email(top_match['Customer'], tx_data['Amount_Received']), height=150)

# --- 8. RISK & AUDIT SECTIONS ---
elif menu == "Risk & Governance":
    st.title("🛡️ Institutional Risk Radar")
    # Sunburst for concentration risk
    fig_sun = px.sunburst(invoices, path=['Currency', 'Customer', 'ESG_Score'], values='Amount', template="plotly_dark")
    st.plotly_chart(fig_sun, use_container_width=True)
    

elif menu == "Audit Ledger":
    st.title("🔐 SOC2 Compliance Vault")
    st.dataframe(st.session_state.audit_engine.get_logs(), use_container_width=True)
