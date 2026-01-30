# 🌐 Sprint 7 Backlog: Ecosystem Synergy & CRM Intelligence

**Sprint Goal:** Integrate Salesforce/CRM metadata and Credit Agency signals to provide a 360-degree view of counterparty risk and behavioral payment patterns.

---

## 🏗️ Story 7.1: Salesforce/CRM Metadata Integration
**User Persona:** As an AR Analyst, I want to see "Collection Notes" from the sales team within my workbench so I know if a payment delay is due to a known service dispute.

### 📝 Description
Develop a data connector that pulls qualitative data from CRM objects. This context is displayed in a "Context Sidebar" when an analyst reviews a transaction, preventing redundant customer outreach.

### ✅ Acceptance Criteria
- [ ] **Data Bridge:** Successfully maps `Customer_ID` to CRM "Open Cases" or "Account Notes."
- [ ] **UI Integration:** Analyst Workbench displays the last 3 CRM interactions for the selected payer.
- [ ] **AI Context:** The `GenAIAssistant` is updated to reference CRM notes (e.g., "I see there was a dispute regarding shipment #402...") in dunning drafts.



---

## 🏗️ Story 7.2: Credit Agency Signal Integration (D&B / Experian)
**User Persona:** As a Credit Manager, I want to see external credit score changes in real-time so I can adjust credit limits before a customer defaults.

### 📝 Description
Integrate a mock API for external credit rating agencies. If a customer's external rating drops, the SmartCash AI engine automatically increases the "Match Rigor" (requiring 99% confidence instead of 90% for STP).

### ✅ Acceptance Criteria
- [ ] **API Handler:** Ingests external rating scores (e.g., 1-100 scale).
- [ ] **Dynamic Thresholds:** System automatically flags any "High Risk" matches where the external score is below 40.
- [ ] **Dashboard Update:** The **Risk Radar** now includes a toggle to overlay "External Risk" vs "Internal Payment History."

---

## 🏗️ Story 7.3: The "Payment Personality" Profile
**User Persona:** As a Treasurer, I want a behavioral profile for each customer so I can predict who pays late by habit versus who is in genuine financial distress.

### 📝 Description
Create a behavioral analytics layer. Using historical data, the system classifies customers into "Payment Personalities" (e.g., *Early Bird, Habitual Laggard, Seasonal Delinquent*).

### ✅ Acceptance Criteria
- [ ] **Classification Engine:** Uses `scipy` to cluster customers based on "Days Past Due" (DPD) variance.
- [ ] **Visual Profile:** Each customer in the Analyst Workbench gets a "Behavioral Badge."
- [ ] **Liquidity Impact:** Habitual Laggards are excluded from "Opening Cash" projections in the Waterfall chart.



---

## 🏗️ Story 7.4: Automated Credit Limit Enforcement
**User Persona:** As a Finance Director, I want the system to block new order releases if a customer's "Unapplied Cash" + "Open Invoices" exceeds their credit ceiling.

### 📝 Description
Develop a "Credit Breach" alert system. The engine calculates "Net Exposure" in real-time and generates a JSON payload for the ERP/Order Management system to hold new shipments.

### ✅ Acceptance Criteria
- [ ] **Exposure Logic:** `Exposure = (Sum of Open Invoices) - (Unidentified Credits in Bank Feed)`.
- [ ] **Real-time Alert:** Visual "Breach" indicator in the Executive Dashboard for Top 5 at-risk accounts.
- [ ] **Compliance Log:** Every credit breach is logged with a timestamp in the SOC2 Compliance Vault.

---

## 🚀 Technical Sub-tasks for Developers
1. **API Development:** Create `services/crm_service.py` with mock Salesforce REST endpoints.
2. **Data Science:** Refactor `backend/engine.py` to accept "External_Risk_Score" as a weighting variable in the matching algorithm.
3. **UI Polish:** Add a "Customer 360" modal in the Streamlit interface using `st.expander`.
4. **Mock Data:** Update `mock_data_maker.py` to include a `Credit_Limit` column and `External_Rating` values for the 200 rows.
