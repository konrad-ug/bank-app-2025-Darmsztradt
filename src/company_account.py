from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip):
        self.name = name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0.0
        self.express_transfer_fee = 5.0
    
    def is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10 and nip.isdigit()