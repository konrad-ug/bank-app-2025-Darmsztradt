from src.account import PersonalAccount

class TestCoverageGaps:
    """Tests to fill the code coverage gaps in account.py"""

    def test_get_birth_year_invalid_pesel(self):
        acc = PersonalAccount("John", "Doe", "short", "PROM_123")
        assert acc.pesel == "Invalid"
        assert acc.balance == 0.0

    def test_get_birth_year_1800s(self):
        acc = PersonalAccount("John", "Doe", "00810112345", "PROM_123")
        assert acc.balance == 0.0

    def test_get_birth_year_2100s(self):
        acc = PersonalAccount("John", "Doe", "23410112345", "PROM_123")
        assert acc.balance == 50.0

    def test_get_birth_year_2200s(self):
        acc = PersonalAccount("John", "Doe", "23610112345", "PROM_123")
        assert acc.balance == 50.0

    def test_get_birth_year_value_error(self):
        acc = PersonalAccount("John", "Doe", "ab810112345", "PROM_123")
        assert acc.balance == 0.0
