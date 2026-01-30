# 📈 Sprint 8 Backlog: Predictive Liquidity Ops & Forecasting

**Sprint Goal:** Deploy the "Predictive Treasury" engine to forecast cash arrival dates and automate liquidity sweep simulations.

---

## 🏗️ Story 8.1: AI-Driven Cash Arrival Forecasting
**User Persona:** As a Treasurer, I want to see the "Expected Value Date" for open invoices based on historical behavior rather than just the due date, so I can plan investments accurately.

### 📝 Description
Upgrade the liquidity projections by replacing static `Due_Date` logic with a machine-learning-based `Predicted_Payment_Date`. The engine must factor in "Payment Personalities" (from Sprint 7) and current macro-economic stressors.

### ✅ Acceptance Criteria
- [ ] **Prediction Engine:** Calculates arrival dates with an 85% confidence interval using `scipy` regression models.
- [ ] **Waterfall Sync:** The "Collections" bar in the Executive Dashboard now offers a toggle between "Scheduled" and "Predicted" cash flow.
- [ ] **Variance Alert:** Highlight invoices where the predicted payment date is >15 days past the legal due date.



---

## 🏗️ Story 8.2: Automated Liquidity Sweep Simulation
**User Persona:** As a Cash Manager, I want to simulate moving excess cash from regional "Header" accounts to a "Central Treasury" account to maximize interest income.

### 📝 Description
Develop a "Sweep Simulator" in the sidebar. Based on the "Available Cash" across five currencies (USD, EUR, GBP, INR, CHF), the system suggests optimal concentration amounts while maintaining a local "Safety Buffer."

### ✅ Acceptance Criteria
- [ ] **Simulation Logic:** Users can set a "Regional Buffer" (e.g., $50,000); the system calculates the surplus available for sweeping.
- [ ] **FX Optimization:** Suggests sweeping the currency with the highest current yield/lowest volatility first.
- [ ] **Audit Trail:** Every simulated sweep action is logged as a "Treasury Strategy" in the SOC2 Vault.

---

## 🏗️ Story 8.3: Macro-Economic Risk Layer (VIX & Interest Rates)
**User Persona:** As a CFO, I want to see how external market volatility impacts our collections risk so I can adjust our credit appetite.

### 📝 Description
Integrate a market data feed (mocked) for interest rates and volatility indices. High market volatility should automatically apply a "Risk Multiplier" to the liquidity haircut slider.

### ✅ Acceptance Criteria
- [ ] **Dynamic Stressing:** If "Market Volatility" is high, the "Liquidity Haircut" defaults to a higher minimum (e.g., 10%).
- [ ] **Correlation View:** A new chart showing the relationship between market rates and the company’s average DSO.

---

## 🏗️ Story 8.4: The "Treasury Command" Executive UI
**User Persona:** As an Executive, I want a single view that summarizes Liquidity, Risk, and AI Performance so I don't have to navigate between tabs during board meetings.

### 📝 Description
Consolidate the most critical metrics into a high-density "Command Center" landing page. This page should utilize advanced Streamlit containers to display the Risk Radar, Waterfall, and DSO Forecast side-by-side.

### ✅ Acceptance Criteria
- [ ] **Layout:** Multi-column layout with real-time "Blinking" alerts for credit breaches or liquidity drops.
- [ ] **Exportable PDF:** Add a "Download Board Report" button that captures the current dashboard state.
- [ ] **Performance:** Ensure the consolidated view loads in < 2.5 seconds using optimized caching.



---

## 🚀 Technical Sub-tasks for Developers
1. **Data Science:** Implement `models/payment_forecaster.py` using `scipy.optimize` for arrival date prediction.
2. **Logic Expansion:** Update `backend/engine.py` to calculate surplus cash across multi-currency nodes.
3. **UI Hardening:** Refactor `main.py` to use `st.container` and `st.columns` for the Command Center layout.
4. **Mock Data Tuning:** Update `mock_data_maker.py` to include interest rate variables and regional bank account headers.
