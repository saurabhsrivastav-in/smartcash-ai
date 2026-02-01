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

def test_exact_alias_resolution(engine, sample_invoices):
    """
    Test 1: Verifies match when using an alias (e.g., 'tsla motors gmbh').
    Ensures the 'Waterfall' logic correctly maps aliases to parent entities.
    """
    results = engine.run_match(50000.00, "tsla motors gmbh", "USD", sample_invoices)
    
    assert len(results) > 0, "Engine failed to return any matches for a known alias."
    top_match = results[0]
    assert top_match['Invoice_ID'] == 'INV-001'
    assert top_match['confidence'] >= 0.90
    
    # Check for professional status strings
    status = top_match.get('status', '')
    assert any(term in status for term in ["STP", "High Confidence", "EXCEPTION"]), \
        f"Unexpected status string: {status}"

def test_bank_fee_tolerance_window(engine, sample_invoices):
    """
    Test 2: A small discrepancy (bank fees/short-pays) should still yield a match.
    Validates the 'Fuzzy Amount' logic (typically ±$25 or 1%).
    """
    # $15 difference on a $50k invoice
    results = engine.run_match(49985.00, "Tesla Inc", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-001'
    assert results[0]['confidence'] >= 0.80 

def test_fuzzy_string_similarity(engine, sample_invoices):
    """
    Test 3: Minor typos/fuzzy names should be caught by Levenshtein distance logic.
    """
    results = engine.run_match(2500.00, "Saurabh Software Solutions", "USD", sample_invoices)
    
    assert len(results) > 0
    assert results[0]['Invoice_ID'] == 'INV-003'
    # Thefuzz should yield a high score even with the extra 'Solutions' word
    assert results[0]['confidence'] > 0.70

def test_strict_currency_validation(engine, sample_invoices):
    """
    Test 4: Currency mismatch must prevent high-confidence Straight-Through Processing (STP).
    Cross-currency matching without an FX bridge is a major audit risk.
    """
    # Attempt to match a USD payment against a EUR invoice
    results = engine.run_match(1500.00, "Global Blue SE", "USD", sample_invoices)
    
    # Filter for matches that incorrectly claimed high confidence
    risky_matches = [r for r in results if r['Invoice_ID'] == 'INV-002' and r['confidence'] > 0.85]
    assert len(risky_matches) == 0, "Engine incorrectly gave high confidence to a currency mismatch."

def test_financial_kpi_calculations(engine, sample_invoices):
    """
    Test 5: Verify the Days Sales Outstanding (DSO) and debt calculation logic.
    """
    # Prepare DF for calculation
    calc_df = sample_invoices.copy()
    calc_df['Amount_Remaining'] = calc_df['Amount']
    
    dso = engine.calculate_dso(calc_df)
    total_ar = engine.get_total_outstanding(calc_df)
    
    assert isinstance(dso, (int, float))
    assert dso >= 0
    assert total_ar == 54000.00 # 50000 + 1500 + 2500

def test_empty_ledger_handling(engine):
    """
    Test 6: Robustness check. Ensure the engine doesn't crash on empty input.
    """
    empty_df = pd.DataFrame(columns=['Invoice_ID', 'Customer_Name', 'Amount', 'Currency'])
    results = engine.run_match(100.00, "Unknown Corp", "USD", empty_df)
    
    assert isinstance(results, list)
    assert len(results) == 0
