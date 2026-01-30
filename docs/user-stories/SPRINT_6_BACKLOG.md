# 🤖 Sprint 6 Backlog: Cognitive Automation & Predictive Ops

**Sprint Goal:** Deploy advanced GenAI for unstructured remittance scraping and implement the predictive engine for DSO drift forecasting.

---

## 🏗️ Story 6.1: Cognitive Remittance Scraping (OCR + LLM)
**User Persona:** As an AR Analyst, I want the system to read PDF and Image remittance advices so that I don't have to manually type data from customer portals.

### 📝 Description
Develop a "Remittance Ingestion" pipeline. This uses OCR to extract text from unstructured documents and an LLM to map that text into a structured JSON format (Invoice ID, Amount, Payer).

### ✅ Acceptance Criteria
- [ ] **Extraction:** Successfully extracts `Invoice_ID` and `Amount` from 5 different PDF layouts.
- [ ] **Heuristic Mapping:** The LLM correctly identifies "Short-Pay Reason Codes" (e.g., "damaged goods", "tax withholding").
- [ ] **Workbench Integration:** Extracted data appears as a "Suggested Match" with a `Source: PDF_Remittance` tag.



---

## 🏗️ Story 6.2: Predictive DSO Drift Engine
**User Persona:** As a CFO, I want to see which customers are likely to pay late next month so I can adjust our liquidity forecast.

### 📝 Description
Implement a predictive model using `scipy.stats` and historical payment behavior. The engine analyzes the delta between `Due_Date` and `Actual_Payment_Date` to assign a "Payment Personality" score to each customer.

### ✅ Acceptance Criteria
- [ ] **Drift Calculation:** Calculates the `Average_Days_Late` per customer over a 6-month rolling window.
- [ ] **Visualization:** A "DSO Heatmap" showing customers trending toward higher delinquency.
- [ ] **Stress Test Linkage:** The "Liquidity Bridge" updates its "Expected Collections" bar based on these predictive delays rather than just static due dates.

---

## 🏗️ Story 6.3: Autonomous Dunning Workflows
**User Persona:** As a Credit Manager, I want the system to automatically send follow-up emails for Scenario D (Unidentified Payments) without my manual approval for low-value items.

### 📝 Description
Establish an "Autonomous Threshold" (e.g., for payments < $5,000). If the confidence score is below 70%, the GenAI agent sends the drafted remittance request automatically.

### ✅ Acceptance Criteria
- [ ] **Policy Engine:** Checkbox in settings to "Enable Autonomous Dunning" for specific value tiers.
- [ ] **Email Integration:** Integration with SMTP/Outlook API to fire the `GenAIAssistant` drafts.
- [ ] **Audit Trail:** Every autonomous email sent is logged as an `AI_ACTION` in the SOC2 Compliance Vault.

---

## 🏗️ Story 6.4: Collective Match Logic (Many-to-One)
**User Persona:** As an AR Analyst, I want the system to match one bank credit to multiple invoices so that I can clear bulk payments in one click.

### 📝 Description
Upgrade the matching engine to handle "Scenario E." If a single bank credit equals the sum of multiple open invoices for the same customer, the engine suggests a "Collective Settlement."

### ✅ Acceptance Criteria
- [ ] **Summation Algorithm:** Engine identifies subsets of open invoices that sum up to the `Bank_Amount`.
- [ ] **UI Workbench:** Displays the list of grouped invoices under the "Suggested Match" panel.
- [ ] **Validation:** Match is rejected if the sum exceeds the bank credit by more than the FX tolerance.



---

## 🚀 Technical Sub-tasks for Developers
1. **OCR Pipeline:** Set up `pytesseract` or an AWS Textract/Azure Document Intelligence wrapper.
2. **Predictive Analytics:** Create `analytics/prediction_engine.py` using `scipy.stats.linregress`.
3. **Logic Hardening:** Refine `backend/engine.py` to support "Many-to-One" array comparisons.
4. **Mock Data:** Update `mock_data_maker.py` to include "Payment History" columns (days past due) to train the predictive engine.
