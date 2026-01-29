import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
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
    inv = pd.read_csv('data/invoices.csv')
    bank = pd.read_csv('data/bank_feed.csv')
    inv['Due_Date'] = pd.to_datetime(inv['Due_Date'])
    inv['Year'] = inv['Due_Date'].dt.year
    inv['Month'] = inv['Due_Date'].dt.strftime('%b')
    return inv, bank

# --- 3. SESSION STATE & ORCHESTRATION ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

invoices, bank_feed = load_data()
engine = SmartMatchingEngine()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/fluency/96/shield-with-dollar.png", width=60)
st.sidebar.title("SmartCash AI")
st.sidebar.markdown("**Institutional Treasury Hub**")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation Center", 
    ["Executive Dashboard", "Analyst Workbench", "Risk & Governance", "Audit Ledger"]
)

st.sidebar.divider()
st.sidebar.info(f"🟢 **System:** Operational\n\n📅 **Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n📂 **Records:** {len(invoices)} Invoices")

# --- 5. EXECUTIVE DASHBOARD ---
if menu == "Executive Dashboard":
    st.title("📊 Global Cash & Liquidity Position")
    
    # --- New Advanced Metrics (Strategic KPIs) ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("CEI Score", "89.4%", "+2.1%", help="Collection Effectiveness Index: Quality of collection process.")
    m2.metric("WADD", "4.2 Days", "-1.1 Days", help="Weighted Average Days Delinquent: Volume-weighted impact of lateness.")
    m3.metric("Cash Concentration", "Low", "Diversified", help="Counterparty risk level across portfolio.")
    m4.metric("AI Confidence Avg", "94.8%", "+0.5%", help="Mean accuracy of autonomous matching engine.")

    st.divider()

    # --- Liquidity Bridge & Exposure Section ---
    c1, c2 = st.columns([1.5, 1])

    with c1:
        st.subheader("📉 Liquidity Bridge (Monthly Cash Flow)")
        # B. The Cash Flow Waterfall
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Monthly Flow", orientation = "v",
            measure = ["relative", "relative", "total", "relative", "total"],
            x = ["Beginning Balance", "New Invoices", "Subtotal", "Collections", "Final Cash"],
            y = [1000000, 540000, 0, -420000, 0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#f85149"}},
            increasing = {"marker":{"color":"#2ea043"}},
            totals = {"marker":{"color":"#1f6feb"}}
        ))
        fig_waterfall.update_layout(template="plotly_dark", title="Cash Movement Analysis (USD)", height=450)
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with c2:
        st.subheader("🌍 Multi-Level Exposure Sunburst")
        # A. The Liquidity Sunburst
        fig_sun = px.sunburst(
            invoices, 
            path=['Currency', 'Customer', 'ESG_Score'], 
            values='Amount',
            color='ESG_Score',
            color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'B':'#d29922', 'C':'#f85149'},
            template="plotly_dark"
        )
        fig_sun.update_layout(height=450)
        st.plotly_chart(fig_sun, use_container_width=True)

    st.divider()

    # STP Efficiency by Channel
    st.subheader("⚡ STP Rate by Ingestion Channel")
    stp_data = pd.DataFrame({
        'Channel': ['Bank Feed (MT942)', 'Email (OCR)', 'Vendor Portal', 'Manual API'],
        'Efficiency': [98.2, 82.5, 91.0, 45.3]
    })
    fig_stp = px.bar(stp_data, x='Channel', y='Efficiency', color='Efficiency',
                     color_continuous_scale='Greens', template="plotly_dark",
                     title="Straight-Through Processing Accuracy")
    st.plotly_chart(fig_stp, use_container_width=True)

# --- 6. ANALYST WORKBENCH ---
elif menu == "Analyst Workbench":
    st.title("⚡ Smart Reconciliation Workbench")
    st.markdown("### 📥 Inbound Bank Feed")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)

    st.divider()
    col_sel, col_match = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Step 1: Focus Item")
        tx_id = st.selectbox(
            "Select Transaction for Resolution:",
            bank_feed.index,
            format_func=lambda x: f"{bank_feed.iloc[x]['Bank_TX_ID']} | {bank_feed.iloc[x]['Payer_Name']} ({bank_feed.iloc[x]['Currency']})"
        )
        tx_data = bank_feed.iloc[tx_id]
        st.info(f"**Selected Amount:** {tx_data['Currency']} {tx_data['Amount_Received']:,.2f}")

    with col_match:
        st.subheader("Step 2: AI Execution")
        if st.button("Run Multi-Factor Match"):
            matches = engine.run_match(tx_data['Amount_Received'], tx_data['Payer_Name'], tx_data['Currency'], invoices)
            if matches:
                top_match = matches[0]
                conf = top_match['confidence']
                if conf >= 0.95:
                    st.success(f"STP MATCH CONFIRMED ({conf*100}%)")
                    st.json(top_match)
                    st.balloons()
                    st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "AUTO_STP_POST")
                else:
                    st.warning(f"EXCEPTION ENCOUNTERED: {top_match['status']} ({conf*100}%)")
                    st.write(f"Suggested Invoice: **{top_match['Invoice_ID']}** for **{top_match['Customer']}**")
                    st.markdown("---")
                    st.subheader("🤖 AI Agent Assistance")
                    agent = GenAIAssistant()
                    draft = agent.generate_email(top_match['Customer'], tx_data['Amount_Received'])
                    st.text_area("Draft Communication:", draft, height=200)
                    st.button("📧 Send to Counterparty")
            else:
                st.error("NO MATCH FOUND: Routing to Manual Treasury Investigation.")

# --- 7. RISK & GOVERNANCE ---
elif menu == "Risk & Governance":
    st.title("🛡️ Institutional Risk & ESG Controls")
    
    # C. The ESG Risk Radar
    st.subheader("📊 Portfolio Health: ESG Risk Radar")
    categories = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
          r=[40, 30, 25, 10, 5, 2],
          theta=categories,
          fill='toself',
          name='Portfolio Risk',
          marker=dict(color='#238636')
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, gridcolor="#30363d")),
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("🛑 ESG Compliance Violations")
        risk_clients = invoices[invoices['ESG_Score'].isin(['D', 'E'])]
        st.error(f"{len(risk_clients)} High-Risk Entities Flagged")
        st.dataframe(risk_clients[['Invoice_ID', 'Customer', 'Amount', 'ESG_Score']], hide_index=True)
        
    with g2:
        st.subheader("⚖️ Concentration Risk (Top 5)")
        concentration = invoices.groupby('Customer')['Amount'].sum().nlargest(5).reset_index()
        fig_risk = px.funnel(concentration, x='Amount', y='Customer', template="plotly_dark")
        st.plotly_chart(fig_risk, use_container_width=True)

# --- 8. AUDIT LEDGER ---
elif menu == "Audit Ledger":
    st.title("🔐 SOC2 Compliance Vault")
    logs = st.session_state.audit_engine.get_logs()
    if logs is not None and not logs.empty:
        st.dataframe(logs, use_container_width=True, hide_index=True)
        st.download_button("📥 Export Audit Report (CSV)", logs.to_csv(), "treasury_audit.csv")
    else:
        st.info("System Initialized. Awaiting first transaction logging...")
