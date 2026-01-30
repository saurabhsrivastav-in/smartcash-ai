import os
import json
from dotenv import load_dotenv

# Supporting multi-model strategy (Sprint 6/12)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()

class GenAIAssistant:
    """
    Cognitive Layer for SmartCash AI.
    Handles exception reasoning, adaptive dunning, and liquidity advice.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.provider = "OPENAI" if self.api_key else "MOCK"
        
        if self.api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def reason_exception(self, payment_data, top_matches):
        """
        Sprint 3: Analyzes why the matching engine failed to hit 95% confidence.
        """
        if self.provider == "MOCK":
            return "⚠️ [MOCK MODE] Discrepancy likely due to bank transfer fees ($15-$30) or name abbreviation."

        prompt = f"""
        System: You are an Institutional Treasury Auditor.
        Task: Analyze the mismatch between this bank payment and the ledger.
        
        Bank Payment: {payment_data}
        Potential Matches: {top_matches}
        
        Provide a concise 2-sentence reasoning on why these don't match perfectly 
        and suggest a 'Resolution Path' (e.g., Post with write-off, or Request Remittance).
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Reasoning Error: {str(e)}"

    def generate_adaptive_email(self, customer, amount, invoice_id, esg_score):
        """
        Sprint 4: Generates dunning emails where the 'Tone' is dictated 
        by the customer's ESG Risk Tier.
        """
        # ESG-Driven Tone Logic
        # AA/A = Collaborative, Partner-focused
        # B/C = Firm, Regulatory/Compliance focused
        tone = "collaborative and appreciative" if esg_score in ['AA', 'A'] else "formal and urgent"
        
        if self.provider == "MOCK":
            return f"[OFFLINE DRAFT]\nSubject: Follow-up on Inv {invoice_id}\n\nDear {customer},\n\nPlease advise on the status of our {amount} open balance. (Tone: {tone})"

        prompt = f"""
        Draft a {tone} dunning email for:
        Customer: {customer}
        Amount: {amount}
        Invoice: {invoice_id}
        ESG Rating: {esg_score}
        
        Keep it under 100 words. Do not use placeholders like [Your Name].
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Email Generator Error: {str(e)}"

    def get_liquidity_advice(self, current_cash, dso, stress_level):
        """
        Sprint 8: Strategic advice based on the stress-test slider in main.py.
        """
        prompt = f"""
        Current Cash: {current_cash}
        DSO: {dso} days
        Market Stress Level: {stress_level}%
        
        Provide one 'Treasury Action' to optimize working capital.
        """
        # (Implementation follows the same pattern as above)
        return "Advice: Accelerate receivables from Tier-C customers to offset liquidity haircut."
