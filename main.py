import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. INITIALIZE SESSION STATE (STABILITY FIRST) ---
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
            'Is_Disputed': False
        })
    return pd.DataFrame(inv_data)

if 'ledger' not in st.session_state:
    st.session_state.ledger = load_institutional_data()

def handle_clear():
    st.session_state.search_key = ""
    st.session_state.chat_key = ""

# --- 4. HEADER ---
st.title("🏦 SmartCash AI | Treasury Command")
h_col1, h_col2, h_col3 = st.columns([3, 3, 1])
with h_col1:
    search = st.text_input("🔍 Global Search", key="search_key")
with h_col2:
    chat = st.text_input("🤖 AI Assistant", key="chat_key")
with h_col3:
    st.write(" ")
    if st.button("🗑️ Clear All"):
        handle_clear()
        st.rerun()

st.divider()

# --- 5. SIDEBAR ---
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

# --- 6. DASHBOARD ---
if menu == "📈 Dashboard":
    # METRICS ROW with Bank of America Level
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("BoA Liquidity Tier", "Level 1 (Strong)", "0.02% Var")
    m2.metric("Liquidity Pool", f"${liq_pool:.2f}M")
    m3.metric("Adjusted DSO", f"{34+latency}d")
    m4.metric("Active Disputes", len(view_df[view_df['Is_Disputed']]))

    st.divider()

    # AGEING CHART
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
        order = ["0-15", "16-30", "31-60", "61-90", "91-120", "121-180", "181-360", "361-540"]
        age_data = ov.groupby('Bucket')['Amount_Remaining'].sum().reindex(order, fill_value=0).reset_index()
        
        fig_age = px.bar(age_data, x='Bucket', y='Amount_Remaining', 
                         labels={'Bucket': 'Days Past Due (DPD)', 'Amount_Remaining': 'Balance ($)'},
                         color='Amount_Remaining', color_continuous_scale='Blues')
        fig_age.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_age, use_container_width=True)

    st.divider()

    # INTERACTIVE HEATMAP & CONFIDENCE
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🛡️ Data Confidence")
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=max(0, 100-latency),
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_g.update_layout(height=380, template="plotly_dark")
        st.plotly_chart(fig_g, use_container_width=True)
    
    with c2:
        st.subheader("🔥 Interactive Stress Matrix")
        # Creating a higher resolution interactive heatmap
        fx_range = np.array([-15, -10, -5, -2, 0, 2, 5])
        hedge_range = np.array([0, 20, 40, 60, 80, 100])
        z_data = []
        for fx in fx_range:
            row = []
            for h in hedge_range:
                # Formula: Base Liquidity adjusted by FX Vol and mitigated by hedge coverage
                impact = liq_pool * (1 + (fx/100) * (1 - (h/100)))
                row.append(round(impact, 2))
            z_data.append(row)

        fig_h = go.Figure(data=go.Heatmap(
            z=z_data,
            x=[f"{h}% Hedge" for h in hedge_range],
            y=[f"{fx}% Vol" for fx in fx_range],
            colorscale='RdYlGn',
            text=z_data,
            texttemplate="$%{text}M",
            hoverinfo="z"
        ))
        
        fig_h.update_layout(
            template="plotly_dark", 
            height=380,
            xaxis_title="Hedge Coverage Ratio",
            yaxis_title="Currency Volatility (%)",
            margin=dict(t=10, b=10, l=10, r=10)
        )
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
    t1, t2 = st.tabs(["📩 Dunning Center", "🛠️ Dispute Resolver"])
    with t1:
        ov = view_df[view_df['Status'] == 'Overdue']
        if not ov.empty:
            cust = st.selectbox("Select Debtor", ov['Customer'].unique())
            inv = ov[ov['Customer'] == cust].iloc[0]
            st.text_area("Notice Draft", f"Payment for {inv['Invoice_ID']} ({inv['Amount_Remaining']}) is overdue.")
            if st.button("📤 Send"):
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DUNNING", "ID": inv['Invoice_ID']})
                st.success("Notice Dispatched.")
    with t2:
        to_f = st.selectbox("Invoice ID", view_df['Invoice_ID'])
        if st.button("🚩 Flag Dispute"):
            idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_f][0]
            st.session_state.ledger.at[idx, 'Is_Disputed'] = True
            st.rerun()

elif menu == "📜 Audit":
    st.table(pd.DataFrame(st.session_state.audit))
