import datetime

class GenAIAssistant:
    def __init__(self, model_provider="Gemini-3-Flash"):
        self.model_provider = model_provider
        self.bank_name = "SmartCash Institutional Treasury"
        
    def generate_email(self, customer_name, amount_received, invoice_data=None):
        """
        Generates a professional, multi-factor dispute or reconciliation email.
        Incorporates 'Human-in-the-Loop' logic to ensure institutional tone.
        """
        
        # Determine context: Is this a full match or a discrepancy?
        # In a real app, invoice_data would be a dictionary from our engine.
        expected_amt = invoice_data.get('Amount', 0) if invoice_data else amount_received
        variance = expected_amt - amount_received
        currency = invoice_data.get('Currency', 'USD') if invoice_data else "USD"
        
        # 1. Logic for Short-Pay (Variance handling)
        if variance > 0:
            subject = f"URGENT: Payment Discrepancy Action Required - {customer_name} | Ref: {datetime.date.today()}"
            body = self._compose_short_pay_body(customer_name, amount_received, variance, currency)
        else:
            subject = f"Payment Confirmation & Reconciliation - {self.bank_name}"
            body = self._compose_standard_receipt(customer_name, amount_received, currency)

        return f"Subject: {subject}\n\n{body}"

    def _compose_short_pay_body(self, customer, received, variance, currency):
        return f"""
Dear {customer} Accounts Payable Team,

We have received your recent remittance of {currency} {received:,.2f}. 

Upon reconciliation against our subledger, we have noted a variance of {currency} {variance:,.2f} compared to the outstanding invoice balance. 

**Action Required:**
Please provide a reason code for this deduction (e.g., Bank Fees, Quality Dispute, or Tax Withholding) within 48 business hours to ensure your account remains in good standing and to avoid automated dunning escalations.

Should you require a copy of the original statement, please reply to this thread.

Regards,

The Treasury Operations Team
{self.bank_name}
[Automated via SmartCash AI Governance Layer]
"""

    def _compose_standard_receipt(self, customer, received, currency):
        return f"""
Dear {customer},

This is an automated confirmation that your payment of {currency} {received:,.2f} has been successfully reconciled and posted to your account. 

No further action is required at this time. Thank you for your continued partnership.

Regards,
{self.bank_name}
"""

    def generate_risk_report(self, customer_name, esg_score, exposure_amt):
        """
        Generates an internal briefing for the Credit Risk Committee regarding
        low-rated ESG counterparties.
        """
        return f"""
        INTERNAL MEMORANDUM: High-Risk Counterparty Alert
        ------------------------------------------------
        Entity: {customer_name}
        Risk Rating: {esg_score}
        Current Exposure: ${exposure_amt:,.2f}
        
        Recommendation: Based on the current '{esg_score}' ESG rating and Basel III 
        compliance guidelines, it is recommended to transition this account to 
        'Pre-payment Only' status to mitigate potential credit default risk.
        """
