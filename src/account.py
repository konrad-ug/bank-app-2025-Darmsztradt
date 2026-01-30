import os
import requests
from datetime import date


class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def transfer(self, target_account, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)
            target_account.balance += amount
            target_account.history.append(amount)

    def express_transfer(self, target_account, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)
            self.balance -= self.express_transfer_fee
            self.history.append(-self.express_transfer_fee)
            target_account.balance += amount
            target_account.history.append(amount)


class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.express_transfer_fee = 1

        if promo_code is not None and self.is_promo_code_valid(promo_code):
            if self.get_birth_year(self.pesel) > 1960:
                self.balance += 50.0

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11

    def is_promo_code_valid(self, promo_code):
        return (
            isinstance(promo_code, str)
            and promo_code.startswith("PROM_")
            and len(promo_code) == 8
        )

    def get_birth_year(self, pesel):
        if pesel == "Invalid":
            return 0
        
        try:
            year = int(pesel[0:2])
            month = int(pesel[2:4])
            
            if 80 < month <= 92:
                year += 1800
            elif 0 < month <= 12:
                year += 1900
            elif 20 < month <= 32:
                year += 2000
            elif 40 < month <= 52:
                year += 2100
            elif 60 < month <= 72:
                year += 2200
            return year
        except ValueError:
            return 0

    def submit_for_loan(self, amount):
        if self._last_three_are_deposits() or self._sum_of_last_five_exceeds(amount):
            self.balance += amount
            return True
        return False

    def _last_three_are_deposits(self):
        if len(self.history) >= 3:
            return all(t > 0 for t in self.history[-3:])
        return False

    def _sum_of_last_five_exceeds(self, amount):
        if len(self.history) >= 5:
            return sum(self.history[-5:]) > amount
        return False



class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.express_transfer_fee = 5
        
        if len(nip) != 10:
            self.nip = "Invalid"
        else:
            if not self.validate_nip_with_mf(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip

    def validate_nip_with_mf(self, nip):
        base_url = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().strftime("%Y-%m-%d")
        url = f"{base_url}/api/search/nip/{nip}?date={today}"
        
        try:
            response = requests.get(url)
            print(f"MF API Response: {response.json()}")
            
            if response.status_code == 200:
                data = response.json()
                subject = data.get("result", {}).get("subject")
                if subject and subject.get("statusVat") == "Czynny":
                    return True
            return False
        except Exception as e:
            print(f"MF API Error: {e}")
            return False

    def take_loan(self, amount):
        if self.balance >= 2 * amount and -1775.0 in self.history:
            self.balance += amount
            return True
        return False