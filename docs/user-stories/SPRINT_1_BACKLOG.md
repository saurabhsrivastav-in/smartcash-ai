# 🔍 Sprint 1 Backlog: Foundation & Exact Match Engine

**Sprint Goal:** Establish a robust data pipeline for bank/invoice data and achieve 100% accuracy for "Level 1" Exact Matches.

---

## 🏗️ Story 1.1: Multi-Currency Data Ingestion Layer
**User Persona:** As a Treasury IT Analyst, I want a standardized way to ingest bank and invoice data so that the engine processes consistent formats across USD, EUR, and GBP.

### 📝 Description
Develop the `load_data()` utility to parse raw CSV/MT942 exports. The logic must normalize currency symbols and date formats to ensure compatibility with downstream analytics.

### ✅ Acceptance Criteria
- [ ] Logic parses `Due_Date` into standard Python `datetime` objects.
- [ ] Currency normalization: Handles symbols ($, €, £) and ensures `Amount` is stored as a float.
- [ ] **Validation:** System throws a clear `st.error` if mandatory columns (Invoice_ID, Amount) are missing.
- [ ] **Mock Integration:** Successful execution of `mock_data_maker.py` generates the required schema.

---

## 🏗️ Story 1.2: Level 1 "Exact Match" Logic Gate
**User Persona:** As a Finance Manager, I want the system to auto-clear perfect matches so that the team can focus solely on complex exceptions.

### 📝 Description
Develop the first gate of the **Waterfall Matching Engine**. This story focuses on "Scenario A": High-confidence matching where the bank record exactly mirrors the ERP record.



### ✅ Acceptance Criteria
- [ ] **Gate Criteria:** Match triggered ONLY if `Bank_Amount == Invoice_Amount` AND `Bank_Currency == Invoice_Currency` AND `Bank_Ref == Invoice_ID`.
- [ ] **Conflict Resolution:** System flags an exception if one Bank Reference matches multiple Invoice IDs with the same amount.
- [ ] **Output:** Returns a `confidence_score = 1.0` for all Level 1 matches.

---

## 🏗️ Story 1.3: Executive Liquidity Visualization
**User Persona:** As a CFO, I want to see a high-level view of our cash position so I can assess liquidity health at a glance.

### 📝 Description
Implement the **Executive Dashboard** view in Streamlit using Plotly. This includes the Liquidity Bridge (Waterfall chart) and top-level KPIs.

### ✅ Acceptance Criteria
- [ ] **Waterfall Chart:** Displays "Opening Cash" -> "Expected AR" -> "Net Position" using `go.Waterfall`.
- [ ] **KPI Metrics:** Display "Adjusted DSO", "Liquidity Buffer", and "Available Cash" using `st.metric`.
- [ ] **Visual Integrity:** Ensure the dashboard uses the custom dark-banking CSS theme.

---

## 🏗️ Story 1.4: The SOC2 Compliance Vault (Alpha)
**User Persona:** As a Compliance Officer, I want every automated match to be logged so that we have an immutable audit trail for internal controls.

### 📝 Description
Initialize the `ComplianceGuard` backend to log transactions. Every match must generate a unique fingerprint to ensure non-repudiation.

### ✅ Acceptance Criteria
- [ ] **Logging:** Capture `Invoice_ID`, `Amount`, `Timestamp`, and `Match_Method`.
- [ ] **Hashing:** Generate a SHA-256 hash for each entry to simulate a "locked" ledger.
- [ ] **UI:** Create the "Audit Ledger" view in Streamlit to display these logs in a searchable table.

---

## 🚀 Technical Sub-tasks for Developers
1. **Engine Architecture:** Implement `SmartMatchingEngine.run_match()` method in `backend/engine.py`.
2. **State Management:** Set up `st.session_state` to persist the `audit_engine` across navigation tabs.
3. **Mock Data Tuning:** Update `mock_data_maker.py` to include at least 20% "Perfect Matches" to test Story 1.2.
4. **Performance:** Ensure the `Waterfall` chart renders in < 500ms for 200 rows of data.
