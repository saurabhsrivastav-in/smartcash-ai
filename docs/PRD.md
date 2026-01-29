# 🏦 Product Requirement Document (PRD): SmartCash AI

**Author:** Saurabh Srivastav  
**Version:** 1.0 (Production-Ready)  
**Status:** In-Development / Live Demo  
**Live Application:** [View SmartCash AI Dashboard](https://smartcash-ai-ezywbepvihp9bnvqgndwrb.streamlit.app/)

---

## 1. Executive Summary & Vision
**SmartCash AI** is an autonomous Order-to-Cash (O2C) orchestration layer designed to eliminate "The Remittance Gap." By leveraging Fuzzy Logic, GenAI, and Blockchain-verified audit trails, the system transforms manual bank reconciliation into an **Exception-Only** management workflow.

**Vision:** To achieve a **95% Straight-Through Processing (STP)** rate, reducing DSO and freeing finance teams from repetitive data entry.

---

## 2. Problem Statement
Manual cash application in SAP ERP environments is plagued by:
* **Dirty Data:** Bank remittance info (Tag 86) rarely matches SAP Invoice IDs exactly.
* **Volume Peaks:** Month-end transaction surges lead to delayed revenue recognition.
* **Unapplied Cash:** Millions in "lost" liquidity due to unidentified payments.



---

## 3. User Personas

| Persona | Pain Point | Success Metric |
| :--- | :--- | :--- |
| **AR Analyst** | Spending 4+ hours/day on manual Excel lookups. | Payments processed per hour. |
| **CFO** | High DSO and lack of real-time cash visibility. | DSO Reduction (Days). |
| **Treasury IT** | Complex integration between SWIFT and SAP. | System Uptime & API Latency. |

---

## 4. Functional Specifications

### 4.1 Data Pipeline & Ingestion (FR1)
The system acts as a real-time aggregator for global financial feeds.

* **MT942 Parser:** Autonomous ingestion of SWIFT Intraday reports, parsing Tag 61 (Value Dates) and Tag 86 (Unstructured Text).
* **Multi-Channel OCR:** Layout-aware AI to extract metadata from PDF/Email remittance advices.
* **SAP Linkage:** Bidirectional integration with SAP (Tables BSID/BSAD) to maintain a live "Matching Pool."

### 4.2 The "Waterfall" Matching Engine (FR2 & FR3)
Logic cascades through four gates to ensure maximum automation with zero risk.

1.  **Level 1 (Exact):** `Bank_Amt == Inv_Amt` AND `Ref == Inv_ID`. **(Action: Auto-Post)**
2.  **Level 2 (Fuzzy):** Customer Name similarity > 90% via Levenshtein distance. **(Action: Suggested)**
3.  **Level 3 (Collective):** Sum of multiple Open Invoices matches one Bank Credit. **(Action: Suggested)**
4.  **Level 4 (Short-Pay):** Valid match found with partial payment. **(Action: Trigger Dispute Agent)**



### 4.3 GenAI & Dispute Management (FR4)
When Level 4 logic is triggered, the **GenAI Agent** (GPT-4/Gemini) performs:
* **Contextual Analysis:** Determines if the variance is a bank fee, tax, or dispute.
* **Autonomous Correspondence:** Drafts a personalized email to the customer's AP department requesting remittance details.

---

## 5. Non-Functional Requirements (NFRs)

* **Auditability (FR5):** Every transaction must generate a SHA-256 hash, creating an immutable audit trail for external auditors.
* **Security:** AES-256 encryption for data at rest; PQC-ready (Post-Quantum Cryptography) logic for data in transit.
* **Scalability:** Horizontal scaling to process **50,000 items/hour**.
* **Performance:** UI interactions must maintain a latency of **<1.5s**.

---

## 6. Success Metrics (KPIs)

| Metric | Baseline | Target (Q4 2026) |
| :--- | :--- | :--- |
| **STP Rate** | 40% (Manual) | **85% - 95%** |
| **DSO Reduction** | 35 Days | **-5 Days** |
| **Analyst Capacity** | 50 Postings/Day | **250+ Postings/Day** |

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Sprint 1-4)
* Connectivity: MT942 Parsing & SAP Read-only API.
* Core: Level 1 & 2 Waterfall logic.

### Phase 2: Intelligence (Sprint 5-8)
* AI Agent: GenAI Email drafting and Deduction coding.
* UI: Analyst Workbench & Executive Dashboard.

### Phase 3: Autonomous Scale (Sprint 9-12)
* Compliance: Blockchain Audit Logs.
* Treasury: CBDC Atomic Settlement and Liquidity Sweeps.

---

## 8. Exception Handling & Edge Cases
* **Currency Variance:** Midday FX rate pull for cross-currency matching.
* **Overpayments:** Trigger "Unapplied Credit" workflow in SAP.
* **Duplicate Detection:** Hash-checking Bank Transaction IDs to prevent double-posting.

---
