from src.account import PersonalAccount

class TestLoans:
    def test_loan_approved_three_deposits(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.history = [100.0, 200.0, 300.0]
        acc.balance = 600.0
        
        result = acc.submit_for_loan(500.0)
        
        assert result is True
        assert acc.balance == 1100.0

    def test_loan_approved_sum_of_five(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.history = [-100.0, 500.0, -50.0, 200.0, 100.0]
        acc.balance = 650.0
        
        result = acc.submit_for_loan(600.0)
        
        assert result is True
        assert acc.balance == 1250.0

    def test_loan_denied_not_enough_transactions(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.history = [100.0, 200.0]
        acc.balance = 300.0
        
        result = acc.submit_for_loan(100.0)
        
        assert result is False
        assert acc.balance == 300.0

    def test_loan_denied_conditions_not_met(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.history = [-100.0, -200.0, -300.0, 50.0, 60.0]
        acc.balance = 100.0
        
        result = acc.submit_for_loan(1000.0)
        
        assert result is False
        assert acc.balance == 100.0

    def test_loan_with_express_fee_in_history(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.history = [500.0, -100.0, -1.0, 200.0, 300.0]
        acc.balance = 900.0
        
        result = acc.submit_for_loan(800.0)
        
        assert result is True
        assert acc.balance == 1700.0

    def test_loan_denied_last_three_not_all_positive(self):
        acc = PersonalAccount("John", "Doe", "12345678901")
        acc.history = [100.0, -50.0, 200.0]
        acc.balance = 250.0
        
        result = acc.submit_for_loan(100.0)
        
        assert result is False
        assert acc.balance == 250.0
