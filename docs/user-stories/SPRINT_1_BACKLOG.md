# Sprint 1 Backlog: Foundation & Exact Match Engine

**Sprint Goal:** Establish the automated pipeline for MT942 bank files and achieve auto-posting for 1:1 "Perfect Matches" between Bank and SAP data.

---

## 🏗️ Story 1.1: MT942 Bank File Ingestion
**User Persona:** As a Treasury IT Analyst, I want the system to automatically ingest and parse MT942 files 4x daily so that intraday cash visibility is real-time.

### 📝 Description
The system must connect to the Treasury SFTP folder, identify new SWIFT MT942 files, and extract transaction data into the SmartCash database.

### ✅ Acceptance Criteria
- [ ] System successfully parses **Tag 61** (Transaction amount, date, and DC indicator).
- [ ] System successfully parses **Tag 86** (Unstructured remittance/reference info).
- [ ] System handles "Intraday" logic (updates 4x daily: 09:00, 12:00, 15:00, 18:00).
- [ ] Logic prevents duplicate entry of the same Bank Reference ID.

---

## 🏗️ Story 1.2: SAP Open Items Synchronization
**User Persona:** As an AR Analyst, I want the system to sync with the SAP Open Item list (BSID/BSAD) so that I am matching against the most current outstanding invoices.

### 📝 Description
Establish a read-only API connection to SAP to pull all "Open" status invoices including Invoice ID, Customer Name, Due Date, and Net Amount.



### ✅ Acceptance Criteria
- [ ] Successful data pull of all invoices with status "Open."
- [ ] Field mapping is accurate (SAP `VBELN` to `Invoice_ID`, `WRBTR` to `Amount`).
- [ ] Data refresh completes in < 5 minutes for a dataset of 10,000 records.

---

## 🏗️ Story 1.3: Level 1 "Exact Match" Logic
**User Persona:** As a Finance Manager, I want the system to auto-clear payments that perfectly match an invoice so the team can focus solely on exceptions.

### 📝 Description
Develop the core matching algorithm for **Scenario A** (Full Payment). If the bank reference matches the Invoice ID and the amounts are identical, the system marks the item as "Ready to Post."



### ✅ Acceptance Criteria
- [ ] **Logic Gate:** Match triggered ONLY if `Bank_Amount == Invoice_Amount` AND `Bank_Ref == Invoice_ID`.
- [ ] **Status Update:** Matched records must be flagged as `STATUS_AUTO_POST`.
- [ ] **Audit Trail:** Every match must log the `Match_Timestamp` and `Match_Type: Exact`.

---

## 🏗️ Story 1.4: Foundation Dashboard UI
**User Persona:** As an AR Analyst, I want a basic dashboard to see the total "Unapplied Cash" so I can track the day's remaining workload.

### 📝 Description
Create a Streamlit-based interface that displays the summary of ingested MT942 transactions and their current status (Matched vs. Unmatched).

### ✅ Acceptance Criteria
- [ ] Display Total Value of "Unapplied Cash" in a header metric.
- [ ] Table view showing: Payer Name, Amount, Reference, and Status (Green/Red).
- [ ] Filter functionality to view only "Unmatched" items.

---

## 🚀 Technical Sub-tasks for Developers
1. **Database Schema:** Create `transactions` and `invoices` tables in PostgreSQL.
2. **API Layer:** Set up FastAPI endpoints for `/ingest/mt942` and `/match/run`.
3. **Environment:** Configure `.env` files for SAP and Bank SFTP credentials.
