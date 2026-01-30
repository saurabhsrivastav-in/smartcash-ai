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
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RESOURCE INITIALIZATION ---
@st.cache_data
def load_data():
    try:
        inv = pd.read_csv('data/invoices.csv')
        bank = pd.read_csv('data/bank_feed.csv')
        return inv, bank
    except Exception as e:
        st.error(f"⚠️ Data Source Missing: {e}")
        return pd.DataFrame(), pd.DataFrame()   

# Persistent Session Objects
if 'engine' not in st.session_state:
    st.session_state.engine = SmartMatchingEngine()
if 'vault' not in st.session_state:
    st.session_state.vault = ComplianceVault()
if 'analytics' not in st.session_state:
    st.session_state.analytics = TreasuryAnalytics()

invoices, bank_feed = load_data()

# --- 3. SIDEBAR: NAVIGATION & CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    st.title("SmartCash AI")
    st.caption("Institutional Liquidity Management v1.0")
    st.divider()
    
    # NEW NAVIGATION MENU
    st.subheader("🧭 Navigation")
    menu = st.radio(
        "Select Workspace",
        ["📈 Executive Dashboard", "⚡ Analyst Workbench", "🛡️ Risk Radar", "📜 Audit Ledger"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.subheader("🛠️ Stress Parameters")
    latency_days = st.slider("Collection Latency (Days)", 0, 90, 15)
    
    entity_list = ["All Entities"] + (invoices['Company_Code'].unique().tolist() if not invoices.empty else [])
    entity = st.selectbox("Company Entity", entity_list)
    
    if entity != "All Entities":
        invoices = invoices[invoices['Company_Code'] == entity]
        bank_feed = bank_feed[bank_feed['Company_Code'] == entity]
    
    st.divider()
    st.info(f"🟢 **System Status: Secure**\n\n**Vault Ref:** {datetime.now().strftime('%H%M%S')}-TXN")

# --- 4. TOP-LEVEL METRICS ---
m1, m2, m3, m4 = st.columns(4)
base_dso = st.session_state.engine.calculate_dso(invoices) if not invoices.empty else 0
m1.metric("Adjusted DSO", f"{base_dso + latency_days:.1f} Days", f"+{latency_days}d Latency")
m2.metric("Matching STP Rate", "94.2%", "+1.4% WoW")
m3.metric("ESG Risk Weight", "Medium", "Tier B Avg")
m4.metric("Vault Health", "Verified", "SHA-256 Active")

st.divider()

# --- 5. PAGE ROUTING LOGIC ---

# --- TAB 1: EXECUTIVE DASHBOARD ---
if menu == "📈 Executive Dashboard":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("💧 Liquidity Bridge (Stress-Adjusted)")
        if not invoices.empty:
            waterfall_data = st.session_state.analytics.get_waterfall_data(invoices, latency_days)
            fig_waterfall = go.Figure(go.Waterfall(
                measure = waterfall_data["measure"],
                x = waterfall_data["x"], y = waterfall_data["y"],
                decreasing = {"marker":{"color":"#f85149"}},
                increasing = {"marker":{"color":"#3fb950"}},
                totals = {"marker":{"color":"#1f6feb"}}
            ))
            fig_waterfall.update_layout(template="plotly_dark", height=450)
            st.plotly_chart(fig_waterfall, use_container_width=True)

    with c2:
        st.subheader("📅 Cash Flow Forecast")
        months = ["Dec", "Jan", "Feb", "Mar"]
        forecast = [42, 45, 48 + (latency_days/2), 52 + latency_days]
        
        # Create figure with labels
        fig_forecast = px.line(
            x=months, 
            y=forecast, 
            markers=True, 
            template="plotly_dark",
            labels={'x': 'Fiscal Month', 'y': 'Liquidity (M)'} # Defining axis labels
        )
        
        fig_forecast.update_traces(
            line_color="#58a6ff", 
            line_width=4,
            name="Projected Cash"
        )
        
        # Refined axis styling
        fig_forecast.update_layout(
            xaxis_title="Reporting Period",
            yaxis_title="Expected Inflow (USD Millions)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)

# --- TAB 2: ANALYST WORKBENCH ---
elif menu == "⚡ Analyst Workbench":
    st.subheader("📥 Active Bank Feed")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)
    
    if not bank_feed.empty:
        w1, w2 = st.columns([1, 2])
        with w1:
            st.subheader("Step 1: Focus Item")
            tx_selection = st.selectbox("Select Bank Transaction", bank_feed.index, 
                                       format_func=lambda x: f"{bank_feed.iloc[x]['Payer_Name']} | {bank_feed.iloc[x]['Amount_Received']}")
            tx = bank_feed.iloc[tx_selection]
            st.info(f"**Target:** {tx['Payer_Name']} | **Sum:** {tx['Currency']} {tx['Amount_Received']:,.2f}")

        with w2:
            st.subheader("Step 2: AI Match Execution")
            if st.button("🔥 Execute Multi-Factor Matching"):
                results = st.session_state.engine.run_match(tx['Amount_Received'], tx['Payer_Name'], tx['Currency'], invoices)
                if results:
                    match = results[0]
                    st.success(f"✅ **STP MATCH FOUND: {match['confidence']*100:.1f}% Confidence**")
                    st.session_state.vault.log_action(match['Invoice_ID'], "AUTO_MATCH_STP", tx['Amount_Received'])
                else:
                    st.error("❌ No suitable candidates found.")

# --- TAB 3: RISK RADAR ---
elif menu == "🛡️ Risk Radar":
    st.subheader("🌎 Institutional Risk Exposure (ESG Weighted)")
    
    if 'ESG_Score' in invoices.columns and 'Company_Code' in invoices.columns:
        # Define Weighting Logic
        rating_weights = {'AAA': 0.05, 'AA': 0.15, 'A': 0.25, 'B': 0.40, 'C': 0.60, 'D': 0.80}
        invoices['Risk_Factor'] = invoices['ESG_Score'].map(rating_weights)
        invoices['Weighted_Risk'] = invoices['Amount'] * invoices['Risk_Factor']
        
        # Display Hierarchy Visualization
        name_col = 'Customer' if 'Customer' in invoices.columns else 'Customer_Name'
        
        fig_sun = px.sunburst(
            invoices, 
            path=['Company_Code', 'Currency', name_col, 'ESG_Score'], 
            values='Weighted_Risk',
            color='ESG_Score',
            color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'A':'#3fb950', 'B':'#d29922', 'C':'#db6d28', 'D':'#f85149'},
            template="plotly_dark",
            title="Institutional Risk Hierarchy (By Weighted Exposure)"
        )
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # Data View
        st.subheader("Detailed Exposure Ledger")
        st.dataframe(invoices[['Company_Code', 'Currency', name_col, 'Amount', 'ESG_Score', 'Weighted_Risk']], use_container_width=True)
    else:
        st.error("Schema Mismatch: Please ensure invoices.csv contains 'Company_Code' and 'ESG_Score'.")

# --- TAB 4: AUDIT LEDGER ---
elif menu == "📜 Audit Ledger":
    st.subheader("🔐 SOC2 Compliance Vault (Immutable)")
    st.info("Real-time feed from the SHA-256 Hashed Audit Ledger.")
    logs = st.session_state.vault.get_logs()
    st.dataframe(logs, use_container_width=True, hide_index=True)
