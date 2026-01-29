# Sprint 5 Backlog: Strategic Optimization & Global Scaling

**Sprint Goal:** Implement ML-driven self-learning for matching, multi-currency support for global entities, and "One-Click" month-end closing reports.

---

## 🏗️ Story 5.1: ML Feedback Loop (Self-Learning Matching)
**User Persona:** As a Product Manager, I want the system to learn from manual analyst corrections so that the auto-match rate improves over time without manual rule updates.

### 📝 Description
Develop a "Learning Layer" that monitors manual overrides. If an analyst consistently matches "Payer A" to "Entity B" despite low fuzzy scores, the system should create a "Learned Mapping" to automate that match in the future.



### ✅ Acceptance Criteria
- [ ] System stores manual override patterns in a `learned_logic` table.
- [ ] After 3 identical manual matches, the system proposes an "Auto-Rule" for approval.
- [ ] Confidence scores for learned matches increase dynamically over time.

---

## 🏗️ Story 5.2: Multi-Currency & FX Variance Handling
**User Persona:** As a Global AR Lead, I want the system to match payments in different currencies (e.g., EUR payment for a USD invoice) so that we can support international entities.

### 📝 Description
Integrate a real-time Exchange Rate API. The system must calculate the FX variance during the matching process and suggest "Exchange Loss/Gain" posting codes if the variance is within a 2% threshold.

### ✅ Acceptance Criteria
- [ ] Integration with an FX rate provider (e.g., OANDA or XE.com).
- [ ] Automated calculation of `Invoice_Amount_FX` vs `Payment_Amount`.
- [ ] Automated posting of FX differences to the designated GL account.

---

## 🏗️ Story 5.3: "Month-End" Command Center
**User Persona:** As a Financial Controller, I want a high-level summary of all unapplied cash and disputed claims so that I can close the books faster at month-end.

### 📝 Description
A dedicated dashboard view that consolidates all "Blocking Issues." It highlights high-value unapplied cash that must be resolved before the ledger closes.



### ✅ Acceptance Criteria
- [ ] "Closing Readiness" score (0-100%) based on unapplied cash volume.
- [ ] Bulk-action capability to post all remaining minor variances (<$5.00) to a "Write-off" account.
- [ ] One-click generation of the "Account Reconciliation" (Rec) report for auditors.

---

## 🏗️ Story 5.4: Predictive "Payment Behavior" Profiling
**User Persona:** As a Credit Risk Analyst, I want to see a "Payment Personality" for each customer so that I can adjust credit limits based on real-world behavior rather than just credit scores.

### 📝 Description
Analyze historical data to categorize customers as "Early Birds," "Grace-Period Payers," or "Chronic Late Payers."

### ✅ Acceptance Criteria
- [ ] Customer profile page showing "Average Days to Pay" vs "Terms."
- [ ] Trend analysis: Is this customer getting faster or slower at paying?
- [ ] Integration of these profiles into the Sprint 3 Priority Worklist logic.

---

## 🚀 Technical Sub-tasks for Developers
1. **ML Integration:** Set up a Scikit-learn classifier to identify matching patterns.
2. **API Extension:** Add support for ISO currency codes in the backend matching engine.
3. **Data Aggregation:** Create a "Month-End" view in SQL that joins `Transactions`, `Invoices`, and `Deductions`.
4. **Optimization:** Index the `learned_logic` table to ensure the matching engine remains <200ms.
