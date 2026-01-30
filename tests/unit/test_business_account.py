import pytest
from src.account import BusinessAccount


class TestBusinessAccount:
    def test_business_account_creation(self):
        acc = BusinessAccount("MyCompany", "1234567890")
        assert acc.company_name == "MyCompany"
        assert acc.nip == "1234567890"
        assert acc.balance == 0.0

    @pytest.mark.parametrize("nip,expected", [
        ("123", "Invalid"),
        ("12345678901", "Invalid"),
    ])
    def test_business_account_invalid_nip(self, nip, expected):
        acc = BusinessAccount("MyCompany", nip)
        assert acc.nip == expected
