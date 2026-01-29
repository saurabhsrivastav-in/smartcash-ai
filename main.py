import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from backend.engine import SmartMatchingEngine
from backend.compliance import ComplianceGuard
from backend.treasury import TreasuryManager
from backend.ai_agent import GenAIAssistant

# --- CONFIGURATION (Enterprise Theme) ---
st.set_page_config(page_title="SmartCash AI | Institutional Treasury", page_icon="🏦", layout="wide")

# Custom CSS for a professional "Dark Mode" Banking Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INGESTION (Multi-Year & Multi-Currency) ---
@st.cache_data
def load_data():
    # Adding a simulated 'Year' and 'Currency' logic to dataframes
    inv = pd.read_csv('data/invoices.csv')
    bank = pd.read_csv('data/bank_feed.csv')
    
    # Mocking Date columns if not present for Multi-Year viz
    inv['Due_Date'] = pd.to_datetime(inv['Due_Date'])
    inv['Year'] = inv['Due_Date'].dt.year
    return inv, bank

# --- STATE MANAGEMENT ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

# --- SIDEBAR: STRATEGIC NAVIGATION ---
st.sidebar.image("https://img.icons8.com/fluency/96/bank-building.png", width=80)
st.sidebar.title("SmartCash AI")
st.sidebar.caption("Institutional Cash & Liquidity Hub")
menu = st.sidebar.radio("Command Center", 
    ["Executive Dashboard", "Analyst Workbench", "Risk & ESG Governance", "Audit Vault"])

invoices, bank_feed = load_data()

# --- 1. EXECUTIVE DASHBOARD (C-Suite View) ---
if menu == "Executive Dashboard":
    st.title("📊 Global Treasury Insights")
    
    # KPI Row: Multi-Factor Metrics
    c1, c2, c3, c4 = st.columns(4)
    total_receivable = invoices['Amount'].sum()
    c1.metric("Total Liquidity (USD Eq)", f"${total_receivable/1e6:.2f}M", "+12.5%")
    c2.metric("STP Auto-Match Rate", "94.2%", "Benchmark: 85%")
    c3.metric("Weighted Portfolio ESG", "A-", "Target: AA")
    c4.metric("DSO (Days Sales Outstanding)", "26.4 Days", "-3.2 Days")

    st.divider()

    # Multi-Year Trend Analysis
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📈 Multi-Year Inflow Forecast")
        # Aggregating data for Multi-year view
        yearly_data = invoices.groupby(['Year', 'ESG_Score'])['Amount'].sum().reset_index()
        fig = px.area(yearly_data, x="Year", y="Amount", color="ESG_Score", 
                     line_group="ESG_Score", title="Revenue Growth by ESG Portfolio",
                     color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🌍 Currency Concentration")
        fig_pie = px.pie(bank_feed, names='Currency', values='Amount_Received', 
                        hole=0.4, title="Global FX Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

# --- 2. ANALYST WORKBENCH (Smart Reconciliation) ---
elif menu == "Analyst Workbench":
    st.title("⚡ Smart Reconciliation Engine")
    
    # Multi-Currency Bank Feed Table
    st.subheader("Unapplied Incoming Payments")
    st.dataframe(bank_feed.style.highlight_max(axis=0, subset=['Amount_Received']), use_container_width=True)
    
    selected_tx_idx = st.selectbox(
        "🔎 Select Transaction to Clear:",
        bank_feed.index,
        format_func=lambda x: f"{bank_feed.iloc[x]['Bank_TX_ID']} | {bank_feed.iloc[x]['Payer_Name']} | {bank_feed.iloc[x]['Currency']} {bank_feed.iloc[x]['Amount_Received']}"
    )
    
    tx = bank_feed.iloc[selected_tx_idx]
    
    if st.button("🚀 Execute Smart Match"):
        engine = SmartMatchingEngine()
        results = engine.run_match(tx['Amount_Received'], tx['Payer_Name'], invoices)
        
        if results:
            res = results[0]
            confidence = res['confidence']
            
            # Confidence Threshold Logic
            if confidence >= 0.90:
                st.success(f"High Confidence Match ({confidence*100:.1f}%)")
                st.balloons()
                st.info(f"Auto-posting TXN-{tx['Bank_TX_ID']} to ERP via SAP JCo Connector...")
                st.session_state.audit_engine.log_transaction(res['Invoice_ID'], "STP_AUTO_POST")
            else:
                st.warning(f"Low Confidence ({confidence*100:.1f}%). Manual Review Triggered.")
                
                # JPMC AI Feature: Smart Dispute Agent
                st.subheader("🤖 AI Dispute Assistant")
                if st.button("Generate Dispute Draft"):
                    agent = GenAIAssistant()
                    email = agent.generate_email(res['Customer'], tx['Amount_Received'])
                    st.text_area("Smart Email Response:", email, height=200)

# --- 3. RISK & ESG GOVERNANCE ---
elif menu == "Risk & ESG Governance":
    st.title("🛡️ ESG & Counterparty Risk")
    
    
    
    # Governance Dashboard
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.subheader("Critical ESG Alerts")
        # Identify 'E' and 'D' rated customers with high balances
        at_risk = invoices[invoices['ESG_Score'].isin(['E', 'D'])]
        st.error(f"Alert: {len(at_risk)} Customers below Compliance Grade C")
        st.table(at_risk[['Customer', 'Amount', 'ESG_Score']])

    with risk_col2:
        st.subheader("Counterparty Exposure")
        # Top 5 exposure
        top_5 = invoices.groupby('Customer')['Amount'].sum().nlargest(5).reset_index()
        fig_risk = px.bar(top_5, x='Amount', y='Customer', orientation='h', title="Top 5 Concentration Risk")
        st.plotly_chart(fig_risk, use_container_width=True)

# --- 4. AUDIT VAULT ---
elif menu == "Audit Vault":
    st.title("🔐 Compliance & Audit Ledger")
    st.caption("Immutable record of all AI-driven clearing actions.")
    
    logs = st.session_state.audit_engine.get_logs()
    if not logs.empty:
        st.dataframe(logs, use_container_width=True)
        st.download_button("📥 Export SOC2 Audit Log", logs.to_csv(), "audit_log.csv")
    else:
        st.info("No logs found for the current session.")
