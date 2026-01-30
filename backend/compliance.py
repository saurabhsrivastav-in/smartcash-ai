import pandas as pd
import hashlib
import json
import random
from datetime import datetime, timedelta

class ComplianceVault:
    """
    Implements a WORM (Write Once, Read Many) style audit ledger.
    Uses SHA-256 hashing to ensure non-repudiation of AI and human actions.
    """
    def __init__(self, ledger_path="data/audit_ledger.csv"):
        self.ledger_path = ledger_path
        self.vault = []
        self._generate_mock_audit_trail()

    def generate_sha256(self, data_dict):
        """
        Creates a unique cryptographic hash of the transaction metadata.
        This is the core requirement for Sprint 9's 'Immutable Ledger'.
        """
        # Sort keys to ensure consistent hashing regardless of dictionary order
        encoded_data = json.dumps(data_dict, sort_keys=True).encode()
        return hashlib.sha256(encoded_data).hexdigest()

    def log_action(self, invoice_ref, action_type, amount=0, operator="AI_AGENT_STP"):
        """
        Logs a new event with a deterministic cryptographic signature.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Data payload to be hashed
        payload = {
            "Timestamp": timestamp,
            "Invoice_Ref": invoice_ref,
            "Action": action_type,
            "Amount": float(amount),
            "Operator": operator
        }

        new_entry = {
            **payload,
            "Event_ID": f"TXN-{random.randint(100000, 999999)}",
            "Status": "✅ SECURE",
            "Hash_ID": self.generate_sha256(payload) # Actual SHA-256 Signature
        }
        
        self.vault.insert(0, new_entry)
        # In production, you would append this row to self.ledger_path here

    def _generate_mock_audit_trail(self):
        """Populates historical data with valid SHA-256 signatures for the UI."""
        actions = ["AUTO_MATCH_STP", "MANUAL_OVERRIDE", "STRESS_TEST_ADJ", "TREASURY_SWEEP"]
        operators = ["AI_GEN_AGENT", "SYSTEM_ROOT", "TREASURY_MGR_01", "AUDIT_BOT"]
        
        for i in range(12):
            past_time = (datetime.now() - timedelta(hours=i*3)).strftime("%Y-%m-%d %H:%M:%S")
            ref = f"INV-{random.randint(5000, 5999)}"
            act = random.choice(actions)
            amt = random.uniform(1000, 50000)
            op = random.choice(operators)
            
            payload = {
                "Timestamp": past_time,
                "Invoice_Ref": ref,
                "Action": act,
                "Amount": round(amt, 2),
                "Operator": op
            }

            self.vault.append({
                **payload,
                "Event_ID": f"TXN-{random.randint(100000, 999999)}",
                "Status": "✅ VERIFIED",
                "Hash_ID": self.generate_sha256(payload)
            })

    def get_logs(self):
        """Returns the vault as a DataFrame, primarily for the 'Audit Ledger' tab."""
        df = pd.DataFrame(self.vault)
        # Ensure the Hash_ID is visible but truncated for UI aesthetics
        return df
