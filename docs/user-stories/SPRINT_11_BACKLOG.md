# 🛡️ Sprint 11 Backlog: Post-Quantum Security & T+0 Readiness

**Sprint Goal:** Implement Post-Quantum Cryptographic (PQC) standards for data-at-rest and prepare the engine for real-time, T+0 settlement reconciliation.

---

## 🏗️ Story 11.1: Post-Quantum Cryptographic (PQC) Hardening
**User Persona:** As a Chief Information Security Officer (CISO), I want our financial data encrypted using quantum-resistant algorithms so that our long-term treasury secrets are protected against "Harvest Now, Decrypt Later" attacks.

### 📝 Description
Upgrade the encryption layer for the `Audit Ledger` and `Customer_PII` data. Transition from standard AES/RSA to NIST-approved post-quantum algorithms (e.g., CRYSTALS-Kyber or Dilithium) for data-at-rest.

### ✅ Acceptance Criteria
- [ ] **Algorithm Migration:** Implement a PQC wrapper for the sensitive columns in the `invoices.csv` and `compliance_vault`.
- [ ] **Performance Impact:** Ensure that PQC encryption/decryption does not increase dashboard latency by more than 15%.
- [ ] **Key Rotation:** Implement an automated key rotation policy logged in the system's internal security heartbeat.



---

## 🏗️ Story 11.2: Real-Time T+0 Settlement Reconciliation
**User Persona:** As a Treasury Manager, I want the system to reconcile payments in real-time (FedNow / SEPA Instant) rather than waiting for batch processing, so we can achieve true intraday liquidity.

### 📝 Description
Refactor the ingestion engine to support "Stream Ingestion" rather than "Batch Loading." The engine must trigger the matching logic the moment a single JSON-based ISO 20022 message is received.

### ✅ Acceptance Criteria
- [ ] **Latency Gate:** Matching logic for a single T+0 transaction must complete in < 200ms.
- [ ] **Immediate Posting:** Successfully identifies and "pre-posts" matches before the end-of-day bank statement is generated.
- [ ] **UI Update:** Add a "Live Feed" ticker to the Executive Dashboard showing real-time reconciled value.

---

## 🏗️ Story 11.3: ISO 20022 camt.053 Rich Data Parsing
**User Persona:** As an AR Analyst, I want the system to utilize the "Ultimate Debtor" and "Remittance Information" fields in camt.053 messages to improve STP rates for complex global payments.

### 📝 Description
Upgrade the MT942 parser to a full XML-based ISO 20022 `camt.053` parser. This allows the engine to extract rich metadata that is often lost in legacy bank formats.

### ✅ Acceptance Criteria
- [ ] **XML Mapping:** Correctly maps `<UltmtDbtr>` and `<RmtInf>` tags to the `SmartMatchingEngine`.
- [ ] **Enhanced STP:** Use the structured remittance data to achieve a 99%+ match rate for ISO-compliant payments.
- [ ] **Fallback Logic:** Maintain backward compatibility for legacy MT940/MT942 formats.



---

## 🏗️ Story 11.4: Anomaly Detection (Fraud Prevention)
**User Persona:** As a Risk Manager, I want the system to flag "Velocity Anomalies" or "Bank Account Mismatches" so we can prevent redirection fraud and unauthorized payment tampering.

### 📝 Description
Implement a machine-learning-based anomaly detection layer. The system flags transactions that deviate significantly from a customer’s historical payment "fingerprint" (e.g., new bank account, unusual time of day, or strange amount).

### ✅ Acceptance Criteria
- [ ] **Anomaly Scoring:** Every match receives a "Fraud Probability Score" (0.0 to 1.0).
- [ ] **Isolation:** High-risk anomalies are automatically quarantined in a "Fraud Review" tab.
- [ ] **Audit Trail:** Log the specific reason for the fraud flag (e.g., "New Beneficiary Account Detected").

---

## 🚀 Technical Sub-tasks for Developers
1. **Security:** Research and integrate a PQC library (e.g., `liboqs` or a Python wrapper for Dilithium).
2. **Protocol Upgrade:** Develop `backend/iso20022_parser.py` using `lxml` for high-performance XML parsing.
3. **Data Science:** Implement an Isolation Forest or One-Class SVM model for `anomaly_detection.py`.
4. **Mock Data:** Update `mock_data_maker.py` to generate XML-based camt.053 files and "fraudulent" payment outliers.
