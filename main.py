import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. ENTERPRISE CONFIG & THEME ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #58a6ff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #161b22; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (150 Invoices + 50 Bank Txns) ---
@st.cache_data
def load_institutional_data():
    customers = ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech', 'Indo Power', 'Euro Mart']
    entities = ['1000 (US)', '2000 (EU)', '3000 (UK)']
    currencies = {'1000 (US)': 'USD', '2000 (EU)': 'EUR', '3000 (UK)': 'GBP'}
    ratings = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    
    inv_data = []
    for i in range(150):
        ent = np.random.choice(entities)
        amt = np.random.uniform(100000, 2500000)
        due = datetime(2026, 1, 30) - timedelta(days=np.random.randint(-40, 110))
        inv_data.append({
            'Invoice_ID': f"INV-{1000+i}",
            'Company_Code': ent,
            'Customer': np.random.choice(customers),
            'Amount': round(amt, 2),
            'Amount_Remaining': round(amt, 2),
            'Currency': currencies[ent],
            'ESG_Score': np.random.choice(ratings),
            'Due_Date': due.strftime('%Y-%m-%d'),
            'Status': 'Overdue' if due < datetime(2026, 1, 30) else 'Open',
            'Is_Disputed': False, 'Dispute_Reason': 'N/A', 'Internal_Notes': ''
        })
    
    bank_data = []
    for i in range(50):
        ent = np.random.choice(entities)
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': np.random.choice(customers) if np.random.random() < 0.8 else "Unknown",
            'Company_Code': ent,
            'Date': (datetime(2026, 1, 20) + timedelta(days=np.random.randint(0, 10))).strftime('%Y-%m-%d'),
            'Amount_Received': round(np.random.uniform(50000, 1200000), 2),
            'Currency': currencies[ent]
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

# --- 3. PERSISTENT STATE ---
if 'ledger' not in st.session_state:
    i_df, b_df = load_institutional_data()
    st.session_state.ledger = i_df
    st.session_state.bank = b_df
    st.session_state.audit = []
    st.session_state.match_target = None

# --- 4. GLOBAL COMMAND CENTER (Search & AI Chat) ---
st.title("🏦 SmartCash AI | Treasury Command")
g_col1, g_col2 = st.columns([1, 1])

with g_col1:
    search = st.text_input("🔍 Global Ledger Search", placeholder="ID or Customer Name...")
with g_col2:
    chat = st.text_input("🤖 AI Assistant", placeholder="e.g., 'Total in dispute?'")

if search:
    res = st.session_state.ledger[st.session_state.ledger['Invoice_ID'].str.contains(search, case=False) | st.session_state.ledger['Customer'].str.contains(search, case=False)]
    if not res.empty: st.dataframe(res[['Invoice_ID', 'Customer', 'Amount_Remaining', 'Status']], height=150)

if chat:
    if "dispute" in chat.lower():
        val = st.session_state.ledger[st.session_state.ledger['Is_Disputed']]['Amount_Remaining'].sum()
        st.info(f"AI: Found ${val/1e6:.2f}M in active disputes.")

st.divider()

# --- 5. SIDEBAR & FILTERS ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Analyst Workbench", "📜 Audit"])
    st.divider()
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

# Filter Data for View
view_df = st.session_state.ledger.copy()
if ent_f != "Consolidated": view_df = view_df[view_df['Company_Code'] == ent_f]

# --- 6. WORKSPACE ROUTING ---

if menu == "📈 Dashboard":
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    liq = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.1)
    m1.metric("Liquidity Pool", f"${liq:.2f}M", f"{-latency*0.1:.2f}M Drift")
    m2.metric("Adjusted DSO", f"{34+latency}d", f"+{latency}d")
    m3.metric("Critical Risk", f"${view_df[view_df['Status']=='Overdue']['Amount_Remaining'].sum()/1e6:.1f}M")
    m4.metric("STP Accuracy", "94.2%", "Target: 95%")

    # Charts
    c1, c2 = st.columns([1, 2])
    with c1:
        score = max(0, 100 - (latency * 2))
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=score, title={'text': "Data Confidence %"},
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}, {'range':[50,80], 'color':"#d29922"}]}))
        fig_g.update_layout(height=300, template="plotly_dark")
        st.plotly_chart(fig_g, use_container_width=True)
    
    with c2:
        st.subheader("⏳ Ageing Bucket Analysis")
        today = datetime(2026, 1, 30)
        ov_df = view_df[view_df['Status'] == 'Overdue'].copy()
        def set_bucket(d):
            diff = (today - datetime.strptime(d, '%Y-%m-%d')).days
            if diff <= 30: return "0-30"
            elif diff <= 60: return "31-60"
            else: return "90+"
        if not ov_df.empty:
            ov_df['Bucket'] = ov_df['Due_Date'].apply(set_bucket)
            fig_a = px.bar(ov_df.groupby('Bucket')['Amount_Remaining'].sum().reset_index(), x='Bucket', y='Amount_Remaining', color='Bucket', color_discrete_sequence=["#3fb950", "#d29922", "#f85149"])
            st.plotly_chart(fig_a, use_container_width=True)

    # Simulator & FX
    st.divider()
    s1, s2 = st.columns(2)
    with s1:
        st.subheader("🔮 Recovery Simulator")
        if st.toggle("Simulate 90+ Day Recovery"):
            rate = st.slider("Success Rate %", 0, 100, 50)
            st.success(f"Projected Cash Inflow: +${(liq*(rate/100)):.2f}M")
    with s2:
        st.subheader("💱 FX Advisor")
        if st.toggle("Simulate USD Strengthening"):
            st.error("Strategy: SELL EUR/GBP to protect USD balance.")
    
    if st.button("📊 Download Board Deck"): st.toast("PDF Prepared.")

elif menu == "🛡️ Risk Radar":
    # Smart Summary
    st.subheader("📊 Collection Triage")
    d_val = view_df[view_df['Is_Disputed']]['Amount_Remaining'].sum()
    c_val = view_df[(view_df['Status']=='Overdue') & (~view_df['Is_Disputed'])]['Amount_Remaining'].sum()
    r1, r2, r3 = st.columns(3)
    r1.metric("🚩 Cash in Dispute", f"${d_val/1e6:.2f}M")
    r2.metric("✅ Actionable Overdue", f"${c_val/1e6:.2f}M")
    r3.metric("ESG Index", "78.4", "Health")

    st.divider()
    # THE BEAUTIFUL SUNBURST
    st.subheader("🛡️ Interactive Exposure Map")
    weights = {'AAA':0.1, 'AA':0.2, 'A':0.3, 'B':0.5, 'C':0.7, 'D':0.9}
    view_df['Risk_Score'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights)
    fig_s = px.sunburst(view_df, path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], values='Risk_Score', color='ESG_Score', color_discrete_map={'AAA':'#238636', 'D':'#f85149'})
    fig_s.update_layout(height=600, template="plotly_dark")
    st.plotly_chart(fig_s, use_container_width=True)

elif menu == "⚡ Analyst Workbench":
    st.subheader("⚡ Reconcile & Resolve")
    t1, t2, t3 = st.tabs(["🧩 Matcher", "📩 Dunning", "🛠️ Dispute Resolver"])
    
    with t1:
        b = st.session_state.bank
        b['label'] = b['Bank_ID'] + " | " + b['Customer'] + " | " + b['Company_Code'] + " | $" + b['Amount_Received'].astype(str)
        sel = st.selectbox("Select Transaction", b['label'])
        txn = b[b['label'] == sel].iloc[0]
        
        if st.button("🔥 Run AI Match"):
            matches = view_df[view_df['Customer'] == txn['Customer']]
            if not matches.empty:
                st.session_state.match_target = matches.iloc[0]
                st.success(f"Matched to {st.session_state.match_target['Invoice_ID']}")

        if st.session_state.match_target is not None:
            m = st.session_state.match_target
            part = st.toggle("Partial Payment")
            amt = st.number_input("Apply Amount", value=float(txn['Amount_Received'])) if part else float(m['Amount_Remaining'])
            
            c_a, c_b, c_c = st.columns(3)
            if c_a.button("📤 Post to ERP"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == m['Invoice_ID']][0]
                if part and amt < m['Amount_Remaining']:
                    st.session_state.ledger.at[idx, 'Amount_Remaining'] -= amt
                else:
                    st.session_state.ledger.drop(idx, inplace=True)
                st.session_state.audit.insert(0, {"Action": "ERP POST", "Inv": m['Invoice_ID'], "Amt": amt})
                st.session_state.match_target = None
                st.rerun()
            if c_b.button("🚩 Flag Dispute"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == m['Invoice_ID']][0]
                st.session_state.ledger.at[idx, 'Is_Disputed'] = True
                st.rerun()

    with t3:
        disp_list = view_df[view_df['Is_Disputed']]
        if not disp_list.empty:
            target = st.selectbox("Resolve Item", disp_list['Invoice_ID'])
            reason = st.selectbox("Reason", ["Pricing", "Damaged", "Short-Ship"])
            notes = st.text_area("Analyst Notes")
            if st.button("✅ Resolve"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == target][0]
                st.session_state.ledger.at[idx, 'Is_Disputed'] = False
                st.session_state.ledger.at[idx, 'Dispute_Reason'] = reason
                st.session_state.ledger.at[idx, 'Internal_Notes'] = notes
                st.rerun()
        else: st.info("No active disputes.")

elif menu == "📜 Audit":
    st.table(st.session_state.audit)
