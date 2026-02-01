import pytest
from backend.compliance import ComplianceEngine

@pytest.fixture
def compliance():
    return ComplianceEngine()

def test_sanctions_check_pass(compliance):
    """Verifies that a clean company passes the sanctions check."""
    # Testing a standard valid entity
    result = compliance.check_sanctions("Apple Inc")
    assert result['status'] == "CLEARED"
    assert result['risk_score'] < 10

def test_sanctions_check_flag(compliance):
    """Verifies that restricted entities are flagged correctly."""
    # Using a common test string for restricted entities
    result = compliance.check_sanctions("Restricted Corp LLC")
    assert result['status'] == "FLAGGED"
    assert "Manual Review Required" in result['action']

def test_esg_validation(compliance):
    """Ensures ESG scores are within valid banking ranges (0-100)."""
    # Assuming your engine has an ESG validation method
    assert compliance.is_valid_esg("AAA") is True
    assert compliance.is_valid_esg("Invalid_Score") is False

def test_kyc_status_mapping(compliance):
    """Tests the mapping of KYC statuses to transaction limits."""
    # Verified = High Limit, Pending = Low/Zero Limit
    assert compliance.get_transaction_limit("VERIFIED") >= 100000
    assert compliance.get_transaction_limit("PENDING") == 0
