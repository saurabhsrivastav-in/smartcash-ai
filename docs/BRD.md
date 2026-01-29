# BRD: SmartCash AI Automation

**Project:** SmartCash AI Automation: Order-to-Cash (O2C)  
**Product Area:** Invoice Management & Cash Application Automation  
**Author:** Saurabh Srivastav  
**Date:** January 2026  
**Status:** Final Version for Stakeholder Approval  

---

## 1. Executive Summary
The current Order-to-Cash (O2C) cycle suffers from significant manual bottlenecks in the Invoice Management phase. Despite having SAP and MT942 bank feeds, the reconciliation of remittance details (emails, web data, images) remains manual. This project aims to automate the end-to-end matching of payments to invoices, reducing the 'Unapplied Cash' balance and accelerating the clearing of the General Ledger (GL).

---

## 2. Business Context: The O2C Process
The organization follows a standard 12-step Order-to-Cash process. This automation specifically targets **Step 10 (Invoice Management)** and **Step 11 (Reconciliation)**.

1. Purchase Order
2. Check Inventory
3. Accept Purchase Order
4. Create Sales Invoice
5. Deliver Goods and Services
6. Update Open Account Receivables
7. Billing and Invoicing
8. Payment Initiation (External Merchant Portals/Custom Forms)
9. Payment Receipt
10. **Invoice Management (Target Area)**
11. **Reconciliation (Target Area)**

---

## 3. Current State Analysis

### 3.1 Existing Process Workflow
Currently, the team matches remittance details manually using a centralized mailbox. The process includes:
* **Pre-reminders:** Manual list of invoices due by month-end.
* **Registration:** Manual entry of customer comments into the cash report.
* **Claims Handling:** Manual coordination with commercial teams.
* **Dunning:** Automated but often ignored due to incomplete information.

### 3.2 Current Limitations
* **Response Gaps:** Customers do not always respond to dunning emails (ZF259).
* **Calculation Errors:** Persistent differences between total overdue amounts and actual payments received.
* **Audit Trail Gaps:** No track of the time difference between receiving payment info and SAP entry.
* **Claim Visibility:** No real-time tracking of claim aging or deductions.

---

## 4. Technical Architecture (Current)
The information management is handled by three core technical units:
1. **Treasury IT:** Manages the interface between the Bank and Treasury.
2. **SAP IT Team:** Manages data flow between Treasury/SAP and reporting objects.
3. **Operations Team:** Manages the online reports factory.

### 4.1 Payment Data (MT942)
The system uses **SAP MT942 (SWIFT Message Format)** for interim transaction reports.
* **Frequency:** Treasury sends MT942 files to SAP **4x daily**.
* **Recording:** Transactions are recorded directly into the GL Account in SAP.

---

## 5. Functional Requirements

### 5.1 Data Ingestion & Integration (FR)
| ID | Requirement | Description | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | **MT942 Integration** | Auto-ingest intraday MT942 files 4x daily for real-time balance updates. | High |
| **FR-02** | **Multi-Source Ingestion** | Extract data from PDF images, email bodies, and web data. | High |
| **FR-03** | **Order Linking** | Link original Order data and PO numbers to outstanding AR data. | High |
| **FR-04** | **File Integration** | Merge Cash files and Overdue files to create a single matching source. | Medium |

### 5.2 Matching Scenarios (The Logic Gates)
The system must identify and handle the following four customer confirmation scenarios:
1. **Scenario A:** Confirmation of the amount to be paid.
2. **Scenario B:** Confirmation of the amount NOT to be paid.
3. **Scenario C:** Confirmation of amount with claims/conditions.
4. **Scenario D:** No confirmation received.

### 5.3 Payment Type Handling
The engine must process four distinct payment types:
* **Bulk Payment:** One payment covering multiple invoices.
* **Part Payment:** Partial amount received (requires deduction coding).
* **Full Payment:** 1:1 match between payment and invoice.
* **Advance Payment:** Receipt without a matching invoice (post to account).

---

## 6. AI Worklist & Analytics
* **Prioritized Worklist:** System must auto-generate a list of tasks based on historic data and current urgency.
* **Auto-Deduction Coding:** Suggest codes for claims based on customer history.
* **Time-Gap Tracker:** Monitor the latency between bank credit receipt and GL settlement.

---

## 7. Non-Functional Requirements
* **Performance:** 95% of daily transactions must be matched within 2 hours.
* **Security:** Data must be encrypted; Role-based access (RBAC) required.
* **Scalability:** Must support 10x current volume as the O2C process grows.
* **Compliance:** Adherence to SOX and GDPR.

---

## 8. Product Roadmap

### Phase 1: Foundation (Q1)
* Automate MT942 ingestion.
* Implement exact match logic (Invoice # + Due Date).
* Basic 'Overdue vs. Cash' reporting.

### Phase 2: Intelligence (Q2)
* PDF/Email remittance scraping (OCR/AI).
* Fuzzy matching for customer names.
* Real-time Claim Aging dashboard.

### Phase 3: Total O2C Integration (Q3)
* Integration of Order data to Outstanding data.
* AI-prioritized actions based on historical behavior.
* Automated GL update/clearing upon confirmation.

---

## 9. Success Metrics (KPIs)
* **DSO Reduction:** 3–5 days.
* **Auto-Match Rate:** Target 85%.
* **Manual Effort Reduction:** 60% for the encashment team.
* **Accuracy:** < 0.5% misapplication rate.

---

## 10. Risks & Mitigation
| Risk | Mitigation Strategy |
| :--- | :--- |
| **Non-responsive customers** | Implement AI-driven reminders based on historical response triggers. |
| **Data Mismatches** | Human-in-the-loop review for any match under 90% confidence. |
| **SAP Latency** | Intraday MT942 processing (4x daily) to minimize sync delay. |

---
