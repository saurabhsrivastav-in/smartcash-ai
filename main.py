import os
import sys
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")

# Institutional Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #58a6ff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
@st.cache_data
def load_data():
    inv = pd.DataFrame({
        'Company_Code': ['1000', '1000', '2000', '3000', '1000', '2000'],
        'Customer': ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log'],
        'Amount': [5200000, 15000000, 1250000, 3200000, 12450750, 450500],
        'Currency': ['USD', 'USD', 'EUR', 'GBP', 'USD', 'EUR'],
        'ESG_Score': ['AAA', 'B', 'D', 'A', 'C', 'D'],
        'Date': ['2026-01-15', '2026-01-21', '2024-12-21', '2026-03-02', '2024-11-01', '2024-11-16']
    })
    bank = pd.DataFrame({'Date': [pd.Timestamp('2026-01-25')], 'Company_Code': ['1000'], 'Amount': [1000000]})
    return inv, bank

raw_invoices, bank_feed = load_data()

# Initialize Session States
if 'audit_log' not in st.session_state: 
    st.session_state.audit_log = []

# --- SIDEBAR & GLOBAL CONTROLS ---
with st.sidebar:
    st.title("🏦 SmartCash AI")
    # RESTORED ALL TABS
    menu = st.radio("Workspace", ["📈 Executive Dashboard", "🛡️ Risk Radar", "⚡ Analyst Workbench", "📜 Audit Ledger"])
    st.divider()
    st.subheader("⚙️ Global Parameters")
    latency_days = st.slider("Collection Latency (Days)", 0, 90, 15)
    
    entity_options = ["All Entities"] + list(raw_invoices['Company_Code'].unique())
    selected_entity = st.selectbox("Company Entity", entity_options)
    
    st.divider()
    st.subheader("📝 Scenario Governance")
    scenario_name = st.text_input("Scenario Label", "Q1 Assessment")
    scenario_note = st.text_area("Notes", "Simulating market volatility.")

# --- FILTERING LOGIC (The "Wiring") ---
invoices = raw_invoices.copy()
if selected_entity != "All Entities":
    invoices = invoices[invoices['Company_Code'] == selected_entity]

# Apply Latency to calculation
base_liquidity = 292500000 / 1000000 # In Millions
# Latency reduces immediate liquidity in our model
adjusted_liquidity = base_liquidity - (latency_days * 0.5) 

# --- DASHBOARD ROUTING ---

if menu == "📈 Executive Dashboard":
    # 1. TOP METRICS
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34 + latency_days} Days", f"+{latency_days}d Latency")
    m2.metric("Liquidity Buffer", f"${adjusted_liquidity:.1f}M", f"{-latency_days*0.5:.1f}M Latency Impact")
    m3.metric("Avg ESG Score", "Tier B", "Stable")
    m4.metric("STP Rate", "94.2%", "Verified")

    st.divider()
    
    # 2. DATA CONFIDENCE & FORECAST
    c1, c2 = st.columns([1, 2])
    with c1:
        fig_conf = go.Figure(go.Indicator(
            mode="gauge+number", value=92, title={'text': "Data Confidence (%)"},
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_conf.update_layout(height=250, template="plotly_dark", margin=dict(t=50, b=0))
        st.plotly_chart(fig_conf, use_container_width=True)
        
    with c2:
        st.subheader("💹 Cash Flow Forecast")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        fig_flow = go.Figure()
        fig_flow.add_trace(go.Scatter(x=months, y=[42, 48, 45, 52, 58, 62], name="2026 Forecast", line=dict(color='#58a6ff', width=4)))
        fig_flow.add_trace(go.Scatter(x=months, y=[38, 41, 40, 46, 50, 52], name="2025 Actual", line=dict(color='#30363d', dash='dot')))
        fig_flow.update_layout(template="plotly_dark", height=280, margin=dict(t=20, b=20))
        st.plotly_chart(fig_flow, use_container_width=True)

    st.divider()

    # 3. STRESS TEST & WATERFALL
    col_ctrl, col_chart = st.columns([1, 2])
    with col_ctrl:
        st.subheader("🚨 Stress Test")
        fx_swing = st.toggle("5% USD Strengthening")
        hedge_ratio = st.slider("Hedge Ratio %", 0, 100, 50) / 100 if fx_swing else 0
        
        if st.button("💾 Log Scenario to Ledger"):
            st.session_state.audit_log.insert(0, {"Timestamp": datetime.now().strftime("%H:%M"), "Label": scenario_name, "Liquidity": f"${adjusted_liquidity:.1f}M"})
            st.success("Archived.")

    with col_chart:
        st.subheader("📉 Hedge Effectiveness Waterfall")
        fx_loss = -14.6 if fx_swing else 0
        hedge_gain = abs(fx_loss) * hedge_ratio
        fig_water = go.Figure(go.Waterfall(
            orientation = "v", x = ["Base", "FX Loss", "Hedge", "Net"],
            y = [adjusted_liquidity, fx_loss, hedge_gain, 0],
            measure = ["absolute", "relative", "relative", "total"],
            decreasing = {"marker":{"color":"#f85149"}}, increasing = {"marker":{"color":"#3fb950"}}, totals = {"marker":{"color":"#1f6feb"}}
        ))
        fig_water.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig_water, use_container_width=True)

    # 4. SENSITIVITY HEATMAP
    st.divider()
    st.subheader("🔥 Risk Sensitivity Heatmap")
    fx_range = np.linspace(-0.10, 0.02, 5)
    hedge_range = np.linspace(0, 1, 5)
    z_data = [[round(adjusted_liquidity * f * (1 - h), 2) for h in hedge_range] for f in fx_range]
    fig_heat = px.imshow(z_data, text_auto=True, color_continuous_scale='RdYlGn', labels=dict(x="Hedge", y="FX Swing", color="Impact"),
                         x=['0%', '25%', '50%', '75%', '100%'], y=['-10%', '-7%', '-4%', '-1%', '+2%'])
    fig_heat.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_heat, use_container_width=True)

# --- RESTORED: RISK RADAR (Original High-Detail Version) ---
elif menu == "🛡️ Risk Radar":
    st.subheader("🛡️ Institutional Risk Exposure (ESG Weighted)")
    rating_weights = {'AAA': 0.05, 'AA': 0.15, 'A': 0.25, 'B': 0.40, 'C': 0.60, 'D': 0.80}
    invoices['Risk_Factor'] = invoices['ESG_Score'].map(rating_weights)
    invoices['Weighted_Risk'] = invoices['Amount'] * invoices['Risk_Factor']

    fig_sun = px.sunburst(
        invoices, path=['Company_Code', 'Currency', 'Customer', 'ESG_Score'], 
        values='Weighted_Risk', color='ESG_Score',
        color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'A':'#3fb950', 'B':'#d29922', 'C':'#db6d28', 'D':'#f85149'},
        hover_data={'Amount': ':,.0f', 'Weighted_Risk': ':,.0f'},
        template="plotly_dark"
    )
    st.plotly_chart(fig_sun, use_container_width=True)
    st.subheader("📜 Detailed Exposure Ledger")
    st.dataframe(invoices[['Customer', 'Amount', 'Currency', 'ESG_Score', 'Weighted_Risk']], use_container_width=True)

# --- OTHER TABS ---
elif menu == "⚡ Analyst Workbench":
    st.subheader("⚡ Transaction Matching Engine")
    st.info("Select a bank record to see AI-suggested invoice matches.")
    st.dataframe(bank_feed)

elif menu == "📜 Audit Ledger":
    st.subheader("🔐 Compliance Audit Ledger")
    if st.session_state.audit_log:
        st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True)
    else:
        st.info("No logs captured yet.")
