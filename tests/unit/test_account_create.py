from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe","04242912345")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "04242912345"
    
    def test_pesel_too_long(self):
        account = Account("Jane", "Smith","123456789012")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = Account("Alice", "Johnson","123456789")
        assert account.pesel == "Invalid"
    
    def test_pesel_none(self):
        account = Account("Bob", "Brown",None)
        assert account.pesel == "Invalid"
    
    def test_valid_promo_code(self):
        account = Account("Charlie", "Davis","12345678901","PROM_225")
        assert account.balance == 50.0

    def test_promo_code_wrong_prefix(self):
        account = Account("Eve", "White","12345678901","PROMO_225")
        assert account.balance == 0.0
    
    def test_promo_code_wrong_suffix(self):
        account = Account("Eve", "White","12345678901","PROM_2255")
        assert account.balance == 0.0

    def test_promo_code_absent(self):
        account = Account("Frank", "Green","12345678901")
        assert account.balance == 0.0