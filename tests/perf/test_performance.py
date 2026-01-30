import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 0.5


class TestPerformance:
    def test_create_and_delete_100_accounts(self):
        for i in range(100):
            pesel = f"1234567{i:04d}"
            
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/accounts",
                json={"name": f"User{i}", "surname": f"Test{i}", "pesel": pesel},
                timeout=TIMEOUT
            )
            elapsed = time.time() - start
            
            assert response.status_code == 201, f"Create failed for account {i}"
            assert elapsed < TIMEOUT, f"Create took {elapsed}s, expected < {TIMEOUT}s"
            
            start = time.time()
            response = requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
            elapsed = time.time() - start
            
            assert response.status_code == 200, f"Delete failed for account {i}"
            assert elapsed < TIMEOUT, f"Delete took {elapsed}s, expected < {TIMEOUT}s"

    def test_100_incoming_transfers(self):
        pesel = "99988877766"
        requests.post(
            f"{BASE_URL}/api/accounts",
            json={"name": "TransferTest", "surname": "User", "pesel": pesel},
            timeout=TIMEOUT
        )
        
        expected_balance = 0
        for i in range(100):
            amount = 100 + i
            expected_balance += amount
            
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/accounts/{pesel}/transfer",
                json={"amount": amount, "type": "incoming"},
                timeout=TIMEOUT
            )
            elapsed = time.time() - start
            
            assert response.status_code == 200, f"Transfer {i} failed"
            assert elapsed < TIMEOUT, f"Transfer took {elapsed}s, expected < {TIMEOUT}s"
        
        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
        assert response.status_code == 200
        assert response.json()["balance"] == expected_balance
        
        requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)

    def test_create_1000_then_delete_all(self):
        pesels = []
        
        for i in range(1000):
            pesel = f"5555{i:07d}"
            pesels.append(pesel)
            
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/accounts",
                json={"name": f"Bulk{i}", "surname": f"User{i}", "pesel": pesel},
                timeout=TIMEOUT
            )
            elapsed = time.time() - start
            
            assert response.status_code == 201, f"Create failed for account {i}"
            assert elapsed < TIMEOUT, f"Create took {elapsed}s"
        
        for i, pesel in enumerate(pesels):
            start = time.time()
            response = requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT)
            elapsed = time.time() - start
            
            assert response.status_code == 200, f"Delete failed for account {i}"
            assert elapsed < TIMEOUT, f"Delete took {elapsed}s"
