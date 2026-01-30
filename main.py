import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. BOILERPLATE & STABILITY INITIALIZATION ---
if 'audit' not in st.session_state:
    st.session_state.audit = []
if 'search_key' not in st.session_state:
    st.session_state.search_key = ""
if 'chat_key' not in st.session_state:
    st.session_state.chat_key = ""

# --- 2. DATA ENGINE (FIX FOR ATTRIBUTE ERROR) ---
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
    
    bank_data = []
    for i in range(20):
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': np.random.choice(customers),
            'Amount_Received': round(np.random.uniform(20000, 1500000), 2),
            'Date': (datetime(2026, 1, 15) + timedelta(days=i)).strftime('%Y-%m-%d')
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

# Ensure data is loaded into session state before anything else renders
if 'ledger' not in st.session_state or 'bank' not in st.session_state:
    ledger_df, bank_df = load_institutional_data()
    st.session_state.ledger = ledger_df
    st.session_state.bank = bank_df

def handle_clear():
    st.session_state.search_key = ""
    st.session_state.chat_key = ""

# --- 3. UI CONFIG ---
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

# --- 4. HEADER & SEARCH ---
st.title("🏦 SmartCash AI | Treasury Command")
h_col1, h_col2, h_col3 = st.columns([3, 3, 1])
with h_col1:
    search_term = st.text_input("🔍 Global Search", key="search_key", placeholder="Search Customer or Invoice ID...")
with h_col2:
    chat_term = st.text_input("🤖 AI Assistant", key="chat_key", placeholder="Ask me about a customer or invoice...")
with h_col3:
    st.write(" ")
    st.button("🗑️ Clear All", on_click=handle_clear)

st.divider()

# --- 5. SEARCH & FILTER LOGIC (UPDATED FOR AI ASSISTANT) ---
view_df = st.session_state.ledger.copy()

# Combine search_term and chat_term into a single master filter
# If either box has text, the application will filter for that string
combined_query = search_term if search_term else chat_term

if combined_query:
    view_df = view_df[view_df['Customer'].str.contains(combined_query, case=False) | 
                     view_df['Invoice_ID'].str.contains(combined_query, case=False)]

with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Workbench", "📜 Audit"])
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

if ent_f != "Consolidated":
    view_df = view_df[view_df['Company_Code'] == ent_f]

liq_pool = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.12)
today = datetime(2026, 1, 30)

# --- 6. WORKSPACE ---

if menu == "📈 Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("BoA Liquidity Tier", "Level 1 (Strong)", "0.02% Var")
    m2.metric("Filtered Liquidity", f"${liq_pool:.2f}M")
    m3.metric("Adjusted DSO", f"{34+latency}d")
    m4.metric("Matching Items", len(view_df))

    st.divider()

    # PRIMARY: AGEING CHART
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
                         color='Amount_Remaining', color_continuous_scale='Turbo')
        fig_age.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_age, use_container_width=True)
        

    st.divider()

    # SECONDARY: INTERACTIVE HEATMAP
    st.subheader("🔥 Interactive Stress Matrix (FX vs Hedge)")
    fx_range = np.array([-15, -10, -5, -2, 0, 5, 10])
    hedge_range = np.array([0, 25, 50, 75, 100])
    z_data = [[round(liq_pool * (1 + (fx/100) * (1 - (h/100))), 2) for h in hedge_range] for fx in fx_range]

    fig_h = go.Figure(data=go.Heatmap(
        z=z_data, x=[f"{h}% Hedge" for h in hedge_range], y=[f"{fx}% Vol" for fx in fx_range],
        colorscale='RdYlGn', text=z_data, texttemplate="$%{text}M", hoverinfo="z"
    ))
    fig_h.update_layout(template="plotly_dark", height=400, xaxis_title="Hedge Coverage", yaxis_title="FX Volatility (%)")
    st.plotly_chart(fig_h, use_container_width=True)
    

elif menu == "🛡️ Risk Radar":
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
        st.write("**Recent Bank Transactions**")
        st.dataframe(st.session_state.bank, use_container_width=True)
        st.info("AI Matching engine is active. Select an entry to reconcile with open invoices.")

    with t2:
        ov = view_df[view_df['Status'] == 'Overdue']
        if not ov.empty:
            target = st.selectbox("Select Debtor", ov['Customer'].unique())
            inv = ov[ov['Customer'] == target].iloc[0]
            st.markdown("### 📧 Professional Notice Draft")
            email_body = f"""Subject: URGENT: Payment Overdue for {inv['Customer']} ({inv['Invoice_ID']})
            
Dear Accounts Payable Team,

This is a formal notice regarding Invoice {inv['Invoice_ID']}, which was due on {inv['Due_Date']}.
Our records indicate an outstanding balance of {inv['Currency']} {inv['Amount_Remaining']:,.2f}.

Please confirm the payment status or provide a remittance advice by EOD.

Best Regards,
Treasury Operations Team"""
            st.text_area("Final Review", email_body, height=280)
            if st.button("📤 Dispatch Professional Notice"):
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DUNNING", "ID": inv['Invoice_ID'], "Detail": f"Sent to {target}"})
                st.success("Notice dispatched.")
        else: st.info("No overdue items found for the current search/filter.")

    with t3:
        c_flag, c_res = st.columns(2)
        with c_flag:
            to_freeze = st.selectbox("Invoice to Freeze", view_df[~view_df['Is_Disputed']]['Invoice_ID'])
            if st.button("🚩 Freeze Invoice"):
                idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_freeze][0]
                st.session_state.ledger.at[idx, 'Is_Disputed'] = True
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DISPUTE_FLAG", "ID": to_freeze, "Detail": "Manual Dispute"})
                st.rerun()
        with c_res:
            disputed = view_df[view_df['Is_Disputed']]
            if not disputed.empty:
                to_resolve = st.selectbox("Invoice to Unfreeze", disputed['Invoice_ID'])
                if st.button("✅ Resolve"):
                    idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_resolve][0]
                    st.session_state.ledger.at[idx, 'Is_Disputed'] = False
                    st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "RESOLVED", "ID": to_resolve, "Detail": "Issue Settled"})
                    st.rerun()
            else: st.info("No active disputes.")

elif menu == "📜 Audit":
    st.table(pd.DataFrame(st.session_state.audit))
