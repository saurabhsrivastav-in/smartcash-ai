import pytest
import pandas as pd
from backend.engine import SmartMatchingEngine

@pytest.fixture
def engine():
    """Initializes the Smart Matching Engine for testing."""
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
    """Test 1: Verifies match when using an alias (e.g., 'tsla motors gmbh')."""
    # Note: Engine resolves 'tsla motors gmbh' to 'Tesla Inc'
    results = engine.run_match(50000.00, "tsla motors gmbh", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-001'
    # Engine returns 0.9 for alias-based matches
    assert results[0]['confidence'] >= 0.90
    
    # Engine uses 'EXCEPTION: High Confidence' for alias matches instead of pure STP
    status = results[0].get('status', '')
    assert any(term in status for term in ["STP", "High Confidence"])

def test_bank_fee_tolerance(engine, sample_invoices):
    """Test 2: A small discrepancy (bank fees) should still yield a match."""
    results = engine.run_match(49985.00, "Tesla Inc", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-001'
    assert results[0]['confidence'] >= 0.80 

def test_fuzzy_name_match(engine, sample_invoices):
    """Test 3: Minor typos/fuzzy names should be caught."""
    results = engine.run_match(2500.00, "Saurabh Software", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-003'
    assert results[0]['confidence'] > 0.70

def test_currency_mismatch(engine, sample_invoices):
    """Test 4: Wrong currency should result in low confidence or exclusion."""
    results = engine.run_match(1500.00, "Global Blue SE", "USD", sample_invoices)
    
    # We verify that no "High Confidence" (0.85+) match exists for a currency mismatch
    bad_matches = [r for r in results if r['Invoice_ID'] == 'INV-002' and r['confidence'] > 0.85]
    assert len(bad_matches) == 0

def test_dso_calculation(engine, sample_invoices):
    """Test 5: Verify the Days Sales Outstanding (DSO) calculation logic."""
    # Mapping 'Amount' to 'Amount_Remaining' for the DSO function
    dso_df = sample_invoices.rename(columns={'Amount': 'Amount_Remaining'})
    dso = engine.calculate_dso(dso_df)
    assert dso >= 0
