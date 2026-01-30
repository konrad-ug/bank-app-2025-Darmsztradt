import pytest
from src.account import BusinessAccount


@pytest.fixture
def business_account():
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
