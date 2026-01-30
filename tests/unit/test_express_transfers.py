from src.account import PersonalAccount, BusinessAccount

class TestExpressTransfers:
    def test_express_transfer_personal(self):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 100.0
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        acc1.express_transfer(acc2, 50.0)
        
        # Balance = 100 - 50 (transfer) - 1 (fee) = 49
        assert acc1.balance == 49.0
        assert acc2.balance == 50.0

    def test_express_transfer_business(self):
        acc1 = BusinessAccount("Corp", "1234567890")
        acc1.balance = 100.0
        acc2 = BusinessAccount("OtherCorp", "0987654321")
        
        acc1.express_transfer(acc2, 50.0)
        
        # Balance = 100 - 50 (transfer) - 5 (fee) = 45
        assert acc1.balance == 45.0
        assert acc2.balance == 50.0
    
    def test_express_transfer_insufficient_funds(self):
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 20.0
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        # Fee is 1. Amount 50. Balance 20. 20 < 50, so no transfer.
        acc1.express_transfer(acc2, 50.0)
        
        assert acc1.balance == 20.0
        assert acc2.balance == 0.0

    def test_express_transfer_negative_balance_allowed(self):
        # Feature 8: "Saldo może zejść poniżej 0 (maksymalnie o kwotę opłaty)"
        # Implies if Balance >= Amount, proceed.
        # Example: Balance 50. Transfer 50. Fee 1.
        # 50 >= 50 -> OK.
        # New balance: 50 - 50 - 1 = -1.
        
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc1.balance = 50.0
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        acc1.express_transfer(acc2, 50.0)
        
        assert acc1.balance == -1.0
        assert acc2.balance == 50.0

    def test_express_transfer_negative_balance_business(self):
        acc1 = BusinessAccount("Corp", "1234567890")
        acc1.balance = 50.0
        acc2 = BusinessAccount("OtherCorp", "0987654321")
        
        acc1.express_transfer(acc2, 50.0)
        
        assert acc1.balance == -5.0
        assert acc2.balance == 50.0
