# 🚀 Go-Live Checklist: SmartCash AI Deployment

**Project:** SmartCash AI Automation: Next-Gen Treasury Cutover  
**Release Version:** v1.0.0-PROD (Enterprise Build)  
**Deployment Date:** January 2026  
**Owner:** Saurabh Srivastav, Product Manager  

---

## 1. Pre-Deployment (T-minus 72 Hours)
*Foundational stability and data integrity checks.*

- [ ] **Data Sanitization:** Purge all "Test/Dummy" rows from `data/invoices.csv` and `data/bank_feed.csv`.
- [ ] **Infrastructure Freeze:** GitHub `main` branch locked; no further commits allowed without emergency CAB approval.
- [ ] **Environment Secret Audit:** Confirm `.env` variables (SAP BAPI credentials, OpenAI API keys) are moved to the Secure Secret Manager.
- [ ] **Backup Verification:** Execute a full snapshot of existing SAP AR tables (BSIK/BSID) and the Python local database.

---

## 2. Technical Cutover (T-minus 24 Hours)
*Establishing the plumbing between the bank and the engine.*



- [ ] **MT942 SFTP Handshake:** Verify Treasury IT can pull the 4x daily SWIFT files without authentication latency.
- [ ] **SSL/TLS & PQC:** Confirm the `https` certificate is active; verify Post-Quantum Cryptography (PQC) encryption for vendor data.
- [ ] **Docker / Cloud Scale:** Confirm the container orchestration (Kubernetes/ECS) is set to 3x redundancy for the launch window.
- [ ] **Persistence Layer:** Verify the "SOC2 Compliance Vault" has write-permissions for the production logs.

---

## 3. Production Launch (Day 0: Go-Live)
*The critical path for the launch window.*

### Phase A: Data Ingestion (09:00 AM)
- [ ] **MT942 Pulse:** Trigger the first intraday bank file ingestion (Scenario: Morning Credit Sweep).
- [ ] **Remittance Listener:** Activate the Python `imap` listener for the Centralized Remittance Mailbox.
- [ ] **Inflow Sync:** Pull the 1,000+ most recent open items from SAP into the `SmartMatchingEngine`.

### Phase B: Processing & Matching (11:00 AM)
- [ ] **STP Benchmark:** Monitor the first 100 transactions; target >90% Straight-Through Processing accuracy.
- [ ] **Fuzzy Logic Validation:** Review "TheFuzz" scores on the first 10 matches to ensure no false positives.
- [ ] **BAPI Write-back:** (CRITICAL) Enable the SAP connector to post the first batch of auto-matches to the GL.

---

## 4. Organizational Readiness
*Ensuring the team can drive the new system.*



- [ ] **Analyst Certification:** Confirm all 15 AR Analysts have passed the "Workbench Exception Handling" simulation.
- [ ] **Support Escalation:** Distribute the "SmartCash Troubleshooting Matrix" to the Tier-1 Helpdesk.
- [ ] **Customer Communication:** Deploy the registration emails to the Top 50 Strategic Partners for the new Vendor Portal.

---

## 5. Post-Launch Monitoring (T-plus 48 Hours)
*Hyper-care and performance auditing.*

- [ ] **SteerCo Reporting:** Hourly automated summaries of "Auto-Matched vs. Manual Exceptions" sent via Slack/Email.
- [ ] **Latency Audit:** Ensure the Executive Dashboard (Plotly/Streamlit) loads in <1.5s under concurrent user load.
- [ ] **Audit Integrity:** Verify the Hashed Audit Ledger is immutable and recording all "Scenario D" exceptions.

---

## 6. Contingency / Rollback Plan
*Emergency protocols for unexpected system failure.*

| Trigger Event | Action | Responsibility |
| :--- | :--- | :--- |
| **BAPI Posting Error** | Kill SAP Write-back; switch to "Offline Reconciliation" mode. | SAP IT Lead |
| **OCR Failure > 20%** | Revert to manual attachment viewing; disable auto-scrape. | AI Team Lead |
| **Data Mismatch** | Full System Pause; Rollback to T-minus 24h Backup. | DevOps Lead |

---

### Final Go/No-Go Approval

| Authority | Decision | Signature | Time |
| :--- | :--- | :--- | :--- |
| **Saurabh Srivastav (PM)** | [ ] GO [ ] NO-GO | ________________ | ________ |
| **Technical Architect** | [ ] GO [ ] NO-GO | ________________ | ________ |
| **Head of Treasury Ops** | [ ] GO [ ] NO-GO | ________________ | ________ |
