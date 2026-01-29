import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TreasuryManager:
    def __init__(self):
        self.target_dso = 30.0  # Days Sales Outstanding Target
        self.risk_free_rate = 0.045  # 4.5% Annual (Simulation of Treasury Yield)

    def calculate_liquidity_health(self, invoices_df):
        """
        Calculates institutional liquidity metrics:
        1. Weighted Average Days Sales Outstanding (DSO)
        2. Cash Concentration Risk
        3. Estimated Interest Income Lost (Opportunity Cost of unapplied cash)
        """
        if invoices_df.empty:
            return {}

        # 1. DSO Calculation
        # Simulation: Difference between current date and Due Date for Open invoices
        today = datetime.now()
        open_invoices = invoices_df[invoices_df['Status'] == 'Open'].copy()
        
        # Calculate days overdue
        open_invoices['Days_Overdue'] = (today - pd.to_datetime(open_invoices['Due_Date'])).dt.days
        avg_dso = open_invoices['Days_Overdue'].mean() if not open_invoices.empty else 0

        # 2. Opportunity Cost (The 'JPMC' Metric)
        # Formula: (Total Unapplied Cash * Risk Free Rate) / 365 * DSO
        total_unapplied = open_invoices['Amount'].sum()
        daily_opportunity_cost = (total_unapplied * self.risk_free_rate) / 365
        total_loss = daily_opportunity_cost * max(0, avg_dso)

        # 3. Concentration Risk
        concentration = open_invoices.groupby('Customer')['Amount'].sum() / total_unapplied
        high_risk_entities = concentration[concentration > 0.20].to_dict() # Entities > 20% exposure

        return {
            "avg_dso": round(avg_dso, 1),
            "opportunity_cost_usd": round(total_loss, 2),
            "concentration_risk": high_risk_entities,
            "liquidity_position": total_unapplied
        }

    def get_cash_forecast(self, invoices_df, horizon_days=90):
        """
        Generates a 90-day cash inflow forecast.
        Adjusts expected payment dates based on ESG scores (Risk-Adjusted Forecasting).
        """
        open_invoices = invoices_df[invoices_df['Status'] == 'Open'].copy()
        open_invoices['Due_Date'] = pd.to_datetime(open_invoices['Due_Date'])
        
        # Risk-Adjustment Logic: 
        # ESG 'E' rated clients are modeled to pay 15 days late
        # ESG 'AAA' rated clients pay on time
        def adjust_date(row):
            delay = 0
            if row['ESG_Score'] in ['E', 'D']: delay = 15
            elif row['ESG_Score'] == 'C': delay = 7
            return row['Due_Date'] + timedelta(days=delay)

        open_invoices['Expected_Payment_Date'] = open_invoices.apply(adjust_date, axis=1)
        
        forecast = open_invoices.groupby('Expected_Payment_Date')['Amount'].sum().reset_index()
        forecast = forecast.sort_values(by='Expected_Payment_Date')
        
        return forecast

    def get_fx_exposure(self, invoices_df):
        """Identifies net exposure by currency for FX hedging strategies."""
        exposure = invoices_df.groupby('Currency')['Amount'].sum().to_dict()
        return exposure
