import os
import sys
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# --- PATH & BACKEND INTEGRATION ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.engine import SmartMatchingEngine
from backend.compliance import ComplianceVault
from backend.analytics import TreasuryAnalytics

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(
    page_title="SmartCash AI | Treasury Command", 
    page_icon="🏦", 
    layout="wide"
)

# Professional Institutional Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #58a6ff; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #161b22; border-radius: 4px 4px 0 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RESOURCE INITIALIZATION ---
# Change @st.cache_data to @st.cache_data(ttl=1) to force refresh every second during dev
@st.cache_data(ttl=1) 
def load_data():
    try:
        inv = pd.read_csv('data/invoices.csv')
        bank = pd.read_csv('data/bank_feed.csv')
        
        # LOGGING: This prints to your terminal so you can see if columns exist
        print(f"DEBUG: Invoice Columns: {inv.columns.tolist()}")
        
        return inv, bank
    except Exception as e:
        st.error(f"⚠️ Data Source Error: {e}")
        return pd.DataFrame(), pd.DataFrame()    

# Persistent Session Objects
if 'engine' not in st.session_state:
    st.session_state.engine = SmartMatchingEngine()
if 'vault' not in st.session_state:
    st.session_state.vault = ComplianceVault()
if 'analytics' not in st.session_state:
    st.session_state.analytics = TreasuryAnalytics()

invoices, bank_feed = load_data()

# --- 3. SIDEBAR: MACRO CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    st.title("SmartCash AI")
    st.caption("Institutional Liquidity Management v1.0")
    st.divider()
    
    st.subheader("🛠️ Stress Parameters")
    latency_days = st.slider("Collection Latency (Days)", 0, 90, 15)
    
    entity = st.selectbox("Company Entity", ["All Entities", "US01", "EU10", "AP20"])
    if entity != "All Entities":
        invoices = invoices[invoices['Company_Code'] == entity]
        bank_feed = bank_feed[bank_feed['Company_Code'] == entity]
    
    st.divider()
    st.info(f"🟢 **System Status: Secure**\n\n**Vault Ref:** {datetime.now().strftime('%H%M%S')}-TXN")

# --- 4. TOP-LEVEL METRICS ---
m1, m2, m3, m4 = st.columns(4)
# Ensure engine has calculate_dso method
base_dso = st.session_state.engine.calculate_dso(invoices) if not invoices.empty else 0
m1.metric("Adjusted DSO", f"{base_dso + latency_days:.1f} Days", f"+{latency_days}d Latency", delta_color="inverse")
m2.metric("Matching STP Rate", "94.2%", "+1.4% WoW")
m3.metric("ESG Risk Exposure", "Medium", "Tier B Avg", delta_color="off")
m4.metric("Vault Health", "Verified", "SHA-256 Active")

st.divider()

# --- 5. MAIN NAVIGATION TABS ---
tab_exec, tab_workbench, tab_risk, tab_audit = st.tabs([
    "📈 Executive Dashboard", 
    "⚡ Analyst Workbench", 
    "🛡️ Risk Radar", 
    "📜 Audit Ledger"
])

# --- TAB 1: EXECUTIVE DASHBOARD ---
with tab_exec:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("💧 Liquidity Bridge (Stress-Adjusted)")
        if not invoices.empty:
            waterfall_data = st.session_state.analytics.get_waterfall_data(invoices, latency_days)
            fig_waterfall = go.Figure(go.Waterfall(
                orientation = "v",
                measure = waterfall_data["measure"],
                x = waterfall_data["x"],
                y = waterfall_data["y"],
                connector = {"line":{"color":"#30363d"}},
                decreasing = {"marker":{"color":"#f85149"}},
                increasing = {"marker":{"color":"#3fb950"}},
                totals = {"marker":{"color":"#1f6feb"}}
            ))
            fig_waterfall.update_layout(template="plotly_dark", height=450, margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fig_waterfall, use_container_width=True)
        else:
            st.warning("No data available for waterfall.")

    with c2:
        st.subheader("📅 Cash Flow Forecast")
        months = ["Dec", "Jan", "Feb", "Mar"]
        forecast = [42, 45, 48 + (latency_days/2), 52 + latency_days]
        fig_forecast = px.line(x=months, y=forecast, markers=True, template="plotly_dark")
        fig_forecast.update_traces(line_color="#58a6ff", line_width=4)
        st.plotly_chart(fig_forecast, use_container_width=True)

# --- TAB 2: ANALYST WORKBENCH (Corrected Column Names) ---
with tab_workbench:
    st.subheader("📥 Active Bank Feed")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)
    
    st.divider()
    if not bank_feed.empty:
        w1, w2 = st.columns([1, 2])
        with w1:
            st.subheader("Step 1: Focus Item")
            tx_selection = st.selectbox(
                "Select Bank Transaction", 
                bank_feed.index, 
                format_func=lambda x: f"{bank_feed.iloc[x]['Payer_Name']} | {bank_feed.iloc[x]['Amount_Received']}"
            )
            tx = bank_feed.iloc[tx_selection]
            st.info(f"**Target:** {tx['Payer_Name']} | **Sum:** {tx['Currency']} {tx['Amount_Received']:,.2f}")

        with w2:
            st.subheader("Step 2: AI Match Execution")
            if st.button("🔥 Execute Multi-Factor Matching"):
                # Pass Amount_Received to the engine
                results = st.session_state.engine.run_match(tx['Amount_Received'], tx['Payer_Name'], tx['Currency'], invoices)
                
                if results:
                    match = results[0]
                    conf = match['confidence']
                    
                    if conf >= 0.95:
                        st.success(f"✅ **STP MATCH FOUND: {conf*100:.1f}% Confidence**")
                        st.balloons()
                        st.session_state.vault.log_action(match['Invoice_ID'], "AUTO_MATCH_STP", tx['Amount_Received'])
                    else:
                        st.warning(f"⚠️ **EXCEPTION: Low Confidence ({conf*100:.1f}%)**")
                        with st.expander("🤖 GenAI Remittance Assistant", expanded=True):
                            st.markdown("Confidence score below threshold. AI suggests a clarification request:")
                            email_draft = f"Subject: Payment Discrepancy - {tx['Payer_Name']}\n\nDear Accounts Payable,\n\nWe received your payment of {tx['Amount_Received']} but are unable to auto-reconcile it..."
                            st.text_area("Draft Communication", value=email_draft, height=180)
                            st.button("✉️ Dispatch Email")
                else:
                    st.error("❌ No suitable candidates found in Ledger.")
    else:
        st.info("No bank feed data available for the current filter.")

# --- TAB 3: RISK RADAR ---
with tab_risk:
    st.subheader("🌎 Institutional Risk Exposure (ESG Weighted)")
    
    # Define the required columns for the visualization
    required_risk_cols = ['Company_Code', 'Currency', 'ESG_Score', 'Amount']
    
    # Check if all columns exist in the dataframe
    if all(col in invoices.columns for col in required_risk_cols):
        fig_sun = px.sunburst(
            invoices, 
            path=['Company_Code', 'Currency', 'ESG_Score'], 
            values='Amount',
            color='ESG_Score',
            color_discrete_map={
                'AA': '#238636', 
                'A': '#2ea043', 
                'B': '#d29922', 
                'C': '#f85149',
                'N/A': '#30363d'
            },
            template="plotly_dark"
        )
        fig_sun.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)
    else:
        st.warning("⚠️ Risk Radar Unavailable: Missing ESG metadata columns.")
        st.info("Please ensure 'mock_data_maker.py' has been run to generate the latest institutional dataset.")
        # Debugging view for the developer
        st.write("Available Columns:", list(invoices.columns))

# --- TAB 4: AUDIT LEDGER ---
with tab_audit:
    st.subheader("🔐 SOC2 Compliance Vault (Immutable)")
    st.info("The ledger below is a real-time feed from the SHA-256 Hashed Audit CSV.")
    logs = st.session_state.vault.get_logs()
    st.dataframe(logs, use_container_width=True, hide_index=True)
