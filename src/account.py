
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
            return 0 # Or handle appropriately, currently preventing crash if invalid
        
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


class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.nip = nip if len(nip) == 10 else "Invalid"
        self.express_transfer_fee = 5