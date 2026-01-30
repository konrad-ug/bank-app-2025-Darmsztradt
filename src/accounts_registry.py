from src.account import PersonalAccount


class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def find_by_pesel(self, pesel: str):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_all_accounts(self):
        return self.accounts

    def get_count(self):
        return len(self.accounts)
