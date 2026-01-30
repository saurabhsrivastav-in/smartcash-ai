# 🧪 User Acceptance Testing (UAT) Plan: SmartCash AI

**Project:** SmartCash AI - Institutional Treasury Automation  
**Version:** 1.0.0 (Pre-Production Validation)  
**Lead QA/UAT Lead:** Saurabh Srivastav  
**Stakeholders:** Treasury Operations, AR Analysts, Compliance/Audit  

---

## 1. UAT Objective
The goal of this UAT is to ensure that the **SmartCash AI** platform accurately identifies payment matches, handles financial exceptions via AI, and maintains a perfect, non-repudiable audit trail before moving to a live production environment.



---

## 2. Test Environment & Prerequisites
* **Platform:** Streamlit Local Python 3.11+ Environment.
* **Test Data:** Generated via `mock_data_maker.py` (200+ invoices across global currencies).
* **Compliance Layer:** `backend/compliance.py` must be initialized with a local `compliance_log.csv`.
* **Dependencies:** All libraries in `requirements.txt` (including `thefuzz` and `cryptography`) must be installed.

---

## 3. UAT Scope & Test Scenarios

### 3.1 Scenario 1: Executive Dashboard & Macro Stress
**Goal:** Validate that the "Liquidity Haircut" logic correctly impacts the waterfall chart.
* **Action:** Adjust the "Collection Latency" slider in the sidebar.
* **Expected Result:** * "Adjusted DSO" metric increases in real-time.
    * "Liquidity Bridge" waterfall chart updates to show a reduction in "Collections (Stressed)."

### 3.2 Scenario 2: Smart Matching (Exact & Fuzzy)
**Goal:** Test the engine's ability to handle "dirty" bank data via Sprints 1 & 2.
* **Action:** Select a transaction where the payer name is "TSLA Motors" vs "Tesla Inc".
* **Expected Result:** * System returns a "Fuzzy Match" with a confidence score based on `token_set_ratio`.
    * If score > 95%, system flags as "STP: Automated."

### 3.3 Scenario 3: Tamper-Proof Audit Logging (Sprint 9)
**Goal:** Verify the SHA-256 "Non-Repudiation" requirement.
* **Action:** Perform a match, then manually edit the `Amount` field in `data/compliance_log.csv`.
* **Expected Result:** * Re-calculating the hash of the modified row must result in a mismatch against the stored `Hash_ID`.
    * The system signals "Data Integrity Breach" (if verification logic is run).



---

## 4. Acceptance Criteria (Go/No-Go)
| ID | Criteria | Required Result |
| :--- | :--- | :--- |
| **AC-01** | **Matching Accuracy** | > 98% accuracy on Level 1 (Exact) matches. |
| **AC-02** | **System Latency** | UI updates and matching calculations occur in < 1.0 seconds. |
| **AC-03** | **Audit Trail** | 100% of "Approve" actions must generate a 64-character SHA-256 hash. |
| **AC-04** | **ESG Risk Visibility** | Risk Radar Sunburst must correctly segment by ESG Rating (AA to C). |

---

## 5. Defect Severity Matrix
* **S1 (Critical):** Application crash or incorrect cash balance/DSO calculation.
* **S2 (High):** Fuzzy matching logic failing on >85% similarity matches.
* **S3 (Medium):** UI misalignment or formatting errors in the Risk Radar.
* **S4 (Low):** Minor typos in the AI-generated dunning email templates.

---

## 6. Sign-Off Panel
* **Business Lead (Treasury):** ____________________ Date: __________
* **Technical Lead (AI/Eng):** ____________________ Date: __________
* **Audit/Compliance:** ____________________ Date: __________
