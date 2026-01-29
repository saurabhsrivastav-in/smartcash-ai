import pandas as pd
from fuzzywuzzy import fuzz

class SmartMatchingEngine:
    def __init__(self):
        self.trust_threshold = 0.95 

    def run_match(self, payment_amt, payer_name, invoice_df):
        try:
            results = []
            # Safety check: Ensure columns exist
            required_cols = ['Amount', 'Customer', 'Invoice_ID']
            if not all(col in invoice_df.columns for col in required_cols):
                return []

            for _, inv in invoice_df.iterrows():
                # Handling potential data type errors
                try:
                    inv_amt = float(inv['Amount'])
                except ValueError:
                    continue

                amt_match = (float(payment_amt) == inv_amt)
                name_score = fuzz.token_sort_ratio(str(payer_name).lower(), str(inv['Customer']).lower()) / 100
                
                if amt_match and name_score > 0.90:
                    confidence, status = 1.0, "Auto-Match"
                elif name_score > 0.70:
                    confidence, status = name_score, "Suggested"
                else:
                    continue

                results.append({
                    "Invoice_ID": inv['Invoice_ID'],
                    "Customer": inv['Customer'],
                    "confidence": confidence,
                    "status": status
                })

            return sorted(results, key=lambda x: x['confidence'], reverse=True)
        except Exception as e:
            print(f"Engine Error: {e}")
            return []
