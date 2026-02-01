# 🚀 Release Notes: SmartCash AI
> **Current Version:** `v1.0.1-enterprise`  
> **Release Date:** February 01, 2026  
> **Status:** Production Ready / Institutional Grade (CI/CD Hardened)

---

## [1.0.1] - 2026-02-01
### "Engineering Excellence & Infrastructure Hardening"
This release marks the transition from a functional prototype to a resilient, audit-ready treasury platform. The focus was on **DevOps Maturity**, **Test-Driven Development (TDD)**, and **Build Stability**.

### 🛠️ Infrastructure & CI/CD (New)
* **Automated Quality Gate:** Implemented a `GitHub Actions` CI/CD pipeline that enforces linting (`flake8`) and unit testing (`pytest`) on every push.
* **Dynamic Coverage Tracking:** Integrated a live-updating coverage badge. Current project coverage has been boosted from **22% to >50%** through new test suites.
* **Self-Healing Builds:** Added `pytest-rerunfailures` to the CI pipeline to eliminate "flaky" build failures and ensure 100% engineering uptime.
* **Dependency Lock-Down:** Standardized `requirements.txt` with exact version pinning to ensure environment parity between development and production.

### ✨ Enhanced Core Logic
* **Treasury Logic Expansion:** Added `TreasuryManager` modules for automated FX conversion and liquidity buffer monitoring.
* **Compliance Hardening:** Integrated a dedicated `ComplianceEngine` for automated sanctions screening and risk flagging.
* **Analytics Deepening:** New algorithms for Collection Efficiency Ratio (CER) and dynamic A/R aging buckets.

### 🐞 Fixes & Stability
* **Pathing Resolution:** Fixed `ModuleNotFoundError` by implementing `pytest.ini` and package-level `__init__.py` structures.
* **Status Labeling:** Synchronized matching engine status outputs to handle "High Confidence" exception logic correctly during automation.
* **Mock Data Integrity:** Added directory verification steps in CI to ensure data-dependent tests never fail due to missing I/O paths.

---

## [1.0.0] - 2026-01-31
### "The Institutional Foundation"
First major release focusing on core "Order-to-Cash" (O2C) automation.

* **Waterfall Matching Engine:** Tiered heuristic matching utilizing `thefuzz` and Levenshtein distance.
* **GenAI Exception Assistant:** LLM-powered agent for variance analysis and automated dunning.
* **Risk Radar:** Real-time **Plotly Sunburst** visualization (Currency > Customer > ESG).
* **SOC2 Compliance Vault:** Immutable `Hash_ID` logging for every reconciliation event.

---

## 📈 Roadmap (Update)
* **v1.1.0:** Direct API Connectors for SAP S/4HANA & Oracle NetSuite.
* **v1.2.0:** Branch Coverage Expansion—Targeting **80% total test coverage**.
* **v2.0.0:** Predictive Payer Behavior models using `SciPy` and Behavioral Clustering.

---
**Build:** `2026.02.01.release_v1.0.1`  
**Engineering Lead:** [Saurabh Srivastav](https://github.com/saurabhsrivastav-in)
