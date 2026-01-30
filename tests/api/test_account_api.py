import pytest
from app.api import app, registry
from src.account import PersonalAccount


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_registry():
    registry.accounts.clear()
    yield
    registry.accounts.clear()


class TestAccountsAPI:
    def test_create_account(self, client):
        response = client.post('/api/accounts', json={
            "name": "James",
            "surname": "Hetfield",
            "pesel": "89092909825"
        })
        
        assert response.status_code == 201
        assert response.get_json()["message"] == "Account created"

    def test_get_all_accounts_empty(self, client):
        response = client.get('/api/accounts')
        
        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_all_accounts_with_data(self, client):
        client.post('/api/accounts', json={"name": "John", "surname": "Doe", "pesel": "12345678901"})
        client.post('/api/accounts', json={"name": "Jane", "surname": "Smith", "pesel": "09876543210"})
        
        response = client.get('/api/accounts')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    def test_get_account_count(self, client):
        response = client.get('/api/accounts/count')
        assert response.status_code == 200
        assert response.get_json()["count"] == 0
        
        client.post('/api/accounts', json={"name": "Test", "surname": "User", "pesel": "11122233344"})
        
        response = client.get('/api/accounts/count')
        assert response.get_json()["count"] == 1

    def test_get_account_by_pesel(self, client):
        client.post('/api/accounts', json={"name": "James", "surname": "Hetfield", "pesel": "89092909825"})
        
        response = client.get('/api/accounts/89092909825')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "James"
        assert data["surname"] == "Hetfield"
        assert data["pesel"] == "89092909825"

    def test_get_account_by_pesel_not_found(self, client):
        response = client.get('/api/accounts/99999999999')
        
        assert response.status_code == 404
        assert response.get_json()["error"] == "Account not found"

    def test_update_account(self, client):
        client.post('/api/accounts', json={"name": "James", "surname": "Hetfield", "pesel": "89092909825"})
        
        response = client.patch('/api/accounts/89092909825', json={"name": "Lars"})
        
        assert response.status_code == 200
        
        get_response = client.get('/api/accounts/89092909825')
        assert get_response.get_json()["name"] == "Lars"
        assert get_response.get_json()["surname"] == "Hetfield"

    def test_update_account_not_found(self, client):
        response = client.patch('/api/accounts/99999999999', json={"name": "Test"})
        
        assert response.status_code == 404

    def test_delete_account(self, client):
        client.post('/api/accounts', json={"name": "James", "surname": "Hetfield", "pesel": "89092909825"})
        
        response = client.delete('/api/accounts/89092909825')
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account deleted"
        
        get_response = client.get('/api/accounts/89092909825')
        assert get_response.status_code == 404

    def test_delete_account_not_found(self, client):
        response = client.delete('/api/accounts/99999999999')
        
        assert response.status_code == 404


class TestUniquePesel:
    def test_create_duplicate_pesel_returns_409(self, client):
        client.post('/api/accounts', json={"name": "James", "surname": "Hetfield", "pesel": "89092909825"})
        
        response = client.post('/api/accounts', json={"name": "Lars", "surname": "Ulrich", "pesel": "89092909825"})
        
        assert response.status_code == 409
        assert "already exists" in response.get_json()["error"]


class TestTransfersAPI:
    @pytest.fixture
    def account_with_balance(self, client):
        client.post('/api/accounts', json={"name": "James", "surname": "Hetfield", "pesel": "89092909825"})
        client.post('/api/accounts/89092909825/transfer', json={"amount": 1000, "type": "incoming"})
        return "89092909825"

    def test_incoming_transfer(self, client):
        client.post('/api/accounts', json={"name": "James", "surname": "Hetfield", "pesel": "89092909825"})
        
        response = client.post('/api/accounts/89092909825/transfer', json={"amount": 500, "type": "incoming"})
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
        
        acc_response = client.get('/api/accounts/89092909825')
        assert acc_response.get_json()["balance"] == 500

    def test_outgoing_transfer_success(self, client, account_with_balance):
        response = client.post(f'/api/accounts/{account_with_balance}/transfer', json={"amount": 300, "type": "outgoing"})
        
        assert response.status_code == 200
        
        acc_response = client.get(f'/api/accounts/{account_with_balance}')
        assert acc_response.get_json()["balance"] == 700

    def test_outgoing_transfer_insufficient_funds(self, client, account_with_balance):
        response = client.post(f'/api/accounts/{account_with_balance}/transfer', json={"amount": 2000, "type": "outgoing"})
        
        assert response.status_code == 422
        assert response.get_json()["error"] == "Insufficient funds"

    def test_express_transfer_success(self, client, account_with_balance):
        response = client.post(f'/api/accounts/{account_with_balance}/transfer', json={"amount": 500, "type": "express"})
        
        assert response.status_code == 200
        
        acc_response = client.get(f'/api/accounts/{account_with_balance}')
        assert acc_response.get_json()["balance"] == 499

    def test_express_transfer_insufficient_funds(self, client, account_with_balance):
        response = client.post(f'/api/accounts/{account_with_balance}/transfer', json={"amount": 2000, "type": "express"})
        
        assert response.status_code == 422

    def test_transfer_account_not_found(self, client):
        response = client.post('/api/accounts/99999999999/transfer', json={"amount": 100, "type": "incoming"})
        
        assert response.status_code == 404

    def test_transfer_unknown_type(self, client, account_with_balance):
        response = client.post(f'/api/accounts/{account_with_balance}/transfer', json={"amount": 100, "type": "unknown"})
        
        assert response.status_code == 400
        assert response.get_json()["error"] == "Unknown transfer type"
