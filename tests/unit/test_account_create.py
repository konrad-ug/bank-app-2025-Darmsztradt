from src.account import PersonalAccount as Account


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
        account = Account("Charlie", "Davis","61042912345","PROM_225")
        assert account.balance == 50.0

    def test_promo_code_wrong_prefix(self):
        account = Account("Eve", "White","61042912345","PROMO_225")
        assert account.balance == 0.0
    
    def test_promo_code_wrong_suffix(self):
        account = Account("Eve", "White","61042912345","PROM_2255")
        assert account.balance == 0.0

    def test_promo_code_absent(self):
        account = Account("Frank", "Green","61042912345")
        assert account.balance == 0.0

    def test_promo_code_born_1960(self):
        account = Account("Old", "Promo", "60042912345", "PROM_123")
        assert account.balance == 0.0

    def test_promo_code_born_1950(self):
        account = Account("Older", "Promo", "50042912345", "PROM_123")
        assert account.balance == 0.0

    def test_promo_code_born_2000(self):
        account = Account("Young", "Promo", "00242912345", "PROM_123")
        assert account.balance == 50.0