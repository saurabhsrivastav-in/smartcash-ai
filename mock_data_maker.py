import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_data():
    # 1. Setup metadata
    customers = [
        ('Tesla Inc', 'AA'), ('Global Blue SE', 'A'), ('Tech Retail Corp', 'B'),
        ('Saurabh Soft', 'AA'), ('Eco Energy', 'A'), ('Nordic Logistics', 'B'),
        ('Swiss Finance', 'AA'), ('Pacific Rim', 'C'), ('Horizon Ventures', 'A')
    ]
    currencies = ['USD', 'EUR', 'GBP', 'INR', 'CHF']
    
    # 2. Generate Invoices (200 rows)
    invoice_data = []
    for i in range(1, 201):
        cust, esg = customers[np.random.randint(0, len(customers))]
        curr = currencies[np.random.randint(0, len(currencies))]
        amount = np.random.uniform(5000, 150000)
        due_date = datetime.now() + timedelta(days=np.random.randint(-30, 60))
        status = 'Paid' if np.random.random() > 0.4 else 'Open'
        
        invoice_data.append([
            f"INV-{1000+i}", cust, round(amount, 2), curr, 
            due_date.strftime('%Y-%m-%d'), status, esg
        ])
        
    inv_df = pd.DataFrame(invoice_data, columns=[
        'Invoice_ID', 'Customer', 'Amount', 'Currency', 'Due_Date', 'Status', 'ESG_Score'
    ])

    # 3. Generate Bank Feed (Matching ~70% of Open Invoices)
    bank_data = []
    open_invoices = inv_df[inv_df['Status'] == 'Open'].head(20)
    
    for idx, row in open_invoices.iterrows():
        # Add some "noise" to names to test the Fuzzy Matching engine
        noise_name = row['Customer'] + (" Ltd" if np.random.random() > 0.5 else " Group")
        bank_data.append([
            f"TXN-{5000+idx}", row['Amount'], row['Currency'], 
            noise_name, datetime.now().strftime('%Y-%m-%d')
        ])

    bank_df = pd.DataFrame(bank_data, columns=[
        'Bank_TX_ID', 'Amount_Received', 'Currency', 'Payer_Name', 'Date'
    ])

    # 4. Save to 'data' folder
    if not os.path.exists('data'):
        os.makedirs('data')
        
    inv_df.to_csv('data/invoices.csv', index=False)
    bank_df.to_csv('data/bank_feed.csv', index=False)
    print("✅ Mock data generated successfully in /data folder!")

if __name__ == "__main__":
    generate_mock_data()
