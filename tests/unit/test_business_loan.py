import pytest
from unittest.mock import patch, MagicMock
from src.account import BusinessAccount


@pytest.fixture
def mock_mf_api_valid():
    with patch('src.account.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny",
                    "name": "Test Company"
                }
            }
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def business_account(mock_mf_api_valid):
    return BusinessAccount("TestCorp", "1234567890")


class TestBusinessLoan:
    @pytest.mark.parametrize("balance,history,amount,expected_result,expected_balance", [
        (2000.0, [-1775.0, 100.0], 1000.0, True, 3000.0),
        (5000.0, [-500.0, -1775.0, 200.0], 2000.0, True, 7000.0),
        (1000.0, [-1775.0], 600.0, False, 1000.0),
        (2000.0, [-500.0, 100.0], 1000.0, False, 2000.0),
        (1000.0, [-100.0], 500.0, False, 1000.0),
        (3000.0, [-1775.0], 1500.0, True, 4500.0),
    ])
    def test_business_loan_scenarios(self, business_account, balance, history, amount, expected_result, expected_balance):
        business_account.balance = balance
        business_account.history = history
        
        result = business_account.take_loan(amount)
        
        assert result is expected_result
        assert business_account.balance == expected_balance
