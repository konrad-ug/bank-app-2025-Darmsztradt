import pytest
from src.account import PersonalAccount, BusinessAccount


@pytest.fixture
def personal_account_with_balance():
    acc = PersonalAccount("John", "Doe", "12345678901")
    acc.balance = 1000.0
    return acc


class TestAccountHistory:
    def test_history_starts_empty(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        assert acc.history == []

    def test_standard_transfer_history(self, personal_account_with_balance):
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        personal_account_with_balance.transfer(acc2, 200.0)
        
        assert personal_account_with_balance.history == [-200.0]
        assert acc2.history == [200.0]

    @pytest.mark.parametrize("account_type,expected_fee", [
        ("personal", -1.0),
        ("business", -5.0),
    ])
    def test_express_transfer_history(self, account_type, expected_fee):
        if account_type == "personal":
            acc1 = PersonalAccount("John", "Doe", "12345678901")
            acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        else:
            acc1 = BusinessAccount("Corp", "1234567890")
            acc2 = BusinessAccount("OtherCorp", "0987654321")
        
        acc1.balance = 1000.0
        acc1.express_transfer(acc2, 300.0)
        
        assert acc1.history == [-300.0, expected_fee]
        assert acc2.history == [300.0]

    def test_mixed_operations_example_scenario(self):
        my_acc = PersonalAccount("Me", "Me", "12345678901")
        sender = PersonalAccount("Sender", "Person", "09876543210")
        receiver = PersonalAccount("Receiver", "Person", "98765432109")
        
        sender.balance = 1000.0
        sender.transfer(my_acc, 500.0)
        my_acc.express_transfer(receiver, 300.0)
        
        assert my_acc.history == [500.0, -300.0, -1.0]
