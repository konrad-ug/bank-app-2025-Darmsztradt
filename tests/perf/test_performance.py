import pytest
import requests


BASE_URL = "http://localhost:5000"
TIMEOUT = 0.5


class TestPerformance:
    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield
        # Clean up after tests
        try:
            response = requests.get(f"{BASE_URL}/api/accounts", timeout=TIMEOUT)
            if response.status_code == 200:
                accounts = response.json()
                for acc in accounts:
                    requests.delete(f"{BASE_URL}/api/accounts/{acc['pesel']}", timeout=TIMEOUT)
        except:
            pass

    def test_create_and_delete_100_accounts(self):
        for i in range(100):
            pesel = f"{i:011d}"
            
            create_response = requests.post(
                f"{BASE_URL}/api/accounts",
                json={"name": f"User{i}", "surname": f"Test{i}", "pesel": pesel},
                timeout=TIMEOUT
            )
            assert create_response.status_code == 201
            
            delete_response = requests.delete(
                f"{BASE_URL}/api/accounts/{pesel}",
                timeout=TIMEOUT
            )
            assert delete_response.status_code == 200

    def test_100_incoming_transfers(self):
        pesel = "99999999999"
        
        create_response = requests.post(
            f"{BASE_URL}/api/accounts",
            json={"name": "Transfer", "surname": "Test", "pesel": pesel},
            timeout=TIMEOUT
        )
        assert create_response.status_code == 201
        
        for i in range(100):
            transfer_response = requests.post(
                f"{BASE_URL}/api/accounts/{pesel}/transfer",
                json={"amount": 100, "type": "incoming"},
                timeout=TIMEOUT
            )
            assert transfer_response.status_code == 200
        
        account_response = requests.get(
            f"{BASE_URL}/api/accounts/{pesel}",
            timeout=TIMEOUT
        )
        assert account_response.status_code == 200
        assert account_response.json()["balance"] == 10000.0
        
        requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)

    def test_create_1000_then_delete_all(self):
        pesels = []
        
        for i in range(1000):
            pesel = f"{i:011d}"
            pesels.append(pesel)
            
            create_response = requests.post(
                f"{BASE_URL}/api/accounts",
                json={"name": f"User{i}", "surname": f"Test{i}", "pesel": pesel},
                timeout=TIMEOUT
            )
            assert create_response.status_code == 201
        
        for pesel in pesels:
            delete_response = requests.delete(
                f"{BASE_URL}/api/accounts/{pesel}",
                timeout=TIMEOUT
            )
            assert delete_response.status_code == 200
