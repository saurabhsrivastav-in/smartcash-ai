import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. ENTERPRISE CONFIG ---
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

# --- 2. DATA ENGINE (Multi-Year) ---
@st.cache_data
def load_institutional_data():
    customers = ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech', 'Indo Power', 'Euro Mart']
    entities = ['1000 (US)', '2000 (EU)', '3000 (UK)']
    currencies = {'1000 (US)': 'USD', '2000 (EU)': 'EUR', '3000 (UK)': 'GBP'}
    ratings = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    
    inv_data = []
    for i in range(300):
        ent = np.random.choice(entities)
        amt = np.random.uniform(50000, 2500000)
        # Spans late 2024 to early 2026
        due = datetime(2026, 1, 30) - timedelta(days=np.random.randint(-100, 500))
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
            'Is_Disputed': False
        })
    
    bank_data = []
    for i in range(50):
        ent = np.random.choice(entities)
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': np.random.choice(customers),
            'Company_Code': ent,
            'Date': (datetime(2026, 1, 15) + timedelta(days=np.random.randint(0, 15))).strftime('%Y-%m-%d'),
            'Amount_Received': round(np.random.uniform(20000, 1500000), 2),
            'Currency': currencies[ent]
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

# --- 3. STATE & CLEAR LOGIC ---
if 'ledger' not in st.session_state:
    i_df, b_df = load_institutional_data()
    st.session_state.ledger = i_df
    st.session_state.bank = b_df
    st.session_state.audit = []

def handle_clear():
    st.session_state.search_key = ""
    st.session_state.chat_key = ""

# --- 4. HEADER ---
st.title("🏦 SmartCash AI | Treasury Command")
h_col1, h_col2, h_col3 = st.columns([3, 3, 1])

with h_col1:
    search = st.text_input("🔍 Global Search", key="search_key", placeholder="Search Ledger...")
with h_col2:
    chat = st.text_input("🤖 AI Assistant", key="chat_key", placeholder="Inquiry...")
with h_col3:
    st.write(" ")
    if st.button("🗑️ Clear All"):
        handle_clear()
        st.rerun()

if search:
    res = st.session_state.ledger[st.session_state.ledger['Invoice_ID'].str.contains(search, case=False) | st.session_state.ledger['Customer'].str.contains(search, case=False)]
    st.dataframe(res, height=150)

st.divider()

# --- 5. FILTERS ---
with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Workbench", "📜 Audit"])
    st.divider()
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

# Re-Filter Data
view_df = st.session_state.ledger.copy()
if ent_f != "Consolidated":
    view_df = view_df[view_df['Company_Code'] == ent_f]

# Dynamic Stats
stp_val = 98.2 - (len(view_df)/500) - (latency * 0.05)
liq_pool = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.12)
today = datetime(2026, 1, 30)

# --- 6. WORKSPACE ---

if menu == "📈 Dashboard":
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34+latency}d", f"+{latency}d")
    m2.metric("Liquidity Pool", f"${liq_pool:.2f}M")
    m3.metric("STP Accuracy", f"{stp_val:.1f}%", delta_color="normal")
    m4.metric("Active Risks", len(view_df[view_df['Status']=='Overdue']))

    st.divider()
    c1, c2 = st.columns([1, 2])
    with c1:
        # Confidence Gauge
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=max(0, 100-latency), title={'text': "Data Integrity %"},
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_g.update_layout(height=300, template="plotly_dark")
        st.plotly_chart(fig_g, use_container_width=True)
    
    with c2:
        st.subheader("💹 Cash Flow Forecast (Multi-Year)")
        view_df['Period'] = pd.to_datetime(view_df['Due_Date']).dt.to_period('M').astype(str)
        cf = view_df.groupby('Period')['Amount_Remaining'].sum().reset_index()
        fig_cf = px.line(cf, x='Period', y='Amount_Remaining', markers=True)
        fig_cf.update_traces(line_color='#58a6ff', line_width=3)
        fig_cf.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_cf, use_container_width=True)

    st.divider()
    h1, h2 = st.columns(2)
    with h1:
        st.subheader("⏳ Ageing Distribution")
        ov = view_df[view_df['Status'] == 'Overdue'].copy()
        if not ov.empty:
            def bucket(d):
                diff = (today - datetime.strptime(d, '%Y-%m-%d')).days
                return "0-30" if diff <= 30 else "31-60" if diff <= 60 else "90+"
            ov['Bucket'] = ov['Due_Date'].apply(bucket)
            age_data = ov.groupby(['Year', 'Bucket'], as_index=False)['Amount_Remaining'].sum()
            fig_a = px.bar(age_data, x='Bucket', y='Amount_Remaining', color='Year', barmode='group')
            fig_a.update_layout(template="plotly_dark", height=350)
            st.plotly_chart(fig_a, use_container_width=True)
        else: st.info("No Overdue Data")

    with h2:
        st.subheader("🔥 Strategic Stress Heatmap")
        z = [[round(liq_pool * f * (1-h), 2) for h in [0, 0.5, 1]] for f in [-0.1, -0.05, 0, 0.05]]
        fig_h = px.imshow(z, text_auto=True, color_continuous_scale='RdYlGn', x=['0%','50%','100%'], y=['-10%','-5%','0%','+5%'])
        fig_h.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig_h, use_container_width=True)

elif menu == "🛡️ Risk Radar":
    # RESTORED PRE-ORDERED BEAUTIFUL RADAR
    st.subheader("🛡️ Multi-Level Risk Exposure Radar")
    weights = {'AAA':0.05, 'AA':0.1, 'A':0.2, 'B':0.4, 'C':0.6, 'D':0.9}
    view_df['Exposure'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights)
    
    # Path logic: Entity -> Currency -> ESG Score -> Customer
    fig_s = px.sunburst(view_df, 
                        path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], 
                        values='Exposure', 
                        color='ESG_Score',
                        color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'A':'#d29922', 'B':'#db6d28', 'C':'#f85149', 'D':'#b62323'})
    
    fig_s.update_layout(height=700, template="plotly_dark", margin=dict(t=20, l=20, r=20, b=20))
    st.plotly_chart(fig_s, use_container_width=True)
    

elif menu == "⚡ Workbench":
    st.subheader("⚡ Settlement & Dunning")
    t1, t2 = st.tabs(["🧩 Matcher", "📩 Dunning"])
    
    with t1:
        bk = st.session_state.bank
        bk['lbl'] = bk['Bank_ID'] + " | " + bk['Customer'] + " | $" + bk['Amount_Received'].astype(str)
        sel = st.selectbox("Transaction", bk['lbl'])
        txn = bk[bk['lbl'] == sel].iloc[0]
        
        if st.button("🚀 Post to ERP"):
            match = view_df[view_df['Customer'] == txn['Customer']].head(1)
            if not match.empty:
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == match.iloc[0]['Invoice_ID']][0]
                st.session_state.ledger.drop(idx, inplace=True)
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "POST", "ID": match.iloc[0]['Invoice_ID']})
                st.success("Invoice Reconciled.")
                st.rerun()

    with t2:
        ov = view_df[view_df['Status'] == 'Overdue']
        if not ov.empty:
            cust = st.selectbox("Debtor", ov['Customer'].unique())
            if st.button("📧 Dispatch Notice"):
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DUNNING", "ID": cust})
                st.toast(f"Dunning sent to {cust}")
        else: st.success("Queue Clear")

elif menu == "📜 Audit":
    st.table(pd.DataFrame(st.session_state.audit))
