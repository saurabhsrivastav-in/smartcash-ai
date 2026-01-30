import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. ENTERPRISE CONFIG & STYLING ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #58a6ff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #161b22; border-radius: 5px; }
    .stDataFrame { border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED DATA GENERATOR (Restoring 2026 Context) ---
@st.cache_data
def load_institutional_data():
    # Massive Invoice Dataset
    customers = ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech', 'Indo Power', 'Euro Mart']
    entities = ['1000 (US)', '2000 (EU)', '3000 (UK)']
    currencies = {'1000 (US)': 'USD', '2000 (EU)': 'EUR', '3000 (UK)': 'GBP'}
    ratings = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    
    data = []
    for i in range(150): # Expanded for deep filtering
        ent = np.random.choice(entities)
        rate = np.random.choice(ratings, p=[0.2, 0.2, 0.2, 0.2, 0.1, 0.1])
        amt = np.random.uniform(50000, 2000000)
        due = datetime(2026, 1, 1) + timedelta(days=np.random.randint(0, 90))
        data.append({
            'Invoice_ID': f"INV-{1000+i}",
            'Company_Code': ent,
            'Customer': np.random.choice(customers),
            'Amount': round(amt, 2),
            'Currency': currencies[ent],
            'ESG_Score': rate,
            'Due_Date': due.strftime('%Y-%m-%d'),
            'Status': np.random.choice(['Open', 'Overdue'], p=[0.7, 0.3])
        })
    
    bank_feed = [
        {'Bank_ID': 'TXN_991', 'Payer': 'Tesla', 'Amount_Received': 520000.00, 'Currency': 'USD', 'Date': '2026-01-28'},
        {'Bank_ID': 'TXN_992', 'Payer': 'EcoEnergy', 'Amount_Received': 125000.00, 'Currency': 'USD', 'Date': '2026-01-29'},
        {'Bank_ID': 'TXN_993', 'Payer': 'Unknown', 'Amount_Received': 89000.00, 'Currency': 'GBP', 'Date': '2026-01-30'}
    ]
    return pd.DataFrame(data), pd.DataFrame(bank_feed)

invoices, bank_feed = load_institutional_data()

# --- 3. SESSION STATE & GOVERNANCE ---
if 'audit_log' not in st.session_state: st.session_state.audit_log = []
if 'matched_txns' not in st.session_state: st.session_state.matched_txns = []

# --- 4. SIDEBAR GLOBAL COMMAND ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=60)
    st.title("SmartCash AI")
    st.caption("Institutional Liquidity Management v2.4")
    st.divider()
    menu = st.radio("Workspace", ["📈 Executive Dashboard", "🛡️ Risk Radar", "⚡ Analyst Workbench", "📜 Audit Ledger"])
    
    st.divider()
    st.subheader("🛠️ Global Parameters")
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    entity_filter = st.selectbox("Company Entity", ["Consolidated"] + list(invoices['Company_Code'].unique()))
    
    st.divider()
    st.info("🟢 System Status: Secure\nVault Encryption: AES-256")

# --- 5. DATA WIRING & CALCULATIONS ---
df = invoices.copy()
if entity_filter != "Consolidated":
    df = df[df['Company_Code'] == entity_filter]

# Interactive Metrics Logic
esg_weights = {'AAA':100, 'AA':85, 'A':75, 'B':50, 'C':30, 'D':0}
current_esg = df['ESG_Score'].map(esg_weights).mean()
total_liquidity = (df['Amount'].sum() / 1e6) - (latency * 0.15)
stp_rate = 94.2 - (latency * 0.05)

# --- 6. WORKSPACE ROUTING ---

# --- TAB 1: EXECUTIVE DASHBOARD ---
if menu == "📈 Executive Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34 + latency} Days", f"+{latency}d Drift")
    m2.metric("Liquidity Pool", f"${total_liquidity:.2f}M", f"{-latency*0.15:.2f}M Latency")
    m3.metric("ESG Health Index", f"{current_esg:.1f}", "Dynamic")
    m4.metric("STP Reliability", f"{stp_rate:.1f}%", "-0.1% Var")

    st.divider()

    c1, c2 = st.columns([1, 2])
    with c1:
        # Confidence Gauge
        age_score = max(0, 100 - (latency * 2))
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=age_score, title={'text': "Data Confidence (%)"},
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,40], 'color':"#f85149"}, {'range':[40,75], 'color':"#d29922"}]}))
        fig_g.update_layout(height=280, template="plotly_dark", margin=dict(t=50, b=0))
        st.plotly_chart(fig_g, use_container_width=True)
    
    with c2:
        st.subheader("💹 Multi-Year Liquidity Forecast")
        fig_f = go.Figure()
        fig_f.add_trace(go.Scatter(x=['Jan','Feb','Mar','Apr'], y=[42, 48, 45, 52], name="2026 Proj", line=dict(color='#58a6ff', width=4)))
        fig_f.add_trace(go.Scatter(x=['Jan','Feb','Mar','Apr'], y=[38, 40, 41, 44], name="2025 Act", line=dict(color='#30363d', dash='dot')))
        fig_f.update_layout(template="plotly_dark", height=280, margin=dict(t=20, b=20))
        st.plotly_chart(fig_f, use_container_width=True)

    st.divider()

    st.subheader("🔥 Strategic Sensitivity & Stress Test")
    t1, t2 = st.columns([1, 2])
    with t1:
        fx_toggle = st.toggle("Simulate FX Volatility")
        fx_val = st.slider("USD Stronger (%)", 0, 15, 5) if fx_toggle else 0
        hedge_ratio = st.slider("Hedge Coverage (%)", 0, 100, 50) if fx_toggle else 0
        
        if st.button("💾 Archive Scenario"):
            st.session_state.audit_log.insert(0, {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Entity": entity_filter, "Liquidity": f"${total_liquidity:.1f}M",
                "ESG": f"{current_esg:.1f}", "Hedge": f"{hedge_ratio}%"
            })
            st.success("Scenario Vaulted.")

    with t2:
        # Scaled Heatmap
        fx_steps = [-0.10, -0.05, -0.02, 0, 0.05]
        h_steps = [0, 0.25, 0.5, 0.75, 1.0]
        z = [[round(total_liquidity * f * (1-(h)), 2) for h in h_steps] for f in fx_steps]
        fig_h = px.imshow(z, text_auto=True, color_continuous_scale='RdYlGn', aspect="auto",
                          x=['0%','25%','50%','75%','100%'], y=['-10%','-5%','-2%','0%','+5%'],
                          labels=dict(x="Hedge Ratio", y="FX Volatility", color="Impact $M"))
        fig_h.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_h, use_container_width=True)

# --- TAB 2: RISK RADAR ---
elif menu == "🛡️ Risk Radar":
    st.subheader("🛡️ Institutional Risk Radar (ESG Weighted)")
    risk_weights = {'AAA':0.05, 'AA':0.1, 'A':0.2, 'B':0.4, 'C':0.6, 'D':0.95}
    df['Weighted_Risk'] = df['Amount'] * df['ESG_Score'].map(risk_weights)
    
    # Restored Multi-Level Sunburst
    fig_s = px.sunburst(df, path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], 
                        values='Weighted_Risk', color='ESG_Score',
                        color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'B':'#d29922', 'D':'#f85149'})
    fig_s.update_layout(height=600, template="plotly_dark")
    st.plotly_chart(fig_s, use_container_width=True)

    st.divider()
    st.subheader("🔍 Smart Filter Exposure Ledger")
    c1, c2, c3 = st.columns(3)
    with c1: search = st.text_input("Customer Search")
    with c2: rating_f = st.multiselect("Rating Filter", ['AAA','AA','A','B','C','D'], default=['AAA','AA','A','B','C','D'])
    with c3: status_f = st.selectbox("Status Filter", ['All', 'Open', 'Overdue'])
    
    f_df = df[df['ESG_Score'].isin(rating_f)]
    if search: f_df = f_df[f_df['Customer'].str.contains(search, case=False)]
    if status_f != 'All': f_df = f_df[f_df['Status'] == status_f]
    
    st.dataframe(f_df[['Invoice_ID', 'Customer', 'Amount', 'Currency', 'ESG_Score', 'Status', 'Due_Date']], use_container_width=True)

# --- TAB 3: ANALYST WORKBENCH (Restored Functionality) ---
elif menu == "⚡ Analyst Workbench":
    st.subheader("⚡ Smart Matching & Dunning Automation")
    
    t1, t2 = st.tabs(["🧩 Automated Matching", "📩 Dunning Center"])
    
    with t1:
        col_x, col_y = st.columns([1, 1])
        with col_x:
            st.write("**Inbound Bank Feed**")
            selected_txn = st.selectbox("Select Transaction", bank_feed['Bank_ID'])
            txn_row = bank_feed[bank_feed['Bank_ID'] == selected_txn].iloc[0]
            st.code(f"Payer: {txn_row['Payer']}\nAmount: {txn_row['Amount_Received']} {txn_row['Currency']}")
            
            if st.button("🔥 Run Matching Engine"):
                # Simulating Match Logic
                match = df[df['Customer'] == txn_row['Payer']].head(1)
                if not match.empty:
                    st.success(f"STP Match Found: {match['Invoice_ID'].values[0]} (Confidence: 99.8%)")
                    st.session_state.matched_txns.append(selected_txn)
                else:
                    st.warning("No direct match. Reviewing historical payer patterns...")

    with t2:
        st.write("**Delinquent Accounts**")
        overdue_list = df[df['Status'] == 'Overdue']['Customer'].unique()
        target = st.selectbox("Select Customer for Dunning", overdue_list)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("Draft Level 1 (Friendly)"):
                st.info(f"Drafting for {target}...")
                st.markdown(f"> **Subject:** Account Statement - {target}\n> Just a friendly reminder that invoice INV-1004 is now overdue...")
        with col_m2:
            if st.button("Draft Level 3 (Urgent)"):
                st.error(f"Drafting for {target}...")
                st.markdown(f"> **Subject:** URGENT: FINAL NOTICE\n> Your account with {entity_filter} is now 30+ days overdue. Please settle immediately.")

# --- TAB 4: AUDIT LEDGER ---
elif menu == "📜 Audit Ledger":
    st.subheader("📜 SOC2 Audit Trail")
    if st.session_state.audit_log:
        audit_df = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(audit_df, use_container_width=True)
        st.download_button("📥 Export Audit Trail", audit_df.to_csv(index=False), "treasury_audit.csv")
    else:
        st.warning("No data logs recorded in the current session.")
