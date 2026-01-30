import pytest
from src.account import PersonalAccount
from src.accounts_registry import AccountsRegistry


@pytest.fixture
def registry():
    return AccountsRegistry()


@pytest.fixture
def sample_accounts():
    return [
        PersonalAccount("John", "Doe", "12345678901"),
        PersonalAccount("Jane", "Smith", "09876543210"),
        PersonalAccount("Bob", "Brown", "11122233344"),
    ]


class TestAccountsRegistry:
    def test_registry_starts_empty(self, registry):
        assert registry.get_count() == 0
        assert registry.get_all_accounts() == []

    def test_add_account(self, registry, sample_accounts):
        registry.add_account(sample_accounts[0])
        
        assert registry.get_count() == 1
        assert sample_accounts[0] in registry.get_all_accounts()

    def test_add_multiple_accounts(self, registry, sample_accounts):
        for acc in sample_accounts:
            registry.add_account(acc)
        
        assert registry.get_count() == 3
        assert registry.get_all_accounts() == sample_accounts

    @pytest.mark.parametrize("pesel,expected_name", [
        ("12345678901", "John"),
        ("09876543210", "Jane"),
        ("11122233344", "Bob"),
    ])
    def test_find_by_pesel(self, registry, sample_accounts, pesel, expected_name):
        for acc in sample_accounts:
            registry.add_account(acc)
        
        found = registry.find_by_pesel(pesel)
        
        assert found is not None
        assert found.first_name == expected_name

    def test_find_by_pesel_not_found(self, registry, sample_accounts):
        for acc in sample_accounts:
            registry.add_account(acc)
        
        found = registry.find_by_pesel("99999999999")
        
        assert found is None
