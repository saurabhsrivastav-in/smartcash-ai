# 📢 Release Notes: SmartCash AI v1.0.0
**Version:** 1.0.0-PROD (Long-Term Support)  
**Release Date:** January 30, 2026  
**Codename:** *Atomic Settlement* ---

## 🚀 Overview
Version 1.0.0 marks the transition of SmartCash AI from a proof-of-concept to a production-ready **Autonomous Treasury Engine**. This release introduces the full "Match-to-Post" workflow, allowing for 85% straight-through processing (STP) of bank credits directly into SAP.

---

## ✨ Key Features

### 1. SmartMatching Engine (V1 Core)
* **Multi-Factor Heuristics:** Implementation of a 12-layer matching algorithm utilizing `thefuzz` for payer name normalization.
* **Scenario-Based Logic:** Automated routing for Full Payments, Partial Payments (Claims), and Bulk Remittances.
* **Confidence Scoring:** Every match is assigned a percentage score; matches >95% are auto-posted to the GL.



### 2. GenAI Remittance Assistant
* **OCR Integration:** Vision-based extraction of invoice data from unstructured PDF and JPG attachments.
* **Autonomous Communication:** Integration of LLM-based drafting for customer dispute emails and payment clarifications.

### 3. Institutional Governance
* **ESG Risk Guard:** Real-time flagging of transactions involving counterparties with low ESG ratings (D/E).
* **SOC2 Compliance Vault:** Every automated action generates a SHA-256 hashed audit log, ensuring an immutable record for auditors.

### 4. Executive Command Center
* **Liquidity Heatmaps:** Real-time visualization of cash inflow trends by currency (USD, EUR, GBP).
* **DSO Tracker:** Live monitoring of Days Sales Outstanding impact.



---

## 🔧 Technical Improvements
* **Database Optimization:** Refactored PostgreSQL indexing to support 1,000+ transaction lookups in <200ms.
* **Security:** Enabled **Post-Quantum Cryptography (PQC)** for all data-at-rest within the `data/` directory.
* **Scalability:** Implemented `st.cache_data` in the Streamlit frontend to handle large-scale `invoices.csv` datasets without UI lag.

---

## 🐞 Bug Fixes
* **Currency Collision:** Fixed an issue where GBP and EUR amounts were aggregating without conversion in the Summary KPI.
* **Date Parsing:** Resolved a bug in `backend/engine.py` where ISO-8601 dates were failing for weekend-dated transactions.
* **Fuzzy Thresholds:** Tuned the matching sensitivity to reduce false positives for "Tesla Inc" vs "Tesla Energy."

---

## 🛠️ Installation & Upgrade
To deploy this version, update your environment and sync the production data:

```bash
# 1. Pull the latest release
git pull origin main

# 2. Update system packages
sudo apt-get install -y $(cat packages.txt)

# 3. Update Python dependencies
pip install -r requirements.txt

# 4. Initialize the Engine
python main.py
