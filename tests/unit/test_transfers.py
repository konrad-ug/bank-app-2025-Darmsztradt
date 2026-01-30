import pytest
from src.account import PersonalAccount, BusinessAccount


@pytest.fixture
def sender_account():
    acc = PersonalAccount("John", "Doe", "12345678901")
    acc.balance = 100.0
    return acc


@pytest.fixture
def receiver_account():
    return PersonalAccount("Jane", "Doe", "09876543210")


class TestTransfers:
    @pytest.mark.parametrize("initial_balance,amount,expected_sender,expected_receiver", [
        (100.0, 50.0, 50.0, 50.0),
        (20.0, 50.0, 20.0, 0.0),
    ])
    def test_transfer_scenarios(self, amount, initial_balance, expected_sender, expected_receiver):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = initial_balance
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        acc1.transfer(acc2, amount)
        
        assert acc1.balance == expected_sender
        assert acc2.balance == expected_receiver

    def test_transfer_between_different_account_types(self):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 200.0
        acc2 = BusinessAccount("Corp", "1234567890")
        
        acc1.transfer(acc2, 100.0)
        
        assert acc1.balance == 100.0
        assert acc2.balance == 100.0
