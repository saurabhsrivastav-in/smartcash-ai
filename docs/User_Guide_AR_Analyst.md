# 📘 User Guide: SmartCash AI Analyst Workbench
**Version:** 1.0.0 (Production)  
**Target Audience:** Accounts Receivable (AR) Analysts & Treasury Managers  

---

## 1. System Overview
SmartCash AI is an autonomous reconciliation layer that sits between your **Bank (MT942)** and **SAP S/4HANA**. While the system achieves an 85% Straight-Through Processing (STP) rate, your role is to manage "High-Value Exceptions" and refine AI logic.

### Daily Routine
1. **Login:** Access via Enterprise SSO.
2. **Cycle Check:** The system syncs 4x daily (09:00, 12:00, 15:00, 18:00 local time).
3. **Queue Refresh:** Always check the "Total Unapplied Cash" metric before starting.

---

## 2. Navigating the "AI-Prioritized" Worklist
Unlike legacy spreadsheets, your worklist is dynamically ranked by **Urgency and Value**.



### Status Identification
* 🟢 **Auto-Posted (STP):** Completed. No action required. Verified by SHA-256 Audit Hash.
* 🟡 **Suggested Match:** AI confidence is 80%–94%. Requires a "Human-in-the-Loop" (HITL) 1-click verification.
* 🔴 **Critical Exception:** No match found or ESG violation detected. Manual investigation mandatory.

---

## 3. Resolving a "Suggested Match" (Scenario B)
When the AI finds a high-probability match but requires confirmation:

1.  **Open Comparison:** Click the transaction to enter the "Split-Screen View."
2.  **Visual Validation:** Compare the **Payer Name (Bank)** vs. **Customer Name (SAP)**.
3.  **Confidence Metadata:** Hover over the confidence score to see *why* the AI matched them (e.g., "PO Number match in email body").
4.  **Finalize:** Click **[Approve & Post]**. The system executes the SAP BAPI call immediately.



---

## 4. Short-Payments & Deduction Coding (Scenario C)
When a customer pays less than the invoice total, you must "Code the Gap":

1.  **Select Difference:** The AI will highlight the variance in red.
2.  **Reason Coding:** Select the **Standard Reason Code** (e.g., *ZF10 - Freight*, *ZF22 - Early Pay Discount*).
3.  **Documentation:** Drag the customer's PDF debit memo into the **Evidence Box**.
4.  **Post:** Clicking **[Post with Residual]** clears the original invoice and creates a new sub-ledger item for the dispute.

---

## 5. The GenAI Dispute Assistant
For "Scenario D" (No Info) payments, do not write manual emails.

1.  **Trigger Assistant:** Click the **[🤖 Draft Inquiry]** icon.
2.  **Contextual Awareness:** The AI automatically pulls the Bank Reference ID and Payer Name into a professional template.
3.  **Review & Send:** Edit if necessary and click **[Send via Outlook]**.
4.  **Auto-Follow-up:** The system places a 48-hour "Wait" tag on the transaction; if no reply is received, it escalates to the Credit Manager.



---

## 6. Power-User Shortcuts & Filtering
* **Global Search:** Use `Ctrl + K` to jump to any Invoice ID or Bank TXN.
* **Filter by ESG:** Use the sidebar to filter for "High Risk" (Score D/E) counterparties to perform enhanced due diligence.
* **Bulk Clearing:** Hold `Shift` to select multiple Yellow badges for batch approval (only recommended for 90%+ confidence).

---

## 7. Troubleshooting FAQ
| Issue | Solution |
| :--- | :--- |
| **Payment not showing?** | Verify the MT942 file timestamp in the "System Health" sidebar. |
| **"Object Locked" Error?** | The invoice is likely open in an SAP GUI session (User Edit Mode). Close SAP and retry. |
| **Wrong AI Match?** | Click **[Reject Match]**. This feedback trains the model to avoid this error in the next cycle. |

**Support:** Raise a priority ticket in Jira under the `TREASURY-AI` queue or email `it.support@company.com`.
