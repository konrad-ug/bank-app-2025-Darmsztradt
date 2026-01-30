import pytest
from src.account import PersonalAccount as Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "04242912345")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "04242912345"

    @pytest.mark.parametrize("pesel,expected", [
        ("123456789012", "Invalid"),
        ("123456789", "Invalid"),
        (None, "Invalid"),
    ])
    def test_invalid_pesel(self, pesel, expected):
        account = Account("Test", "User", pesel)
        assert account.pesel == expected

    @pytest.mark.parametrize("pesel,promo_code,expected_balance", [
        ("61042912345", "PROM_225", 50.0),
        ("61042912345", "PROMO_225", 0.0),
        ("61042912345", "PROM_2255", 0.0),
        ("61042912345", None, 0.0),
        ("60042912345", "PROM_123", 0.0),
        ("50042912345", "PROM_123", 0.0),
        ("00242912345", "PROM_123", 50.0),
    ])
    def test_promo_code_scenarios(self, pesel, promo_code, expected_balance):
        account = Account("Test", "User", pesel, promo_code)
        assert account.balance == expected_balance