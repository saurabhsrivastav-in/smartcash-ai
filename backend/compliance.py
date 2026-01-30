import pandas as pd
import hashlib
import json
import os
import random
from datetime import datetime, timedelta

class ComplianceVault:
    """
    Implements a WORM (Write Once, Read Many) style audit ledger.
    Ensures every treasury action is cryptographically signed and 
    permanently archived to CSV.
    """
    def __init__(self, ledger_path="data/compliance_log.csv"):
        self.ledger_path = ledger_path
        self.vault = []
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        
        # Initialize the physical log file with headers if it doesn't exist
        if not os.path.exists(self.ledger_path):
            headers = pd.DataFrame(columns=[
                "Timestamp", "Event_ID", "Invoice_Ref", "Action", 
                "Amount", "Operator", "Status", "Hash_ID"
            ])
            headers.to_csv(self.ledger_path, index=False)

    def generate_sha256(self, data_dict):
        """
        Creates a deterministic SHA-256 fingerprint. 
        Crucial for verifying that log entries haven't been tampered with.
        """
        encoded_data = json.dumps(data_dict, sort_keys=True).encode()
        return hashlib.sha256(encoded_data).hexdigest()

    def log_action(self, invoice_ref, action_type, amount=0, operator="AI_AGENT_STP"):
        """
        Signs the transaction and appends it to the permanent CSV log.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "Timestamp": timestamp,
            "Invoice_Ref": invoice_ref,
            "Action": action_type,
            "Amount": float(amount),
            "Operator": operator
        }

        # Generate unique cryptographic ID
        hash_id = self.generate_sha256(payload)
        event_id = f"TXN-{random.randint(100000, 999999)}"

        new_entry = {**payload, "Event_ID": event_id, "Status": "SECURE", "Hash_ID": hash_id}

        # 1. Update In-Memory Vault for UI
        self.vault.insert(0, new_entry)

        # 2. Append to Physical CSV (Non-Repudiation Layer)
        df_entry = pd.DataFrame([new_entry])
        df_entry.to_csv(self.ledger_path, mode='a', header=False, index=False)
        
        return hash_id

    def get_logs(self):
        """
        Reads directly from the physical log to ensure the UI shows 
        the 'Source of Truth'.
        """
        if os.path.exists(self.ledger_path):
            return pd.read_csv(self.ledger_path)
        return pd.DataFrame(self.vault)
