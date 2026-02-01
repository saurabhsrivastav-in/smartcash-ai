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

# --- 2. DATA ENGINE ---
@st.cache_data
def load_institutional_data():
    try:
        inv_df = pd.read_csv("data/invoices.csv")
        bank_df = pd.read_csv("data/bank_feed.csv")
        
        # Standardize all headers to Title_Case with no spaces
        inv_df.columns = [str(c).strip().replace(' ', '_').title() for c in inv_df.columns]
        bank_df.columns = [str(c).strip().replace(' ', '_').title() for c in bank_df.columns]

        # Explicitly map the specific columns causing the KeyError
        inv_df = inv_df.rename(columns={
            'Invoice': 'Invoice_ID',
            'Inv_No': 'Invoice_ID',
            'Amount': 'Amount_Remaining',
            'Balance': 'Amount_Remaining'
        })
        
        # Ensure 'Customer' column exists in both
        if 'Customer_Name' in inv_df.columns: inv_df.rename(columns={'Customer_Name': 'Customer'}, inplace=True)
        if 'Payer' in bank_df.columns: bank_df.rename(columns={'Payer': 'Customer'}, inplace=True)

        return inv_df, bank_df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame(columns=['Customer', 'Invoice_ID', 'Amount_Remaining']), pd.DataFrame()
        
        # 3. SAFETY DEFAULTS: Prevents "Column Unavailable" crashes
        required_cols = {
            'Is_Disputed': False,
            'Status': 'Open',
            'Esg_Score': 'A',
            'Company_Code': 'Main_Entity',
            'Currency': 'USD'
        }
        for col, default in required_cols.items():
            if col not in inv_df.columns:
                inv_df[col] = default

        # 4. DATA TYPES
        inv_df['Due_Date'] = pd.to_datetime(inv_df['Due_Date'], errors='coerce')
        bank_df['Date'] = pd.to_datetime(bank_df.get('Date'), errors='coerce')
        
        return inv_df, bank_df
    except Exception as e:
        st.error(f"⚠️ Initialization Error: {e}")
        # Returns empty dataframes with correct columns so features don't disappear
        return pd.DataFrame(columns=['Customer', 'Invoice_ID', 'Amount_Remaining', 'Due_Date', 'Status', 'Company_Code', 'Esg_Score', 'Is_Disputed', 'Currency']), pd.DataFrame()
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
    chat_term = st.text_input("🤖 AI Assistant", key="chat_key")
with h_col3:
    st.write(" ")
    st.button("🗑️ Clear All", on_click=handle_clear)

st.divider()

# --- 5. SEARCH & FILTER LOGIC ---
view_df = st.session_state.ledger.copy()

if not view_df.empty:
    if search_term:
        view_df = view_df[view_df['Customer'].astype(str).str.contains(search_term, case=False) | 
                          view_df['Invoice_ID'].astype(str).str.contains(search_term, case=False)]
    elif chat_term:
        view_df = view_df[view_df['Customer'].astype(str).str.contains(chat_term, case=False) | 
                          view_df['Invoice_ID'].astype(str).str.contains(chat_term, case=False)]

with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Workbench", "📜 Audit"])
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    
    if 'Company_Code' in st.session_state.ledger.columns and not st.session_state.ledger.empty:
        entities = ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique())
        ent_f = st.selectbox("Company Entity", entities)
    else:
        st.warning("⚠️ 'Company_Code' column not found.")
        ent_f = "Consolidated"
    
    st.divider()
    stress_test = st.toggle("Enable Stress Loading", help="Simulate high-risk market conditions")

if ent_f != "Consolidated" and not view_df.empty:
    if 'Company_Code' in view_df.columns:
        view_df = view_df[view_df['Company_Code'] == ent_f]
    
if 'Amount_Remaining' in view_df.columns and not view_df.empty:
    liq_pool = (pd.to_numeric(view_df['Amount_Remaining'], errors='coerce').sum() / 1e6) - (latency * 0.12)
else:
    liq_pool = 0.0

today = datetime(2026, 1, 30)

# --- 6. WORKSPACE ---

if menu == "📈 Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Cash Conversion Cycle", f"{42+latency} Days", f"{'+3d' if stress_test else '-1d'}", delta_color="inverse")
    m2.metric("Filtered Liquidity", f"${liq_pool:.2f}M")
    m3.metric("Adjusted DSO", f"{34+latency}d")
    m4.metric("Matching Items", len(view_df))

    st.divider()

    st.subheader("📈 Multi-Year Liquidity Trend & Forecast")
    quarters = ['Q1 24', 'Q2 24', 'Q3 24', 'Q4 24', 'Q1 25', 'Q2 25', 'Q3 25', 'Q4 25', 'Q1 26 (Est)', 'Q2 26 (Est)', 'Q3 26 (Est)', 'Q4 26 (Est)', 'Q1 27 (Proj)']
    cash_values = [45, 48, 42, 55, 58, 62, 59, 70, liq_pool, liq_pool * 1.1, liq_pool * 1.05, liq_pool * 1.2, liq_pool * 1.25]
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=quarters[:8], y=cash_values[:8], mode='lines+markers', name='Historical', line=dict(color='#58a6ff', width=3)))
    fig_trend.add_trace(go.Scatter(x=quarters[7:], y=cash_values[7:], mode='lines+markers', name='Forecast', line=dict(color='#238636', width=3, dash='dot')))
    
    fig_trend.update_layout(
        template="plotly_dark", height=400,
        xaxis_title="Time Period (Multi-Year)",
        yaxis_title="Total Liquidity ($ Millions)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.divider()

    st.subheader("⏳ Accounts Receivable Ageing Analysis")

    if 'Status' in view_df.columns and not view_df.empty:
        ov = view_df[view_df['Status'] == 'Overdue'].copy()
        
        if not ov.empty and 'Due_Date' in ov.columns:
            ov['Due_Date'] = pd.to_datetime(ov['Due_Date'])
            
            def get_bucket(invoice_date):
                try:
                    diff = (today - invoice_date).days
                    if diff <= 15: return "0-15"
                    elif diff <= 30: return "16-30"
                    elif diff <= 60: return "31-60"
                    elif diff <= 90: return "61-90"
                    elif diff <= 120: return "91-120"
                    elif diff <= 180: return "121-180"
                    elif diff <= 360: return "181-360"
                    else: return "361+"
                except: return "Unknown"

            ov['Bucket'] = ov['Due_Date'].apply(get_bucket)
            order = ["0-15", "16-30", "31-60", "61-90", "91-120", "121-180", "181-360", "361+"]
            age_data = ov.groupby('Bucket')['Amount_Remaining'].sum().reindex(order, fill_value=0).reset_index()
            
            fig_age = px.bar(age_data, x='Bucket', y='Amount_Remaining', 
                             labels={'Bucket': 'Days Past Due (DPD)', 'Amount_Remaining': 'Balance ($)'},
                             color='Amount_Remaining', color_continuous_scale='Turbo')
            fig_age.update_layout(template="plotly_dark", height=450)
            st.plotly_chart(fig_age, use_container_width=True)
        else: 
            total_pending = view_df['Amount_Remaining'].sum()
            st.info(f"✅ No overdue items found for the current selection.")
            st.metric("Total Outstanding (Current)", f"${total_pending:,.2f}")
            
            st.write("📅 **Upcoming Receivables (Next 30 Days):**")
            upcoming = view_df[view_df['Status'] != 'Overdue'].sort_values('Due_Date').head(5)
            if not upcoming.empty:
                st.dataframe(upcoming[['Customer', 'Due_Date', 'Amount_Remaining']], use_container_width=True)
    else:
        st.warning("Data or 'Status' column unavailable.")

    st.divider()

    st.subheader("🔥 Interactive Stress Matrix (FX vs Hedge)")
    fx_range = np.array([-15, -10, -5, -2, 0, 5, 10])
    hedge_range = np.array([0, 25, 50, 75, 100])
    multiplier = 0.85 if stress_test else 1.0
    z_data = [[round(liq_pool * multiplier * (1 + (fx/100) * (1 - (h/100))), 2) for h in hedge_range] for fx in fx_range]

    fig_h = go.Figure(data=go.Heatmap(
        z=z_data, x=[f"{h}% Hedge" for h in hedge_range], y=[f"{fx}% Vol" for fx in fx_range],
        colorscale='RdYlGn', text=z_data, texttemplate="$%{text}M", hoverinfo="z"
    ))
    fig_h.update_layout(template="plotly_dark", height=400, xaxis_title="Hedge Coverage", yaxis_title="FX Volatility (%)")
    st.plotly_chart(fig_h, use_container_width=True)

elif menu == "🛡️ Risk Radar":
    if not view_df.empty:
        weights = {'AAA':0.05, 'AA':0.1, 'A':0.2, 'B':0.4, 'C':0.6, 'D':0.9}
        
        # Safe column processing
        for col in ['Company_Code', 'Currency', 'ESG_Score', 'Customer']:
            if col in view_df.columns:
                view_df[col] = view_df[col].astype(str).replace('nan', 'Unknown')
            else:
                view_df[col] = "Unknown"
        
        view_df['Amount_Remaining'] = pd.to_numeric(view_df['Amount_Remaining'], errors='coerce').fillna(0)
        
        if 'ESG_Score' in view_df.columns:
            view_df['Exposure'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights).fillna(0)
        else:
            view_df['Exposure'] = 0
            
        view_df['Amount_M'] = view_df['Amount_Remaining'] / 1_000_000

        fig_s = px.sunburst(
            view_df, 
            path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], 
            values='Exposure', 
            color='ESG_Score',
            color_discrete_map={
                'AAA':'#238636', 'AA':'#2ea043', 'A':'#d29922', 
                'B':'#db6d28', 'C':'#f85149', 'D':'#b62323'
            },
            hover_data=['Amount_M']
        )
        
        fig_s.update_traces(
            hovertemplate="<b>%{label}</b><br>" + 
                          "Total Value: $%{customdata[0]:,.4f}M<br>" + 
                          "Risk Exposure: $%{value:,.2f}<extra></extra>"
        )

        fig_s.update_layout(height=700, template="plotly_dark")
        st.plotly_chart(fig_s, use_container_width=True)
    else:
        st.info("Please ensure data is loaded to view Risk Radar.")

elif menu == "⚡ Workbench":
    st.subheader("⚡ Operational Command")
    t1, t2, t3 = st.tabs(["🧩 AI Matcher", "📩 Dunning Center", "🛠️ Dispute Resolver"])
    
    with t1:
        st.write("**Intelligent Bank Reconciliation**")
        match_df = st.session_state.bank.copy()
        ledger_ref = st.session_state.ledger
        
        # Check if necessary columns exist to prevent KeyError
        if not match_df.empty and 'Customer' in match_df.columns and 'Invoice_ID' in ledger_ref.columns:
            
            # SAFER MATCHING LOGIC
            def get_invoice(customer_name):
                match = ledger_ref[ledger_ref['Customer'] == customer_name]
                return match['Invoice_ID'].values[0] if not match.empty else "No Match"

            match_df['Suggested_Invoice'] = match_df['Customer'].apply(get_invoice)
            st.dataframe(match_df, use_container_width=True)
            st.info("AI Matcher identified links between receipts and receivables.")
        else:
            st.warning("Cannot run Matcher. Ensure 'invoices.csv' has an 'Invoice_ID' column and both files have 'Customer'.")

    with t2:
        ov = view_df[view_df['Status'] == 'Overdue'] if 'Status' in view_df.columns else pd.DataFrame()
        if not ov.empty:
            target = st.selectbox("Select Debtor", ov['Customer'].unique())
            inv = ov[ov['Customer'] == target].iloc[0]
            st.markdown("### 📧 Professional Notice Draft")
            
          # 1. First, create the safe ID variable
inv_id = inv.get('Invoice_ID', inv.get('Invoice', 'N/A')) 

# 2. Use 'inv_id' everywhere inside the f-string (DO NOT use inv['Invoice_ID'])
email_body = f"""Subject: URGENT: Payment Overdue for {inv['Customer']} ({inv_id})

Dear Accounts Payable Team,

This is a formal notice regarding Invoice {inv_id}, which was due on {inv['Due_Date']}.
Our records indicate an outstanding balance of {inv.get('Currency', 'USD')} {inv['Amount_Remaining']:,.2f}.

Please confirm the payment status or provide a remittance advice by EOD.

Best Regards,
Treasury Operations Team"""
            
            st.text_area("Final Review", email_body, height=280)
            
            if st.button("📤 Dispatch Professional Notice"):
                st.session_state.audit.insert(0, {
                    "Time": datetime.now().strftime("%H:%M"), 
                    "Action": "DUNNING", 
                    "ID": inv['Invoice_ID'], 
                    "Detail": f"Sent to {target}"
                })
                st.success("Notice dispatched.")
        else: 
            st.info(f"✅ No overdue items found for dunning.")

    with t3:
        c_flag, c_res = st.columns(2)
        if not view_df.empty:
            with c_flag:
                not_disputed = view_df[~view_df['Is_Disputed']]
                if not not_disputed.empty:
                    to_freeze = st.selectbox("Invoice to Freeze", not_disputed['Invoice_ID'])
                    if st.button("🚩 Freeze Invoice"):
                        idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_freeze][0]
                        st.session_state.ledger.at[idx, 'Is_Disputed'] = True
                        st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DISPUTE_FLAG", "ID": to_freeze, "Detail": "Manual Dispute"})
                        st.rerun()
                else:
                    st.info("No invoices available to freeze.")
                    
            with c_res:
                disputed = view_df[view_df['Is_Disputed']]
                if not disputed.empty:
                    to_resolve = st.selectbox("Invoice to Unfreeze", disputed['Invoice_ID'])
                    if st.button("✅ Resolve"):
                        idx = st.session_state.ledger.index[st.session_state.ledger['Invoice_ID'] == to_resolve][0]
                        st.session_state.ledger.at[idx, 'Is_Disputed'] = False
                        st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "RESOLVED", "ID": to_resolve, "Detail": "Issue Settled"})
                        st.rerun()
                else: 
                    st.info("No active disputes.")
        else:
            st.info("Workbench requires active ledger data.")

elif menu == "📜 Audit":
    st.write("### 📜 System Audit Log")
    if st.session_state.audit:
        audit_df = pd.DataFrame(st.session_state.audit)
        st.table(audit_df)
        if st.button("🗑️ Clear Log"):
            st.session_state.audit = []
            st.rerun()
    else:
        st.info("No actions logged yet.")
