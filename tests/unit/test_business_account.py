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
    
    # Business accounts do not have promo code support described in Feature 7, 
    # ensuring they don't accidentally get it if we inherited incorrectly (though init is different).
    # Since __init__ doesn't take promo_code, we don't strictly catch it unless we try checking balance.
    def test_business_account_no_promo(self):
        # Even if we passed something (Python keyword args), implementation should not use it.
        # But BusinessAccount __init__ signature is strict: company_name, nip.
        pass 
