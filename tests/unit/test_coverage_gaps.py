import pytest
from src.account import PersonalAccount


class TestCoverageGaps:
    @pytest.mark.parametrize("pesel,expected_balance", [
        ("short", 0.0),
        ("00810112345", 0.0),
        ("23410112345", 50.0),
        ("23610112345", 50.0),
        ("ab810112345", 0.0),
    ])
    def test_get_birth_year_edge_cases(self, pesel, expected_balance):
        acc = PersonalAccount("John", "Doe", pesel, "PROM_123")
        assert acc.balance == expected_balance

    def test_invalid_pesel_field(self):
        acc = PersonalAccount("John", "Doe", "short", "PROM_123")
        assert acc.pesel == "Invalid"
