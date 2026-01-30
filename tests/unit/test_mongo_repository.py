import pytest
from unittest.mock import patch, MagicMock
from src.accounts_repository import MongoAccountsRepository
from src.account import PersonalAccount


class TestMongoAccountsRepository:
    @pytest.fixture
    def mock_collection(self, mocker):
        mock_client = mocker.patch('src.accounts_repository.MongoClient')
        mock_db = MagicMock()
        mock_coll = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_coll
        return mock_coll

    def test_save_all_clears_collection_first(self, mock_collection):
        repo = MongoAccountsRepository()
        acc = PersonalAccount("John", "Doe", "12345678901")
        
        repo.save_all([acc])
        
        mock_collection.delete_many.assert_called_once_with({})

    def test_save_all_upserts_accounts(self, mock_collection):
        repo = MongoAccountsRepository()
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.balance = 100.0
        acc.history = [100.0]
        
        repo.save_all([acc])
        
        mock_collection.update_one.assert_called_once()
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"pesel": "12345678901"}
        assert call_args[1]["upsert"] is True

    def test_save_all_multiple_accounts(self, mock_collection):
        repo = MongoAccountsRepository()
        acc1 = PersonalAccount("John", "Doe", "12345678901")
        acc2 = PersonalAccount("Jane", "Doe", "09876543210")
        
        repo.save_all([acc1, acc2])
        
        assert mock_collection.update_one.call_count == 2

    def test_load_all_returns_documents(self, mock_collection):
        mock_collection.find.return_value = [
            {"first_name": "John", "last_name": "Doe", "pesel": "12345678901", "balance": 100.0, "history": [100.0]},
            {"first_name": "Jane", "last_name": "Doe", "pesel": "09876543210", "balance": 200.0, "history": [200.0]}
        ]
        
        repo = MongoAccountsRepository()
        result = repo.load_all()
        
        assert len(result) == 2
        assert result[0]["first_name"] == "John"
        assert result[1]["first_name"] == "Jane"

    def test_load_all_empty_collection(self, mock_collection):
        mock_collection.find.return_value = []
        
        repo = MongoAccountsRepository()
        result = repo.load_all()
        
        assert result == []

    def test_clear_deletes_all(self, mock_collection):
        repo = MongoAccountsRepository()
        
        repo.clear()
        
        mock_collection.delete_many.assert_called_once_with({})
