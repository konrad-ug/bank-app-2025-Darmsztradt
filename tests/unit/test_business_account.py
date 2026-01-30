from src.account import BusinessAccount

class TestBusinessAccount:
    def test_business_account_creation(self):
        acc = BusinessAccount("MyCompany", "1234567890")
        assert acc.company_name == "MyCompany"
        assert acc.nip == "1234567890"
        assert acc.balance == 0.0

    def test_business_account_invalid_nip(self):
        acc = BusinessAccount("MyCompany", "123")
        assert acc.nip == "Invalid"

        acc2 = BusinessAccount("MyCompany", "12345678901")
        assert acc2.nip == "Invalid"
    
    def test_business_account_no_promo(self):
        pass 
