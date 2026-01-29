# Sprint 2 Backlog: Intelligence & Exception Handling

**Sprint Goal:** Implement AI-driven fuzzy matching, OCR remittance extraction, and the Analyst Workbench for managing short-payments and deductions.

---

## 🏗️ Story 2.1: Multi-Source Remittance Extraction (OCR)
**User Persona:** As an AR Analyst, I want the system to read PDF attachments from the centralized mailbox so that I don't have to manually open and type remittance data.

### 📝 Description
Integrate an OCR engine to process unstructured document layouts. The system must identify and extract: Invoice Number, Gross Amount, and Discount/Deduction values.



### ✅ Acceptance Criteria
- [ ] Successfully extract text from `.pdf`, `.png`, and `.jpg` formats.
- [ ] Map extracted `Invoice_ID` and `Amount` to the transaction record in the staging table.
- [ ] Assign a **Confidence Score (0-100%)** to each extraction.
- [ ] Flag documents with <60% confidence for manual indexing.

---

## 🏗️ Story 2.2: Fuzzy Logic for Customer Identification
**User Persona:** As a Finance Manager, I want the system to identify payers even if the name on the bank file doesn't perfectly match the SAP master data.

### 📝 Description
Implement string-matching algorithms (e.g., Levenshtein Distance) to reconcile variations like "Walmart Inc" vs "Walamrt" or "Target Corp #402".

### ✅ Acceptance Criteria
- [ ] System identifies matches with a name similarity score >85%.
- [ ] System validates the `Amount` as a secondary check before suggesting a fuzzy match.
- [ ] Suggested matches are presented in the UI with a "Confidence Badge" (e.g., "92% Match").

---

## 🏗️ Story 2.3: Analyst Workbench (Exception UI)
**User Persona:** As an AR Analyst, I want a dedicated interface to review suggested matches so that I can approve or reject AI decisions with one click.



### ✅ Acceptance Criteria
- [ ] **Split View:** Show Bank Transaction on the left and Suggested SAP Invoice on the right.
- [ ] **Action Buttons:** "Confirm Match," "Reject," and "Search Manual."
- [ ] **Real-time Update:** Once confirmed, the status in the DB changes from `SUGGESTED` to `READY_TO_POST`.

---

## 🏗️ Story 2.4: Short-Payment & Deduction Coding
**User Persona:** As a Credit Manager, I want to code partial payments with reason codes so that we can track claims and disputes in real-time.

### 📝 Description
When `Bank_Amount < Invoice_Amount`, the system must force the analyst to select a **Reason Code** before the item can be cleared.

### ✅ Acceptance Criteria
- [ ] Display a "Variance" field (Invoice Amount - Bank Amount).
- [ ] Provide a dropdown of SAP-standard Reason Codes (e.g., ZF01 - Damaged, ZF02 - Tax).
- [ ] System calculates "Remaining Balance" and flags it for the **Claim Aging** report.

---

## 🚀 Technical Sub-tasks for Developers
1. **AI Integration:** Install `PyMuPDF` or `EasyOCR` for remittance processing.
2. **Algorithm Design:** Implement the `fuzzywuzzy` or `RapidFuzz` library in the matching service.
3. **Frontend Evolution:** Add a "Review Queue" page to the Streamlit app.
4. **Data Schema Update:** Add `confidence_score` and `reason_code` columns to the `transactions` table.
