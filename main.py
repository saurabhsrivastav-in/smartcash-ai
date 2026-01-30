import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. STABILITY INITIALIZATION ---
if 'audit' not in st.session_state:
    st.session_state.audit = []
if 'search_query' not in st.session_state:
    st.session_state.search_query = "Consolidated"

# --- 2. DATA ENGINE ---
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
            'Amount_Remaining': round(amt, 2),
            'Currency': currencies[ent],
            'ESG_Score': np.random.choice(ratings),
            'Due_Date': due.strftime('%Y-%m-%d'),
            'Status': 'Overdue' if due < datetime(2026, 1, 30) else 'Open',
            'Is_Disputed': False
        })
    return pd.DataFrame(inv_data), pd.DataFrame([]) # Simplified for demo

if 'ledger' not in st.session_state:
    st.session_state.ledger, _ = load_institutional_data()

# --- 3. EXECUTIVE THEME ---
st.set_page_config(page_title="SmartCash AI | C-Suite", page_icon="🏛️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stMetricValue"] { font-size: 32px; color: #58a6ff; font-weight: 800; }
    .stMetric { background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); border: 1px solid #30363d; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TOP NAVIGATION & AUTO-SUGGEST ---
st.title("🏛️ SmartCash AI | Executive Treasury Dashboard")
suggestion_list = ["Consolidated"] + sorted(st.session_state.ledger['Customer'].unique().tolist())

h_col1, h_col2, h_col3 = st.columns([3, 2, 1])
with h_col1:
    search_selection = st.selectbox("🎯 Strategic Entity Search", options=suggestion_list, index=0)
with h_col2:
    st.write(" ") # Spacer
    mode = st.segmented_control("View Mode", ["Actuals", "AI Forecast", "Stress Test"], default="Actuals")
with h_col3:
    st.write(" ")
    if st.button("🔄 Refresh Data"): st.rerun()

st.divider()

# --- 5. DATA FILTERING ---
view_df = st.session_state.ledger.copy()
if search_selection != "Consolidated":
    view_df = view_df[view_df['Customer'] == search_selection]

# --- 6. INTELLIGENT TOGGLES (SIDEBAR) ---
with st.sidebar:
    st.header("🛠️ Macro Toggles")
    ai_confidence = st.select_slider("AI Confidence Interval", options=[80, 90, 95, 99], value=95)
    bad_debt_provision = st.toggle("Apply Bad Debt Provision", value=True)
    fx_hedging = st.toggle("Enable FX Hedge Overlay", value=False)
    st.divider()
    st.info(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- 7. C-SUITE METRICS (BoA Level 1) ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("BoA Liquidity Tier", "Level 1 (Strong)", "0.02% Var")
m2.metric("Working Capital Pool", f"${(view_df['Amount_Remaining'].sum()/1e6):.1f}M")
m3.metric("Weighted DSO", f"{38} Days", "-2.4% vs LY")
m4.metric("Risk-at-Value (95%)", f"${(view_df['Amount_Remaining'].sum()*0.08/1e6):.1f}M", "Critical")

st.divider()

# --- 8. GRAPHICAL INTELLIGENCE ---
c1, c2 = st.columns([2, 1])

with c1:
    # THE OVERDUE AGEING CHART (AS REQUESTED)
    st.subheader("⏳ Institutional Ageing (DPD Buckets)")
    ov = view_df[view_df['Status'] == 'Overdue'].copy()
    if not ov.empty:
        def get_bucket(d):
            days = (datetime(2026, 1, 30) - datetime.strptime(d, '%Y-%m-%d')).days
            for b in [15, 30, 60, 90, 120, 180, 360, 540]:
                if days <= b: return f"0-{b}" if b==15 else f"{prev+1}-{b}"
                prev = b
            return "540+"
        
        ov['Bucket'] = ov['Due_Date'].apply(get_bucket)
        order = ["0-15", "16-30", "31-60", "61-90", "91-120", "121-180", "181-360", "361-540"]
        age_data = ov.groupby('Bucket')['Amount_Remaining'].sum().reindex(order, fill_value=0).reset_index()
        
        fig_age = px.bar(age_data, x='Bucket', y='Amount_Remaining', text_auto='.2s',
                         color='Amount_Remaining', color_continuous_scale='Reds')
        fig_age.update_layout(template="plotly_dark", height=400, xaxis_title="Days Past Due", yaxis_title="Balance ($)")
        st.plotly_chart(fig_age, use_container_width=True)
        

with c2:
    # CONCENTRATION RISK
    st.subheader("⚠️ Concentration Risk (Top 5)")
    conc_data = view_df.groupby('Customer')['Amount_Remaining'].sum().nlargest(5).reset_index()
    fig_pie = px.pie(conc_data, values='Amount_Remaining', names='Customer', hole=.6,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_pie.update_layout(template="plotly_dark", height=400, showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    

st.divider()

# --- 9. THE INTERACTIVE STRESS MATRIX ---
st.subheader("🔥 Strategic Liquidity Stress Matrix (FX Volatility vs. Hedging)")
fx_range = np.array([-10, -5, 0, 5, 10])
hedge_range = np.array([0, 25, 50, 75, 100])
base_liq = view_df['Amount_Remaining'].sum() / 1e6

z_data = [[round(base_liq * (1 + (fx/100) * (1 - (h/100))), 2) for h in hedge_range] for fx in fx_range]

fig_h = go.Figure(data=go.Heatmap(
    z=z_data, x=[f"{h}% Hedge" for h in hedge_range], y=[f"{fx}% FX Vol" for fx in fx_range],
    colorscale='RdYlGn', text=z_data, texttemplate="$%{text}M", hoverinfo="z"
))
fig_h.update_layout(template="plotly_dark", height=400, margin=dict(t=20, b=20, l=20, r=20))
st.plotly_chart(fig_h, use_container_width=True)

# --- 10. EXECUTIVE ACTION PANEL ---
st.subheader("⚡ Executive Action Thresholds")
cols = st.columns(3)
with cols[0]:
    if st.button("🚀 Authorize AR Discounting", use_container_width=True):
        st.toast("Discounting Facility Activated for High-Risk Buckets")
with cols[1]:
    if st.button("🛡️ Trigger FX Hedge", use_container_width=True):
        st.toast("Hedge Ratio increased to 75% for GBP/USD")
with cols[2]:
    if st.button("📩 Escalated Board Report", use_container_width=True):
        st.toast("Executive Summary PDF generated.")
