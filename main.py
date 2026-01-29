import streamlit as st
import pandas as pd
from datetime import datetime

# --- IMPORT CUSTOM MODULES (Representing your Backend Folders) ---
# Note: Ensure these files exist in your /backend folder
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

# --- INITIALIZE STATE & DATA ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

# Mock Data (Sprint 1: Data Ingestion)
def get_mock_invoices():
    return pd.DataFrame({
        'Invoice_ID': ['INV-1001', 'INV-1002', 'INV-1003', 'INV-1004'],
        'Customer': ['Tesla Motors', 'Global Blue Ltd', 'Saurabh Soft', 'Tech Retail'],
        'Amount': [5000.00, 1250.00, 890.00, 3200.00],
        'ESG_Score': ['AAA', 'B', 'A+', 'A'],
        'Status': ['Open', 'Open', 'Open', 'Open']
    })

# --- SIDEBAR NAVIGATION (Sprint 3 & 4) ---
st.sidebar.title("🏦 SmartCash AI")
st.sidebar.caption("Enterprise Autonomous Finance")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Hub",
    ["Executive Dashboard", "Analyst Workbench", "Autonomous Treasury", "Audit & Governance"]
)

# --- 1. EXECUTIVE DASHBOARD (Sprint 8: Predictive Ops) ---
if menu == "Executive Dashboard":
    st.header("📊 Global Cash Performance")
    
    # KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("STP Rate", "92.4%", "+2.1%")
    c2.metric("Unapplied Cash", "$1.1M", "-15%")
    c3.metric("DSO (Days Sales O/S)", "29 Days", "-4 Days")
    c4.metric("AI Confidence", "98.2%", "Optimal")

    st.subheader("Liquidity Forecast (Sprint 8)")
    chart_data = pd.DataFrame([10, 15, 8, 22, 18, 25], columns=["Projected Cash ($M)"])
    st.area_chart(chart_data)

# --- 2. ANALYST WORKBENCH (Sprint 2, 5, 6, 10) ---
elif menu == "Analyst Workbench":
    st.header("⚡ Smart Worklist")
    st.write("Reviewing exceptions identified by the Autonomous Engine.")
    
    invoices = get_mock_invoices()
    
    # Simulation: Incoming Bank Feed (Sprint 1)
    with st.expander("📥 Simulated Bank Entry (MT942)", expanded=True):
        col_in1, col_in2 = st.columns(2)
        p_amt = col_in1.number_input("Payment Amount Received", value=1250.00)
        p_name = col_in2.text_input("Payer Name from Bank", "Global Blue")

    if st.button("Run AI Matching Engine"):
        # Accessing Backend Logic (Sprint 2 & 5)
        engine = SmartMatchingEngine()
        matches = engine.run_match(p_amt, p_name, invoices)
        
        if matches:
            top_match = matches[0]
            st.write(f"### Logic Result: {top_match['status']}")
            st.progress(top_match['confidence'], text=f"Match Confidence: {top_match['confidence']*100}%")
            
            # Zero-Touch Logic (Sprint 10: Trust > 98%)
            if top_match['confidence'] >= 0.98:
                st.success("🚀 Zero-Touch Clearing Triggered. Posted to SAP.")
                st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "ZERO_TOUCH_POST")
            else:
                st.info("Human Intervention Required")
                
                # GenAI Integration (Sprint 6)
                if st.button("Draft AI Response Email"):
                    assistant = GenAIAssistant()
                    draft = assistant.generate_email(top_match['Customer'], p_amt)
                    st.text_area("GenAI Draft:", value=draft, height=200)
                
                if st.button("Manual Clear & Log"):
                    st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "MANUAL_CLEAR", user="S.Srivastav")
                    st.success("Transaction cleared and recorded in Blockchain Audit Trail.")

# --- 3. AUTONOMOUS TREASURY (Sprint 10 & 12) ---
elif menu == "Autonomous Treasury":
    st.header("🌐 Global Treasury & CBDC Rails")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Liquidity Sweep Logic")
        st.write("Current Idle Cash: **$3.5M**")
        if st.button("Execute Autonomous Sweep"):
            st.session_state.treasury.execute_sweep(3500000)
            st.toast("Funds moved to Money Market Fund.")
            st.success("Liquidity reallocated. Estimated Yield: +1.2%")

    with col_t2:
        st.subheader("Instant Settlement (CBDC)")
        st.toggle("Enable T+0 Settlement", value=True)
        st.write("Status: **Connected to CBDC Sandbox**")

# --- 4. AUDIT & GOVERNANCE (Sprint 9 & 11) ---
elif menu == "Audit & Governance":
    st.header("🛡️ Compliance Vault")
    
    tab1, tab2 = st.tabs(["Blockchain Audit Log", "Ethical AI Monitor"])
    
    with tab1:
        st.subheader("Immutable Transaction Ledger")
        # Displaying the chain from our backend
        audit_data = st.session_state.audit_engine.get_logs()
        st.table(audit_data)
        st.button("Export Certified Audit Package")

    with tab2:
        st.subheader("Bias Detection Firewall (Sprint 11)")
        st.progress(100, text="Fairness Score: 100%")
        st.write("AI logic evaluated for regional and demographic parity.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("🔒 Quantum-Secure Connection Active")
