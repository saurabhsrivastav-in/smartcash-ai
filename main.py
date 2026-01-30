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
    </style>
    """, unsafe_allow_html=True)

# --- 2. MULTI-YEAR DATA GENERATOR ---
@st.cache_data
def load_institutional_data():
    customers = ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech', 'Indo Power', 'Euro Mart']
    entities = ['1000 (US)', '2000 (EU)', '3000 (UK)']
    currencies = {'1000 (US)': 'USD', '2000 (EU)': 'EUR', '3000 (UK)': 'GBP'}
    ratings = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    
    inv_data = []
    for i in range(250):
        ent = np.random.choice(entities)
        amt = np.random.uniform(50000, 2000000)
        years = [2024, 2025, 2026]
        due = datetime(np.random.choice(years), np.random.randint(1, 13), np.random.randint(1, 28))
        inv_data.append({
            'Invoice_ID': f"INV-{1000+i}",
            'Company_Code': ent,
            'Customer': np.random.choice(customers),
            'Amount': round(amt, 2),
            'Amount_Remaining': round(amt, 2),
            'Currency': currencies[ent],
            'ESG_Score': np.random.choice(ratings),
            'Due_Date': due.strftime('%Y-%m-%d'),
            'Year': due.year,
            'Status': 'Overdue' if due < datetime(2026, 1, 30) else 'Open',
            'Is_Disputed': False, 'Dispute_Reason': 'N/A', 'Internal_Notes': ''
        })
    
    bank_data = []
    for i in range(50):
        ent = np.random.choice(entities)
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': np.random.choice(customers),
            'Company_Code': ent,
            'Date': (datetime(2026, 1, 10) + timedelta(days=np.random.randint(0, 20))).strftime('%Y-%m-%d'),
            'Amount_Received': round(np.random.uniform(10000, 1000000), 2),
            'Currency': currencies[ent],
            'Matched': False
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

# --- 3. SESSION STATE ---
if 'ledger' not in st.session_state:
    i_df, b_df = load_institutional_data()
    st.session_state.ledger = i_df
    st.session_state.bank = b_df
    st.session_state.audit = []

# --- 4. GLOBAL HEADER & CLEAR SYSTEM ---
def clear_all():
    st.session_state.search_val = ""
    st.session_state.chat_val = ""

st.title("🏦 SmartCash AI | Treasury Command")
col_s, col_c, col_btn = st.columns([3, 3, 1])
with col_s:
    search = st.text_input("🔍 Global Search", key="search_val", placeholder="Search Invoice or Customer...")
with col_c:
    chat = st.text_input("🤖 AI Assistant", key="chat_val", placeholder="Ask a question...")
with col_btn:
    st.write(" ") 
    if st.button("🗑️ Clear All"):
        clear_all()
        st.rerun()

if search:
    res = st.session_state.ledger[st.session_state.ledger['Invoice_ID'].str.contains(search, case=False) | st.session_state.ledger['Customer'].str.contains(search, case=False)]
    if not res.empty:
        st.dataframe(res, height=150)

st.divider()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Executive Dashboard", "🛡️ Risk Radar", "⚡ Analyst Workbench", "📜 Audit Ledger"])
    st.divider()
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

# Filter Dataset
view_df = st.session_state.ledger.copy()
if ent_f != "Consolidated":
    view_df = view_df[view_df['Company_Code'] == ent_f]

# --- 6. DYNAMIC CALCULATIONS ---
entity_complexity = len(view_df) / 250
stp_val = 98.5 - (entity_complexity * 10) - (latency * 0.05)
liq_val = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.15)
today = datetime(2026, 1, 30)

# --- 7. WORKSPACE ROUTING ---

if menu == "📈 Executive Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34+latency}d", f"+{latency}d")
    m2.metric("Liquidity Pool", f"${liq_val:.2f}M", "Dynamic")
    m3.metric("STP Accuracy", f"{stp_val:.1f}%", f"{ent_f}")
    m4.metric("Risk Items", len(view_df[view_df['Status']=='Overdue']), "Critical")

    st.divider()

    c1, c2 = st.columns([1, 2])
    with c1:
        score = max(0, min(100, 100 - (latency * 1.5)))
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=score, title={'text': "Data Integrity %"},
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,40], 'color':"#f85149"}]}))
        fig_g.update_layout(height=300, template="plotly_dark")
        st.plotly_chart(fig_g, use_container_width=True)

    with c2:
        st.subheader("💹 Multi-Year Cash Flow Projection")
        view_df['Month_Year'] = pd.to_datetime(view_df['Due_Date']).dt.to_period('M').astype(str)
        cf_data = view_df.groupby('Month_Year')['Amount_Remaining'].sum().reset_index()
        if not cf_data.empty:
            fig_cf = px.line(cf_data, x='Month_Year', y='Amount_Remaining', markers=True)
            fig_cf.update_traces(line_color='#58a6ff', line_width=4)
            fig_cf.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig_cf, use_container_width=True)
            

    st.divider()
    h1, h2 = st.columns(2)
    with h1:
        st.subheader("⏳ Ageing Distribution (Multi-Year)")
        ov_df = view_df[view_df['Status'] == 'Overdue'].copy()
        if not ov_df.empty:
            def get_b(d):
                diff = (today - datetime.strptime(d, '%Y-%m-%d')).days
                if diff <= 30: return "0-30"
                elif diff <= 60: return "31-60"
                else: return "90+"
            ov_df['Bucket'] = ov_df['Due_Date'].apply(get_b)
            # Grouping with safety reset
            age_data = ov_df.groupby(['Year', 'Bucket'], as_index=False)['Amount_Remaining'].sum()
            age_fig = px.bar(age_data, x='Bucket', y='Amount_Remaining', color='Year', barmode='group',
                             color_continuous_scale=px.colors.sequential.Blues)
            age_fig.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(age_fig, use_container_width=True)
        else:
            st.info("No overdue items for this entity.")

    with h2:
        st.subheader("🔥 FX Stress Test Heatmap")
        z = [[round(liq_val * f * (1-h), 2) for h in [0, 0.5, 1]] for f in [-0.1, -0.05, 0, 0.05]]
        fig_h = px.imshow(z, text_auto=True, color_continuous_scale='RdYlGn', x=['0%','50%','100%'], y=['-10%','-5%','0%','+5%'])
        fig_h.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig_h, use_container_width=True)
        

elif menu == "🛡️ Risk Radar":
    st.subheader("🛡️ Strategic Risk Concentration")
    weights = {'AAA':0.1, 'AA':0.2, 'A':0.3, 'B':0.5, 'C':0.7, 'D':0.9}
    view_df['Risk_Score'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights)
    fig_s = px.sunburst(view_df, path=['Year', 'Company_Code', 'Currency', 'Customer'], values='Risk_Score', color='Year')
    fig_s.update_layout(height=600, template="plotly_dark")
    st.plotly_chart(fig_s, use_container_width=True)
    

elif menu == "⚡ Analyst Workbench":
    st.subheader("⚡ Dunning & Dispute Management")
    t1, t2, t3 = st.tabs(["🧩 AI Matcher", "📩 Dunning Center", "🛠️ Dispute Resolver"])
    
    with t1:
        bk = st.session_state.bank
        bk['lbl'] = bk['Bank_ID'] + " | " + bk['Customer'] + " | $" + bk['Amount_Received'].astype(str)
        sel_bank = st.selectbox("Select Bank Entry", bk['lbl'])
        txn = bk[bk['lbl'] == sel_bank].iloc[0]
        
        if st.button("🔥 Match & Post to ERP"):
            match = view_df[view_df['Customer'] == txn['Customer']].head(1)
            if not match.empty:
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == match.iloc[0]['Invoice_ID']][0]
                st.session_state.ledger.drop(idx, inplace=True)
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Action": "ERP_POST", "ID": match.iloc[0]['Invoice_ID']})
                st.success("Invoice Cleared & Posted.")
                st.rerun()

    with t2:
        ov_list = view_df[view_df['Status'] == 'Overdue']
        if not ov_list.empty:
            target = st.selectbox("Select Debtor", ov_list['Customer'].unique())
            inv = ov_list[ov_list['Customer'] == target].iloc[0]
            email_body = st.text_area("Email Content", f"Dear {target}, Your payment for {inv['Invoice_ID']} is overdue...")
            if st.button("📧 Send Dunning"):
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Action": "DUNNING_SENT", "ID": target})
                st.success("Notice dispatched.")
        else: st.success("Queue clear.")

    with t3:
        d_items = view_df[view_df['Is_Disputed']]
        if not d_items.empty:
            res_id = st.selectbox("Resolve Item", d_items['Invoice_ID'])
            if st.button("✅ Resolve"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == res_id][0]
                st.session_state.ledger.at[idx, 'Is_Disputed'] = False
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Action": "RESOLVED", "ID": res_id})
                st.rerun()
        else:
            f_id = st.selectbox("Invoice to Freeze", view_df['Invoice_ID'])
            if st.button("🚩 Freeze Invoice"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == f_id][0]
                st.session_state.ledger.at[idx, 'Is_Disputed'] = True
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Action": "DISPUTED", "ID": f_id})
                st.rerun()

elif menu == "📜 Audit Ledger":
    if st.session_state.audit:
        st.table(pd.DataFrame(st.session_state.audit))
    else: st.info("No logs.")
