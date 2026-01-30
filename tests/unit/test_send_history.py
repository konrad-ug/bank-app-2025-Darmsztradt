import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from src.account import PersonalAccount, BusinessAccount


@pytest.fixture
def mock_mf_api():
    with patch('src.account.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def personal_account():
    acc = PersonalAccount("John", "Doe", "12345678901")
    acc.history = [100, -1, 500]
    return acc


@pytest.fixture
def business_account(mock_mf_api):
    acc = BusinessAccount("TestCorp", "1234567890")
    acc.history = [5000, -1000, 500]
    return acc


class TestSendHistoryViaEmail:
    def test_personal_account_send_success(self, personal_account):
        with patch('src.account.SMTPClient') as MockSMTPClient:
            mock_smtp = MockSMTPClient.return_value
            mock_smtp.send.return_value = True
            
            result = personal_account.send_history_via_email("test@example.com")
            
            assert result is True
            mock_smtp.send.assert_called_once()
            call_args = mock_smtp.send.call_args
            today = date.today().strftime("%Y-%m-%d")
            assert call_args[0][0] == f"Account Transfer History {today}"
            assert call_args[0][1] == "Personal account history: [100, -1, 500]"
            assert call_args[0][2] == "test@example.com"

    def test_personal_account_send_failure(self, personal_account):
        with patch('src.account.SMTPClient') as MockSMTPClient:
            mock_smtp = MockSMTPClient.return_value
            mock_smtp.send.return_value = False
            
            result = personal_account.send_history_via_email("test@example.com")
            
            assert result is False
            mock_smtp.send.assert_called_once()

    def test_business_account_send_success(self, business_account):
        with patch('src.account.SMTPClient') as MockSMTPClient:
            mock_smtp = MockSMTPClient.return_value
            mock_smtp.send.return_value = True
            
            result = business_account.send_history_via_email("corp@example.com")
            
            assert result is True
            mock_smtp.send.assert_called_once()
            call_args = mock_smtp.send.call_args
            today = date.today().strftime("%Y-%m-%d")
            assert call_args[0][0] == f"Account Transfer History {today}"
            assert call_args[0][1] == "Company account history: [5000, -1000, 500]"
            assert call_args[0][2] == "corp@example.com"

    def test_business_account_send_failure(self, business_account):
        with patch('src.account.SMTPClient') as MockSMTPClient:
            mock_smtp = MockSMTPClient.return_value
            mock_smtp.send.return_value = False
            
            result = business_account.send_history_via_email("corp@example.com")
            
            assert result is False
            mock_smtp.send.assert_called_once()

    def test_email_subject_contains_today_date(self, personal_account):
        with patch('src.account.SMTPClient') as MockSMTPClient:
            mock_smtp = MockSMTPClient.return_value
            mock_smtp.send.return_value = True
            
            personal_account.send_history_via_email("test@example.com")
            
            today = date.today().strftime("%Y-%m-%d")
            call_args = mock_smtp.send.call_args
            assert today in call_args[0][0]

    def test_empty_history_personal(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        with patch('src.account.SMTPClient') as MockSMTPClient:
            mock_smtp = MockSMTPClient.return_value
            mock_smtp.send.return_value = True
            
            acc.send_history_via_email("test@example.com")
            
            call_args = mock_smtp.send.call_args
            assert call_args[0][1] == "Personal account history: []"
