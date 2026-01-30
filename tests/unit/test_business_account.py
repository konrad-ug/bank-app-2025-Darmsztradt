import pytest
from unittest.mock import patch, MagicMock
from src.account import BusinessAccount


@pytest.fixture
def mock_mf_api_valid():
    with patch('src.account.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny",
                    "name": "Test Company"
                }
            }
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_mf_api_invalid():
    with patch('src.account.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": None
            }
        }
        mock_get.return_value = mock_response
        yield mock_get


class TestBusinessAccount:
    def test_business_account_creation(self, mock_mf_api_valid):
        acc = BusinessAccount("MyCompany", "1234567890")
        assert acc.company_name == "MyCompany"
        assert acc.nip == "1234567890"
        assert acc.balance == 0.0

    @pytest.mark.parametrize("nip,expected", [
        ("123", "Invalid"),
        ("12345678901", "Invalid"),
    ])
    def test_business_account_invalid_nip_length(self, nip, expected):
        acc = BusinessAccount("MyCompany", nip)
        assert acc.nip == expected

    def test_business_account_nip_not_registered(self, mock_mf_api_invalid):
        with pytest.raises(ValueError) as excinfo:
            BusinessAccount("MyCompany", "1234567890")
        assert str(excinfo.value) == "Company not registered!!"

    def test_validate_nip_with_mf_returns_true(self, mock_mf_api_valid):
        acc = BusinessAccount("MyCompany", "1234567890")
        assert acc.nip == "1234567890"

    def test_validate_nip_api_error(self):
        with patch('src.account.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            with pytest.raises(ValueError):
                BusinessAccount("MyCompany", "1234567890")
