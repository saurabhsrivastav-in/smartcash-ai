# 🧪 User Acceptance Testing (UAT) Plan: SmartCash AI
> **Project:** SmartCash AI - Treasury Automation Engine  
> **Environment:** UAT / Staging  
> **Testing Lead:** Saurabh Srivastav  
> **Primary Tester:** AR/Treasury Analyst (Persona)

---

## 1. Introduction & Scope
The purpose of this UAT is to verify that **SmartCash AI** meets the business requirements defined in the BRD, specifically focusing on the accuracy of the matching engine and the usability of the Risk Radar dashboard.

**Acceptance Criteria:** * 100% of P0 requirements (Matching & Audit) must pass.
* No "High" or "Critical" bugs in the reconciliation flow.

---

## 2. Test Environment & Prerequisites
* **URL:** [UAT Link / Localhost:8501]
* **Test Data:** `data/UAT_Invoices_Jan26.csv` (Synthetic but realistic institutional data).
* **Tools:** Access to the Streamlit UI and the `Audit_Ledger` hash results.

---

## 3. Test Scenarios (The Confirmation Gates)

### 3.1 Scenario 1: Straight-Through Processing (STP)
* **Objective:** Verify Level 1 (Exact) matching logic.
* **Input:** Bank feed entry exactly matching Invoice ID and Amount.
* **Expected Result:** Status displays "AUTO-CLEARED"; Entry recorded in SOC2 Vault.
* **Pass/Fail:** [ ]

### 3.2 Scenario 2: Fuzzy Logic Accuracy
* **Objective:** Verify Level 2 (Heuristic) matching.
* **Input:** Bank feed with customer name "Saurabh Srivastav INC" vs. Invoice name "Saurabh Srivastav."
* **Expected Result:** System provides a "Suggestion" with a confidence score >90%.
* **Pass/Fail:** [ ]

### 3.3 Scenario 3: GenAI Correspondence
* **Objective:** Verify the Exception Management workflow.
* **Input:** A "Red" scenario (No match found).
* **Expected Result:** `GenAIAssistant` drafts a context-aware email including the Payer's name and the specific variance.
* **Pass/Fail:** [ ]

### 3.4 Scenario 4: Treasury Stress Simulator
* **Objective:** Verify the mathematical precision of liquidity modeling.
* **Input:** Move "Collection Latency" slider to 15 days.
* **Expected Result:** Cash flow waterfall updates dynamically using `NumPy` logic without lag.
* **Pass/Fail:** [ ]



---

## 4. Test Schedule & Roles

| Phase | Activity | Responsible |
| :--- | :--- | :--- |
| **Phase 1** | Sanity Check & Data Load | Saurabh Srivastav |
| **Phase 2** | Functional Testing (Scenarios 1-4) | Treasury Analyst |
| **Phase 3** | Compliance & Audit Log Verification | Compliance Officer |
| **Phase 4** | Final Sign-off | Treasury Lead |

---

## 5. Defect Logging
Any issues found during UAT must be logged in the **GitHub Issues** tab using the following template:
* **Severity:** (Critical / Major / Minor)
* **Step to Reproduce:** (1, 2, 3...)
* **Expected vs. Actual:** [Describe the gap]

---

## 6. UAT Approval Sign-off
**I, the undersigned, have reviewed the results of this UAT and confirm that SmartCash AI is ready for Production deployment.**

**Signature:** ____________________  **Date:** __________  
**Title:** ________________________

---
**Build ID:** `2026.01.31.UAT`
