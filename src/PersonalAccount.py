from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 0.0
        if promo_code is not None and self.is_promo_code_valid(promo_code):
            self.balance += 50.0
        self.history = []

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11

    def is_promo_code_valid(self, promo_code):
        return (
            isinstance(promo_code, str)
            and promo_code.startswith("PROM_")
            and len(promo_code) == 8
        )
    def submit_for_loan(self, amount):
        if self.is_eligible_for_loan(amount):
            self.balance += amount
            return True
        return False
    
    def is_eligible_for_loan(self, amount):
        return all(x > 0 for x in self.history[:-3]) or sum(self.history[:-5]) > amount