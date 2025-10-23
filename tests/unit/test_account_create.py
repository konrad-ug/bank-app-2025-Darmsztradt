from src.PersonalAccount import PersonalAccount
from src.company_account import CompanyAccount

class TestPersonalAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe","04242912345")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "04242912345"
    
    def test_pesel_too_long(self):
        account = PersonalAccount("Jane", "Smith","123456789012")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = PersonalAccount("Alice", "Johnson","123456789")
        assert account.pesel == "Invalid"
    
    def test_pesel_none(self):
        account = PersonalAccount("Bob", "Brown",None)
        assert account.pesel == "Invalid"
    
    def test_valid_promo_code(self):
        account = PersonalAccount("Charlie", "Davis","12345678901","PROM_225")
        assert account.balance == 50.0

    def test_promo_code_wrong_prefix(self):
        account = PersonalAccount("Eve", "White","12345678901","PROMO_225")
        assert account.balance == 0.0
    
    def test_promo_code_wrong_suffix(self):
        account = PersonalAccount("Eve", "White","12345678901","PROM_2255")
        assert account.balance == 0.0

    def test_promo_code_absent(self):
        account = PersonalAccount("Frank", "Green","12345678901")
        assert account.balance == 0.0

class TestTransfers:
    def test_outgoing_transfer_successful(self):
        account = PersonalAccount("Ivy", "Black","12345678901")
        account.balance = 100.0

        account.outgoing_transfer(30.0)

        assert account.balance == 70.0

    def test_incoming_transfer(self):
        account = PersonalAccount("Jack", "Hall","12345678901")
        account.incoming_transfer(15.0)
        assert account.balance == 15.0

    def test_outgoing_transfer_insufficient_funds(self):
        account = PersonalAccount("Kate", "King","12345678901")
        account.balance = 20.0
        
        account.outgoing_transfer(20.0)
        
        assert account.balance == 0.0
    def test_incoming_transfer_negative_amount(self):
        account = PersonalAccount("Liam", "Moore","12345678901")
        account.balance = 50.0
        
        account.incoming_transfer(-50.0)
        
        assert account.balance == 50.0

    def test_outgoing_transfer_negative_amount(self):
        account = PersonalAccount("Mia", "Scott","12345678901")
        account.balance = 50.0
        
        account.outgoing_transfer(-20.0)
        
        assert account.balance == 50.0

class TestCompanyAccount:
    def test_account_creation(self):
        account = CompanyAccount("TechCorp", "1234567890")
        assert account.name == "TechCorp"
        assert account.nip == "1234567890"
        assert account.balance == 0.0
    def test_nip_too_long(self):
        account = CompanyAccount("BiznessInc", "12345678901")
        assert account.nip == "Invalid"
    def test_nip_too_short(self):
        account = CompanyAccount("EnterprisesLLC", "123456789")
        assert account.nip == "Invalid"
    def test_nip_none(self):
        account = CompanyAccount("GlobalSolutions", None)
        assert account.nip == "Invalid"
    