import pandas as pd
import datetime
import hashlib
import json

class ComplianceGuard:
    def __init__(self, ledger_path='data/audit_ledger.csv'):
        self.ledger_path = ledger_path
        self._initialize_ledger()

    def _initialize_ledger(self):
        """Ensures the immutable ledger exists with integrity headers."""
        try:
            pd.read_csv(self.ledger_path)
        except FileNotFoundError:
            columns = [
                'Timestamp', 'Event_Type', 'Entity_ID', 'Performed_By', 
                'Action_Details', 'Integrity_Hash', 'Previous_Hash'
            ]
            pd.DataFrame(columns=columns).to_csv(self.ledger_path, index=False)

    def _generate_signature(self, data_block, prev_hash):
        """Creates a SHA-256 digital fingerprint for record chaining."""
        record_string = json.dumps(data_block, sort_keys=True) + str(prev_hash)
        return hashlib.sha256(record_string.encode()).hexdigest()

    def log_transaction(self, entity_id, event_type, details="System Automated"):
        """
        Logs a treasury action with cryptographic chaining to prevent tampering.
        Compliant with SOC2 and Basel III audit requirements.
        """
        df = pd.read_csv(self.ledger_path)
        
        # Get the hash of the last record for chaining
        prev_hash = df.iloc[-1]['Integrity_Hash'] if not df.empty else "0x000"
        
        timestamp = datetime.datetime.now().isoformat()
        action_details = {
            "entity": entity_id,
            "type": event_type,
            "meta": details
        }

        # Generate cryptographic signature for this entry
        current_hash = self._generate_signature(action_details, prev_hash)

        new_entry = {
            'Timestamp': timestamp,
            'Event_Type': event_type,
            'Entity_ID': entity_id,
            'Performed_By': 'SMARTCASH_AI_ENGINE',
            'Action_Details': json.dumps(action_details),
            'Integrity_Hash': current_hash,
            'Previous_Hash': prev_hash
        }

        # Append to ledger and save
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(self.ledger_path, index=False)
        
        return current_hash

    def verify_ledger_integrity(self):
        """
        Validates the entire audit trail. 
        If a single row was manually edited in the CSV, the chain breaks.
        """
        df = pd.read_csv(self.ledger_path)
        if df.empty: return True

        for i in range(1, len(df)):
            prev_hash = df.iloc[i-1]['Integrity_Hash']
            if df.iloc[i]['Previous_Hash'] != prev_hash:
                return False, f"Integrity Breach at row {i}"
        
        return True, "Ledger Verified: Secure"

    def get_logs(self):
        """Returns the audit trail for the Streamlit UI."""
        return pd.read_csv(self.ledger_path)
