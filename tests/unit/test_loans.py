import pytest
from src.account import PersonalAccount


@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "12345678901")


class TestLoans:
    @pytest.mark.parametrize("history,balance,amount,expected_result,expected_balance", [
        ([100.0, 200.0, 300.0], 600.0, 500.0, True, 1100.0),
        ([-100.0, 500.0, -50.0, 200.0, 100.0], 650.0, 600.0, True, 1250.0),
        ([500.0, -100.0, -1.0, 200.0, 300.0], 900.0, 800.0, True, 1700.0),
        ([100.0, 200.0], 300.0, 100.0, False, 300.0),
        ([-100.0, -200.0, -300.0, 50.0, 60.0], 100.0, 1000.0, False, 100.0),
        ([100.0, -50.0, 200.0], 250.0, 100.0, False, 250.0),
    ])
    def test_loan_scenarios(self, personal_account, history, balance, amount, expected_result, expected_balance):
        personal_account.history = history
        personal_account.balance = balance
        
        result = personal_account.submit_for_loan(amount)
        
        assert result is expected_result
        assert personal_account.balance == expected_balance
