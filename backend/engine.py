import pandas as pd
from fuzzywuzzy import fuzz

class SmartMatchingEngine:
    def __init__(self):
        # JPMC Standard: STP (Straight Through Processing) requires > 95% confidence
        self.auto_post_threshold = 0.95
        self.manual_review_threshold = 0.70
        
        # Simulated Entity Mapping (Parent-Subsidiary or Alias logic)
        self.entity_aliases = {
            "tesla motors": "tesla inc",
            "tesla germany gmbh": "tesla inc",
            "global blue se": "global blue ltd",
            "saurabh softwares": "saurabh soft"
        }

    def run_match(self, payment_amt, payer_name, currency, invoice_df):
        """
        Multi-Factor Reconciliation Engine
        Calculates a weighted confidence score based on:
        1. Amount & Currency Match (40%)
        2. Fuzzy Name Match with Alias Resolution (40%)
        3. Metadata/Reference Alignment (20%)
        """
        try:
            results = []
            # Safety check: Ensure columns exist
            required_cols = ['Amount', 'Customer', 'Invoice_ID', 'Currency']
            if not all(col in invoice_df.columns for col in required_cols):
                return []

            for _, inv in invoice_df.iterrows():
                try:
                    inv_amt = float(inv['Amount'])
                    pay_amt = float(payment_amt)
                except ValueError:
                    continue

                # --- 1. Amount & Currency Logic (Weight: 0.40) ---
                amt_score = 0.0
                if pay_amt == inv_amt and currency == inv['Currency']:
                    amt_score = 1.0
                elif abs(pay_amt - inv_amt) / inv_amt < 0.02: # Handle 2% variance/bank fees
                    amt_score = 0.7 
                
                # --- 2. Enhanced Name Matching (Weight: 0.40) ---
                # Resolve Aliases
                clean_payer = str(payer_name).lower().strip()
                resolved_payer = self.entity_aliases.get(clean_payer, clean_payer)
                clean_customer = str(inv['Customer']).lower().strip()
                
                # Use Token Set Ratio for handles like "Inc" or "Ltd" variations
                name_score = fuzz.token_set_ratio(resolved_payer, clean_customer) / 100

                # --- 3. Final Weighted Confidence Calculation ---
                # Formula: (Amount * 0.5) + (Name * 0.5) 
                # (Simplified for this version, but scalable to include Date/Ref)
                total_confidence = (amt_score * 0.5) + (name_score * 0.5)

                # --- 4. Categorization Logic ---
                if total_confidence >= self.auto_post_threshold:
                    status = "STP: Auto-Match"
                elif total_confidence >= self.manual_review_threshold:
                    status = "Exception: High Confidence"
                else:
                    status = "Exception: Low Confidence"

                if total_confidence > 0.50: # Only return plausible matches
                    results.append({
                        "Invoice_ID": inv['Invoice_ID'],
                        "Customer": inv['Customer'],
                        "Currency": inv['Currency'],
                        "confidence": round(total_confidence, 2),
                        "status": status,
                        "esg_score": inv.get('ESG_Score', 'N/A')
                    })

            # Sort by highest confidence
            return sorted(results, key=lambda x: x['confidence'], reverse=True)

        except Exception as e:
            print(f"Strategic Engine Error: {e}")
            return []
