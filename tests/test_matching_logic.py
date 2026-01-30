import pytest
import pandas as pd
from backend.engine import SmartMatchingEngine

@pytest.fixture
def engine():
    return SmartMatchingEngine()

@pytest.fixture
def sample_invoices():
    """Creates a controlled dataset for testing match accuracy."""
    return pd.DataFrame({
        'Invoice_ID': ['INV-001', 'INV-002', 'INV-003'],
        'Customer_Name': ['Tesla Inc', 'Global Blue SE', 'Saurabh Soft'],
        'Amount': [50000.00, 1500.00, 2500.00],
        'Currency': ['USD', 'EUR', 'USD'],
        'Status': ['Open', 'Open', 'Open'],
        'ESG_Score': ['AA', 'A', 'B']
    })

def test_exact_match(engine, sample_invoices):
    """Test 1: Exact Amount, Currency, and Resolved Alias should yield >95% confidence."""
    # Using an alias defined in engine.py: "tsla motors gmbh" -> "Tesla Inc"
    results = engine.run_match(50000.00, "tsla motors gmbh", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-001'
    assert results[0]['confidence'] >= 0.95
    assert "STP: Automated" in results[0]['status']

def test_bank_fee_tolerance(engine, sample_invoices):
    """Test 2: A $15 discrepancy should still yield a high-confidence match (80%)."""
    # $50,000 invoice, but only $49,985 received
    results = engine.run_match(49985.00, "Tesla Inc", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-001'
    # Confidence should be around 0.82 (amt_score 0.8 + name_score 1.0 weighted)
    assert results[0]['confidence'] >= 0.80 
    assert "EXCEPTION" in results[0]['status']

def test_fuzzy_name_match(engine, sample_invoices):
    """Test 3: Minor typos in names should be caught by Fuzzy Logic."""
    # "Saurabh Software" vs "Saurabh Soft"
    results = engine.run_match(2500.00, "Saurabh Software", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-003'
    assert results[0]['confidence'] > 0.70

def test_currency_mismatch(engine, sample_invoices):
    """Test 4: Correct amount but wrong currency should result in low confidence."""
    # Amount matches INV-002 (1500), but currency is USD instead of EUR
    results = engine.run_match(1500.00, "Global Blue SE", "USD", sample_invoices)
    
    # name_score (0.4) + amt_score (0.0) = 0.4 total
    # The engine filters out anything <= 0.40
    assert len([r for r in results if r['Invoice_ID'] == 'INV-002' and r['confidence'] > 0.5]) == 0

def test_dso_calculation(engine, sample_invoices):
    """Test 5: Verify the DSO math."""
    dso = engine.calculate_dso(sample_invoices)
    # Total AR = 54000. Total Sales = 54000. DSO = (1/1)*365 = 365.
    assert dso == 365.0
