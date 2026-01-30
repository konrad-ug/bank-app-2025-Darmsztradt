from src.account import PersonalAccount, BusinessAccount

class TestTransfers:
    def test_transfer_sufficient_funds(self):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 100.0
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        acc1.transfer(acc2, 50.0)
        
        assert acc1.balance == 50.0
        assert acc2.balance == 50.0

    def test_transfer_insufficient_funds(self):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 20.0
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        acc1.transfer(acc2, 50.0)
        
        assert acc1.balance == 20.0
        assert acc2.balance == 0.0

    def test_transfer_between_different_account_types(self):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 200.0
        acc2 = BusinessAccount("Corp", "1234567890")
        
        acc1.transfer(acc2, 100.0)
        
        assert acc1.balance == 100.0
        assert acc2.balance == 100.0
