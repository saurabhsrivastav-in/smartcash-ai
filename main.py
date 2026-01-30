import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. INITIALIZE SESSION STATE (MUST BE FIRST) ---
# This prevents the StreamlitAPIException by ensuring keys exist before widgets use them
if 'search_key' not in st.session_state:
    st.session_state.search_key = ""
if 'chat_key' not in st.session_state:
    st.session_state.chat_key = ""
if 'audit' not in st.session_state:
    st.session_state.audit = []

# --- 2. CONFIG ---
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

# --- 3. DATA ENGINE ---
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
        # Deep aging data for the new buckets
        due = datetime(2026, 1, 30) - timedelta(days=np.random.randint(-30, 600))
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
            'Is_Disputed': False,
            'Dispute_Reason': 'N/A'
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

if 'ledger' not in st.session_state:
    st.session_state.ledger, st.session_state.bank = load_institutional_data()

# --- 4. FIXED CLEAR LOGIC ---
def handle_clear():
    # To clear widgets bound via 'key', we set state directly
    st.session_state.search_key = ""
    st.session_state.chat_key = ""

# --- 5. HEADER ---
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

# --- 6. SIDEBAR & FILTERS ---
with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Workbench", "📜 Audit"])
    st.divider()
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

view_df = st.session_state.ledger.copy()
if ent_f != "Consolidated": view_df = view_df[view_df['Company_Code'] == ent_f]

liq_pool = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.12)
today = datetime(2026, 1, 30)

# --- 7. WORKSPACE ---

if menu == "📈 Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34+latency}d", f"+{latency}d")
    m2.metric("Liquidity Pool", f"${liq_pool:.2f}M")
    m3.metric("Critical Overdue", f"${view_df[view_df['Status']=='Overdue']['Amount_Remaining'].sum()/1e6:.1f}M")
    m4.metric("Active Disputes", len(view_df[view_df['Is_Disputed']]))

    st.divider()

    # AGEING CHART (PRIORITY)
    st.subheader("⏳ Accounts Receivable Ageing Analysis")
    ov = view_df[view_df['Status'] == 'Overdue'].copy()
    if not ov.empty:
        def get_bucket(d):
            days = (today - datetime.strptime(d, '%Y-%m-%d')).days
            if days <= 15: return "0-15"
            elif days <= 30: return "16-30"
            elif days <= 60: return "31-60"
            elif days <= 90: return "61-90"
            elif days <= 120: return "91-120"
            elif days <= 180: return "121-180"
            elif days <= 360: return "181-360"
            else: return "361-540"
        
        ov['Bucket'] = ov['Due_Date'].apply(get_bucket)
        bucket_order = ["0-15", "16-30", "31-60", "61-90", "91-120", "121-180", "181-360", "361-540"]
        age_data = ov.groupby('Bucket')['Amount_Remaining'].sum().reindex(bucket_order, fill_value=0).reset_index()
        
        fig_age = px.bar(age_data, x='Bucket', y='Amount_Remaining', 
                         labels={'Bucket': 'Days Past Due (DPD)', 'Amount_Remaining': 'Balance Outstanding ($)'},
                         color='Bucket', color_discrete_sequence=px.colors.sequential.YlOrRd_r)
        fig_age.update_layout(template="plotly_dark", height=450, showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
        

    st.divider()

    # HEATMAP & GAUGE
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🛡️ Data Confidence")
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=max(0, 100-latency),
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_g.update_layout(height=350, template="plotly_dark")
        st.plotly_chart(fig_g, use_container_width=True)
    
    with c2:
        st.subheader("🔥 Strategic Stress Heatmap")
        fx_steps = [-0.10, -0.05, -0.02, 0, 0.05]
        h_steps = [0, 0.25, 0.5, 0.75, 1.0]
        z = [[round(liq_pool * (1 + f) * (1 - (h * 0.5)), 2) for h in h_steps] for f in fx_steps]
        
        fig_h = px.imshow(z, text_auto=True, color_continuous_scale='RdYlGn',
                          x=['0%','25%','50%','75%','100%'], 
                          y=['-10%','-5%','-2%','0%','+5%'],
                          labels=dict(x="Hedge Coverage Ratio", y="FX Volatility (%)", color="Liquidity ($M)"))
        fig_h.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig_h, use_container_width=True)

elif menu == "🛡️ Risk Radar":
    st.subheader("🛡️ Multi-Level Risk Exposure Radar")
    weights = {'AAA':0.05, 'AA':0.1, 'A':0.2, 'B':0.4, 'C':0.6, 'D':0.9}
    view_df['Exposure'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights)
    fig_s = px.sunburst(view_df, path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], 
                        values='Exposure', color='ESG_Score',
                        color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'A':'#d29922', 'B':'#db6d28', 'C':'#f85149', 'D':'#b62323'})
    fig_s.update_layout(height=700, template="plotly_dark")
    st.plotly_chart(fig_s, use_container_width=True)

elif menu == "⚡ Workbench":
    st.subheader("⚡ Operational Command")
    t1, t2, t3 = st.tabs(["🧩 AI Matcher", "📩 Dunning Center", "🛠️ Dispute Resolver"])
    
    with t1:
        bk = st.session_state.bank
        bk['lbl'] = bk['Bank_ID'] + " | " + bk['Customer'] + " | $" + bk['Amount_Received'].astype(str)
        sel = st.selectbox("Select Transaction", bk['lbl'])
        txn = bk[bk['lbl'] == sel].iloc[0]
        if st.button("🚀 Match & Post to ERP"):
            match = view_df[view_df['Customer'] == txn['Customer']].head(1)
            if not match.empty:
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == match.iloc[0]['Invoice_ID']][0]
                st.session_state.ledger.drop(idx, inplace=True)
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "ERP_POST", "ID": match.iloc[0]['Invoice_ID'], "Detail": "Full Payment"})
                st.success(f"Matched & Posted: {match.iloc[0]['Invoice_ID']}")
                st.rerun()

    with t2:
        ov = view_df[view_df['Status'] == 'Overdue']
        if not ov.empty:
            cust_name = st.selectbox("Select Debtor", ov['Customer'].unique())
            inv_row = ov[ov['Customer'] == cust_name].iloc[0]
            email_text = f"Subject: URGENT: Payment Overdue for {inv_row['Customer']} ({inv_row['Invoice_ID']})\n\nOutstanding: {inv_row['Currency']} {inv_row['Amount_Remaining']:,.2f}."
            st.text_area("Review Email Body", email_text, height=150)
            if st.button("📤 Send Notice"):
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DUNNING_SENT", "ID": inv_row['Invoice_ID'], "Detail": f"Sent to {cust_name}"})
                st.success("Notice dispatched.")

    with t3:
        c_flag, c_res = st.columns(2)
        with c_flag:
            to_freeze = st.selectbox("Freeze Invoice", view_df[~view_df['Is_Disputed']]['Invoice_ID'])
            if st.button("🚩 Freeze"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_freeze][0]
                st.session_state.ledger.at[idx, 'Is_Disputed'] = True
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DISPUTE_FLAG", "ID": to_freeze, "Detail": "Manual Freeze"})
                st.rerun()
        with c_res:
            disputed_items = view_df[view_df['Is_Disputed']]
            if not disputed_items.empty:
                to_resolve = st.selectbox("Unfreeze Invoice", disputed_items['Invoice_ID'])
                if st.button("✅ Resolve"):
                    idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_resolve][0]
                    st.session_state.ledger.at[idx, 'Is_Disputed'] = False
                    st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DISPUTE_RESOLVED", "ID": to_resolve, "Detail": "Resolved"})
                    st.rerun()

elif menu == "📜 Audit":
    if st.session_state.audit:
        st.table(pd.DataFrame(st.session_state.audit))
