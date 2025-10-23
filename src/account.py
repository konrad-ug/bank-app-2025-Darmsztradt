class Account:
    def __init__(self):
        self.balance = 0.0
    
    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount

    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount