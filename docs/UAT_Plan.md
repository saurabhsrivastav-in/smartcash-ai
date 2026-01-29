# User Acceptance Testing (UAT) Plan: SmartCash AI

**Project:** SmartCash AI Automation (Sprints 1-12)  
**Version:** 1.0.0-STAGING  
**Lead QA/PM:** Saurabh Srivastav  
**Status:** Open for SME Review  

---

## 1. Introduction
The UAT phase is the final validation gate before the "Atomic Settlement" release. This plan ensures that the **SmartCash AI** platform meets the complex needs of modern Treasury departments, specifically focusing on data integrity, SAP synchronization, and AI explainability.

---

## 2. UAT Scope & Strategy
Testing follows the **"Four-Pillar Execution"** model to mirror the development lifecycle:



1.  **Connectivity & Core Matching:** High-speed bank feed ingestion.
2.  **AI Intelligence:** Accuracy of the LLM and Fuzzy Match algorithms.
3.  **Governance & Analytics:** SOC2 compliance and risk visualizations.
4.  **Autonomous Operations:** Hands-free clearing and Agent-to-Agent communication.

---

## 3. Test Scenarios & Acceptance Criteria

### Pillar 1: Infrastructure & ERP Sync
| ID | Scenario | Acceptance Criteria | Result (P/F) |
| :--- | :--- | :--- | :--- |
| **UAT-1.1** | MT942 Intraday Feed | 4x daily bank files pull correctly without record duplication or "ghost" balances. | |
| **UAT-1.2** | Multi-Currency Aggregation | Dashboard correctly converts GBP/EUR to USD base currency using real-time FX rates. | |
| **UAT-1.3** | SAP BAPI Write-back | Successful matches in the UI trigger an immediate "Cleared" status in SAP FBL5N. | |

### Pillar 2: AI Accuracy & Edge Cases
| ID | Scenario | Acceptance Criteria | Result (P/F) |
| :--- | :--- | :--- | :--- |
| **UAT-2.1** | Messy Remittance OCR | AI extracts Invoice IDs from low-resolution PDF scans with >90% OCR accuracy. | |
| **UAT-2.2** | Weighted Fuzzy Matching | System correctly identifies "Tesla Giga Berlin" as "Tesla Inc" via the Heuristic engine. | |
| **UAT-2.3** | LLM Dispute Drafting | "Generate Email" button produces a professional, error-free draft with correct claim codes. | |



### Pillar 3: Security & Risk Controls
| ID | Scenario | Acceptance Criteria | Result (P/F) |
| :--- | :--- | :--- | :--- |
| **UAT-3.1** | Immutable Audit Trail | Attempting to edit a locked transaction log fails; SHA-256 hash remains consistent. | |
| **UAT-3.2** | ESG Score Enforcement | System blocks "Auto-Post" for any counterparty with an ESG score below 'D'. | |
| **UAT-3.3** | Role-Based Access (RBAC) | Analysts cannot view the "Executive Dashboard" unless granted 'Admin' status. | |

---

## 4. Defect Management Workflow
Every failed test must follow the **Defect Lifecycle** below:



* 🔴 **Critical (Blocker):** Financial data corruption or SAP connection failure.
* 🟡 **Major:** Core functionality (like OCR) failing on more than 20% of samples.
* 🔵 **Minor:** Minor UI alignment issues or non-critical dashboard lag.

---

## 5. Environment & Logistics
* **ERP Sandbox:** SAP S/4HANA Staging Client (Client 300).
* **Bank Data:** Anonymized MT942 production logs from Q4 2025.
* **Documentation:** All test evidence (screenshots/logs) must be attached to the GitHub Issue.

---

## 6. UAT Sign-off Thresholds
For a **"GO"** decision, the following metrics must be satisfied:
1.  **Defect Resolution:** 100% of Critical and Major defects closed.
2.  **Matching Precision:** <0.1% false-positive rate on auto-posted transactions.
3.  **Performance:** Dashboard load time <1.5 seconds for 10 concurrent users.

---

### Final Approval Authorization

| Role | Name | Signature | Decision |
| :--- | :--- | :--- | :--- |
| **Product Owner** | Saurabh Srivastav | ________________ | [ ] GO [ ] NO-GO |
| **Global Treasurer** | ________________ | ________________ | [ ] GO [ ] NO-GO |
| **Compliance Officer** | ________________ | ________________ | [ ] GO [ ] NO-GO |
