import pytest
from src.account import PersonalAccount, BusinessAccount


class TestExpressTransfers:
    @pytest.mark.parametrize("account_type,initial_balance,amount,expected_sender,expected_receiver", [
        ("personal", 100.0, 50.0, 49.0, 50.0),
        ("business", 100.0, 50.0, 45.0, 50.0),
        ("personal", 20.0, 50.0, 20.0, 0.0),
        ("personal", 50.0, 50.0, -1.0, 50.0),
        ("business", 50.0, 50.0, -5.0, 50.0),
    ])
    def test_express_transfer_scenarios(self, account_type, initial_balance, amount, expected_sender, expected_receiver):
        if account_type == "personal":
            acc1 = PersonalAccount("John", "Doe", "12345678901")
            acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        else:
            acc1 = BusinessAccount("Corp", "1234567890")
            acc2 = BusinessAccount("OtherCorp", "0987654321")
        
        acc1.balance = initial_balance
        acc1.express_transfer(acc2, amount)
        
        assert acc1.balance == expected_sender
        assert acc2.balance == expected_receiver
