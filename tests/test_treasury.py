import pytest
from backend.treasury import TreasuryManager

@pytest.fixture
def treasury():
    """Initializes the Treasury Manager for unit testing."""
    return TreasuryManager()

def test_fx_conversion_logic(treasury):
    """
    Test 1: Verifies currency conversion accuracy.
    Ensures the engine correctly applies exchange rates to multi-currency flows.
    """
    # Test converting 1000 units from EUR to USD
    # Expected result depends on your engine's internal rate (e.g., 1.1)
    result = treasury.convert_currency(1000, "EUR", "USD")
    
    assert result > 0
    assert isinstance(result, (int, float))
    # Basic sanity check: 1000 EUR should currently be > 1000 USD
    assert result > 1000 

def test_liquidity_buffer_alerts(treasury):
    """
    Test 2: Validates the Risk Alerting system.
    If cash on hand falls below the threshold, a 'CRITICAL' status must be returned.
    """
    # Scenario: Current Cash = $4,000, Required Buffer = $5,000
    alert_status = treasury.check_liquidity_buffer(4000, 5000)
    
    assert "CRITICAL" in alert_status.upper()
    assert "BELOW THRESHOLD" in alert_status.upper()

    # Scenario: Healthy Liquidity
    healthy_status = treasury.check_liquidity_buffer(15000, 5000)
    assert "HEALTHY" in healthy_status.upper()

def test_investment_sweep_math(treasury):
    """
    Test 3: Verifies 'Idle Cash' optimization.
    Calculates how much capital should be moved to overnight investments.
    """
    current_balance = 250000
    target_operating_balance = 100000
    
    # The sweep should be the surplus: 150,000
    sweep_amount = treasury.calculate_investment_sweep(current_balance, target_operating_balance)
    
    assert sweep_amount == 150000
    
    # Test zero-sweep scenario (balance below target)
    low_balance_sweep = treasury.calculate_investment_sweep(80000, 100000)
    assert low_balance_sweep == 0

def test_fx_exposure_report(treasury):
    """
    Test 4: Ensures the engine identifies currency concentration risk.
    """
    balances = {"USD": 50000, "EUR": 40000, "GBP": 10000}
    report = treasury.get_exposure_report(balances)
    
    assert "USD" in report
    assert report["USD"] == 0.5  # 50% of total 100k exposure
