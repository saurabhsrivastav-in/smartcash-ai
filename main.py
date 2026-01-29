import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- IMPORT CUSTOM MODULES ---
try:
    from backend.engine import SmartMatchingEngine
    from backend.compliance import ComplianceGuard
    from backend.treasury import TreasuryManager
    from backend.ai_agent import GenAIAssistant
except ImportError:
    st.error("Backend modules not found. Ensure the /backend folder contains engine.py, compliance.py, etc.")

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="SmartCash AI | Autonomous O2C Portal",
    page_icon="🏦",
    layout="wide"
)

# --- INITIALIZE STATE & PERSISTENT DATA ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

# --- DATA INGESTION (Sprint 1) ---
def load_data():
    """Loads mock ERP and Bank data from the /data folder."""
    if os.path.exists('data/invoices.csv') and os.path.exists('data/bank_feed.csv'):
        inv = pd.read_csv('data/invoices.csv')
        bank = pd.read_csv('data/bank_feed.csv')
        return inv, bank
    else:
        st.error("Data files missing in /data directory.")
        return pd.DataFrame(), pd.DataFrame()

# --- SIDEBAR NAVIGATION (Sprint 3 & 4) ---
st.sidebar.title("🏦 SmartCash AI")
st.sidebar.caption("Enterprise Autonomous Finance v1.0")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Hub",
    ["Executive Dashboard", "Analyst Workbench", "Autonomous Treasury", "Audit & Governance"]
)

# Load data globally for use in different modules
invoices, bank_feed = load_data()

# --- 1. EXECUTIVE DASHBOARD (Sprint 4 & 8) ---
if menu == "Executive Dashboard":
    st.header("📊 Global Cash Performance")
    
    # KPI Metrics (Sprint 8: Predictive Ops)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("STP Rate", "94.2%", "+2.1%")
    c2.metric("Unapplied Cash", "$1.1M", "-15%")
    c3.metric("DSO (Days Sales O/S)", "28 Days", "-4 Days")
    c4.metric("AI Confidence", "98.2%", "Optimal")

    st.subheader("Liquidity Forecast & Working Capital (Sprint 8)")
    chart_data = pd.DataFrame([10, 15, 8, 22, 18, 25, 30], columns=["Projected Liquidity ($M)"])
    st.area_chart(chart_data)
    

# --- 2. ANALYST WORKBENCH (Sprint 2, 5, 6, 10) ---
elif menu == "Analyst Workbench":
    st.header("⚡ Smart Worklist (Human-in-the-Loop)")
    st.write("Processing current bank feed exceptions.")
    
    # Simulation: Selecting a transaction from the bank_feed.csv (Sprint 1)
    st.subheader("Incoming Bank Feed Ingestion")
    selected_tx_idx = st.selectbox("Select Bank Transaction to Process", bank_feed.index, format_func=lambda x: f"{bank_feed.iloc[x]['Payer_Name']} - ${bank_feed.iloc[x]['Amount_Received']}")
    
    tx = bank_feed.iloc[selected_tx_idx]
    
    col_in1, col_in2 = st.columns(2)
    p_amt = col_in1.number_input("Amount Received", value=float(tx['Amount_Received']))
    p_name = col_in2.text_input("Payer Name", value=tx['Payer_Name'])

    if st.button("Run AI Matching Engine"):
        # Accessing Backend Logic (Sprint 2 & 5)
        engine = SmartMatchingEngine()
        matches = engine.run_match(p_amt, p_name, invoices)
        
        if matches:
            top_match = matches[0]
            st.write(f"### Logic Result: {top_match['status']}")
            st.progress(top_match['confidence'], text=f"Match Confidence: {round(top_match['confidence']*100, 2)}%")
            
            # Zero-Touch Logic (Sprint 10: Trust threshold)
            if top_match['confidence'] >= engine.trust_threshold:
                st.success(f"🚀 Zero-Touch Clearing Triggered for {top_match['Invoice_ID']}. Posted to SAP.")
                st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "ZERO_TOUCH_POST")
            else:
                st.info("High Variance Detected: Human Intervention Required")
                
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    # GenAI Integration (Sprint 6)
                    if st.button("Draft AI Response Email"):
                        assistant = GenAIAssistant()
                        draft = assistant.generate_email(top_match['Customer'], p_amt)
                        st.text_area("GenAI Draft (Sprint 6):", value=draft, height=200)
                
                with col_act2:
                    if st.button("Manual Clear & Post to SAP"):
                        st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "MANUAL_CLEAR", user="S.Srivastav")
                        st.success("Transaction cleared and recorded in Blockchain Audit Trail.")
        else:
            st.error("No Match Found. Routing to Dispute Management.")

# --- 3. AUTONOMOUS TREASURY (Sprint 10 & 12) ---
elif menu == "Autonomous Treasury":
    st.header("🌐 Global Treasury & CBDC Rails")
    
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Liquidity Sweep Logic")
        st.write("Current Idle Cash: **$4.2M**")
        if st.button("Execute Autonomous Sweep"):
            res = st.session_state.treasury.execute_sweep(4200000)
            st.toast(f"Sweep Executed via {res['rail']}")
            st.success(f"Liquidity reallocated to Money Market. Status: {res['status']}")

    with col_t2:
        st.subheader("Instant Settlement (CBDC)")
        st.toggle("Enable T+0 Atomic Settlement (Sprint 12)", value=True)
        st.write("Connection: **Live (JPM Coin Sandbox)**")

# --- 4. AUDIT & GOVERNANCE (Sprint 9 & 11) ---
elif menu == "Audit & Governance":
    st.header("🛡️ Compliance Vault")
    
    tab1, tab2 = st.tabs(["Blockchain Audit Log", "Ethical AI Monitor"])
    
    with tab1:
        st.subheader("Immutable Transaction Ledger (Sprint 9)")
        audit_data = st.session_state.audit_engine.get_logs()
        if not audit_data.empty:
            st.table(audit_data)
        else:
            st.info("No transactions logged in this session.")
        st.button("Export Certified Audit Package")

    with tab2:
        st.subheader("Bias Detection Firewall (Sprint 11)")
        st.progress(100, text="Fairness Score: 100%")
        st.write("Analysis: AI logic evaluated for regional and demographic parity. No bias detected in auto-post routines.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("🔒 Quantum-Secure Connection Active (PQC)")
